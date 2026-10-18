"""ckr_server.py -- the checkers table server for LisaCheckers (and any FujiNet machine): every player dials
OUT to it over HTTP, so nobody opens a router port (Tim, 17-Oct-2026).  Python standard library only, so it
runs on the Pi as it is.  18-Oct-2026, REV A.

    python ckr_server.py [port]          (default 8090)

Requests are plain GETs, all with ?table=<id>&player=<name> (names: letters and digits, 8 at most, lower case):
    /tables                  the tables, one a line:  T|<id>|<name>|<players>/2|<lobby|play|over>
    /state                   sits you down if a seat is free (black first, then white), and the state
    /move/<11-15 or 22x15x8> your move; the state comes back (with ERROR <why> on the first line if refused)
    /resign  /draw  /leave   resign; offer or accept a draw (both send /draw); stand up
    /again                   after a game: ready for another, colours swapped

The state, one fact a line (LisaFuji's text reader takes it as it is):
    CK1
    status lobby|play|over
    you black|white|watch
    turn black|white|-
    black <name or ->
    white <name or ->
    board <32 characters, squares 1-32: . empty, b B black man / king, w W white man / king>
    last <the last move, or ->
    moves <how many moves so far>
    draw black|white|-        (who has offered a draw)
    legal <the moves of the player to move, space separated>
    result <text, or ->
    prompt <one line for the screen>

A seat is given up after IDLE seconds without a request; in a game that loses it.  40 moves each with only
kings moving and nothing taken is a draw (the LisaCheckers rule)."""
import sys, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs, unquote
import ckrules as R

IDLE = 300
TABLES = [("c1", "Checkers 1"), ("c2", "Checkers 2"), ("c3", "Checkers 3"), ("test", "Test table")]
LOCK = threading.Lock()


class Table:
    def __init__(self, tid, name):
        self.tid, self.name = tid, name
        self.seat = {R.BLACK: None, R.WHITE: None}
        self.seen = {}
        self.again = set()
        self.reset()

    def reset(self):
        self.board = R.start()
        self.turn = R.BLACK
        self.status = "lobby"
        self.last = "-"
        self.count = 0
        self.quiet = 0
        self.draw = None
        self.result = "-"

    def side_of(self, name):
        for side, who in self.seat.items():
            if who == name:
                return side
        return None

    def sit(self, name):
        if self.side_of(name) is None:
            for side in (R.BLACK, R.WHITE):
                if self.seat[side] is None:
                    self.seat[side] = name
                    break
        if self.status == "lobby" and self.seat[R.BLACK] and self.seat[R.WHITE]:
            self.status = "play"

    def finish(self, text):
        self.status = "over"
        self.result = text
        self.again = set()

    def tidy(self):
        """Give up seats nobody has asked about for IDLE seconds."""
        now = time.time()
        for side in (R.BLACK, R.WHITE):
            who = self.seat[side]
            if who and now - self.seen.get(who, now) > IDLE:
                self.seat[side] = None
                if self.status == "play":
                    self.finish("%s left: %s wins" % (who, self.seat[-side] or "the other side"))
        if self.status != "play" and not self.seat[R.BLACK] and not self.seat[R.WHITE]:
            self.reset()

    def state(self, name, error=None):
        side = self.side_of(name)
        you = {R.BLACK: "black", R.WHITE: "white", None: "watch"}[side]
        turn = {R.BLACK: "black", R.WHITE: "white"}[self.turn] if self.status == "play" else "-"
        legal = " ".join(R.text(m) for m in R.moves(self.board, self.turn)) if self.status == "play" else ""
        if error:
            prompt = error
        elif self.status == "lobby":
            prompt = "Waiting for a second player"
        elif self.status == "over":
            prompt = self.result + ".  /again for another game"
        elif side == self.turn:
            prompt = "Your move" + (": you must jump" if "x" in legal else "")
        elif side is None:
            prompt = "Watching"
        else:
            prompt = "Waiting for %s" % self.seat[self.turn]
        lines = ["ERROR " + error] if error else []
        lines += ["CK1", "status " + self.status, "you " + you, "turn " + turn,
                  "black " + (self.seat[R.BLACK] or "-"), "white " + (self.seat[R.WHITE] or "-"),
                  "board " + R.board_text(self.board), "last " + self.last, "moves %d" % self.count,
                  "draw " + ({R.BLACK: "black", R.WHITE: "white"}.get(self.draw, "-")),
                  "legal " + legal, "result " + self.result, "prompt " + prompt]
        return "\n".join(lines) + "\n"

    def move(self, name, text):
        side = self.side_of(name)
        if self.status != "play":
            return "the game is not on"
        if side != self.turn:
            return "it is not your move"
        mv = R.parse(self.board, side, text)
        if mv is None:
            return "%s is not a legal move" % text
        man = abs(self.board[mv[0][0]]) == 1
        R.play(self.board, mv)
        self.last = R.text(mv)
        self.count += 1
        self.draw = None
        self.quiet = 0 if (mv[1] or man) else self.quiet + 1
        self.turn = -self.turn
        if not R.moves(self.board, self.turn):
            self.finish("%s wins: %s cannot move" % (name, self.seat[self.turn]))
        elif self.quiet >= 80:
            self.finish("a draw: 40 moves each with only kings moving")
        return None


TAB = {tid: Table(tid, nm) for tid, nm in TABLES}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        sys.stdout.write("%s %s %s\n" % (time.strftime("%H:%M:%S"), self.client_address[0], fmt % args))

    def reply(self, text, code=200):
        body = text.encode("ascii", "replace")
        self.send_response(code)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = urlparse(self.path)
        q = parse_qs(u.query)
        path = unquote(u.path)
        with LOCK:
            for t in TAB.values():
                t.tidy()
            if path == "/tables":
                lines = []
                for t in TAB.values():
                    if t.tid == "test" and "dev" not in q:
                        continue
                    n = sum(1 for v in t.seat.values() if v)
                    lines.append("T|%s|%s|%d/2|%s" % (t.tid, t.name, n, t.status))
                return self.reply("\n".join(lines) + "\n")
            tid = (q.get("table", [""])[0] or "").lower()
            name = "".join(ch for ch in (q.get("player", [""])[0] or "").lower() if ch.isalnum())[:8]
            t = TAB.get(tid)
            if t is None or not name:
                return self.reply("ERROR give a table and a player name\n")
            t.seen[name] = time.time()
            err = None
            if path == "/state":
                t.sit(name)
            elif path.startswith("/move/"):
                err = t.move(name, path[6:])
            elif path == "/resign":
                side = t.side_of(name)
                if t.status == "play" and side:
                    t.finish("%s resigned: %s wins" % (name, t.seat[-side]))
            elif path == "/draw":
                side = t.side_of(name)
                if t.status == "play" and side:
                    if t.draw == -side:
                        t.finish("a draw, agreed")
                    else:
                        t.draw = side
            elif path == "/leave":
                side = t.side_of(name)
                if side:
                    t.seat[side] = None
                    if t.status == "play":
                        t.finish("%s left: %s wins" % (name, t.seat[-side] or "the other side"))
                return self.reply("BYE\n")
            elif path == "/again":
                if t.status == "over" and t.side_of(name):
                    t.again.add(name)
                    if t.seat[R.BLACK] and t.seat[R.WHITE] and len(t.again) == 2:
                        t.seat[R.BLACK], t.seat[R.WHITE] = t.seat[R.WHITE], t.seat[R.BLACK]
                        t.reset()
                        t.status = "play"
            else:
                return self.reply("ERROR unknown request\n", 404)
            return self.reply(t.state(name, err))


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    print("checkers table server on port", port, flush=True)
    ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
