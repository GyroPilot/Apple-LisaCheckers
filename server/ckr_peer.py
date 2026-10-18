"""ckr_peer.py -- test players for ckr_server.py: two clients play whole games of random legal moves on one
table, each checking every reply against its own copy of the rules (the board after the move, whose turn,
the legal list), plus the refusals (wrong turn, illegal move), resign, draw, leave and /again.
    python ckr_peer.py [host:port] [games]        18-Oct-2026"""
import random, sys, urllib.request
import ckrules as R

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1:8090"
GAMES = int(sys.argv[2]) if len(sys.argv) > 2 else 20


def get(path, player, table="test"):
    base = HOST if HOST.startswith("http") else "http://" + HOST       # a host:port, or a full address
    url = "%s%s?table=%s&player=%s" % (base, path, table, player)
    with urllib.request.urlopen(url, timeout=10) as r:
        text = r.read().decode()
    st = {}
    for line in text.splitlines():
        k, _, v = line.partition(" ")
        st[k] = v
    return st, text


def check(cond, what):
    if not cond:
        raise SystemExit("FAILED: " + what)


A, B = "peera", "peerb"
st, _ = get("/state", A)
check(st["status"] == "lobby" and st["you"] == "black", "first to sit is black, lobby")
st, _ = get("/state", B)
check(st["status"] == "play" and st["you"] == "white", "second is white, game on")
st, _ = get("/move/22-18", A)
check("ERROR" in st, "an illegal move is refused")
st, _ = get("/move/11-15", B)
check("ERROR" in st and "not your move" in st["ERROR"], "the wrong player is refused")

results = {}
for g in range(GAMES):
    board, side = R.start(), R.BLACK
    names = {R.BLACK: A, R.WHITE: B} if g % 2 == 0 else {R.BLACK: B, R.WHITE: A}
    n = 0
    while True:
        who = names[side]
        st, _ = get("/state", who)
        check(st["board"] == R.board_text(board), "board agrees, game %d move %d" % (g, n))
        legal = R.moves(board, side)
        if st["status"] == "play":           # (a finished game lists no moves, even a drawn one)
            check(sorted(st["legal"].split()) == sorted(R.text(m) for m in legal), "legal list agrees")
        if st["status"] == "over":
            break
        check(st["turn"] == ("black" if side == R.BLACK else "white"), "turn agrees")
        if g == 3 and n == 10:
            get("/resign", who)
            st, _ = get("/state", who)
            check(st["status"] == "over" and "resigned" in st["result"], "resign ends the game")
            break
        if g == 4 and n == 6:
            get("/draw", who)
            get("/draw", names[-side])
            st, _ = get("/state", who)
            check(st["status"] == "over" and "draw" in st["result"], "an agreed draw ends the game")
            break
        mv = random.choice(legal)
        txt = R.text(mv)
        if mv[1] and len(mv[0]) > 2 and random.random() < 0.5:   # the short form: from x to
            fits = [m for m in legal if m[0][0] == mv[0][0] and m[0][-1] == mv[0][-1]]
            if len(fits) == 1:
                txt = "%dx%d" % (mv[0][0], mv[0][-1])
        st, _ = get("/move/" + txt, who)
        check("ERROR" not in st, "move %s accepted (%s)" % (txt, st.get("ERROR")))
        R.play(board, mv)
        side = -side
        n += 1
        if n > 400:
            break
    results[st.get("result", "?")[:30]] = results.get(st.get("result", "?")[:30], 0) + 1
    get("/again", A)
    st, _ = get("/again", B)
    check(st["status"] == "play", "both /again: a new game")
get("/leave", A)
get("/leave", B)
print("ALL CHECKS PASSED,", GAMES, "games")
for k, v in sorted(results.items()):
    print("  %3d  %s" % (v, k))
