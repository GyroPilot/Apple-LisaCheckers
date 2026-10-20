"""ckr_opponent.py -- a patient scripted checkers player for testing LisaCheckers' network play: sits at a table
on the checkers server (default the public one, table 'test') as 'banana', waits, and on its turn plays a legal
move (a capture that takes the most, otherwise at random), checking the server's board against its own rules.
After a game it asks for another (colours swap) once and waits for the other player, up to GAMES games.  Ctrl-C leaves the table.
    python ckr_opponent.py [base-url] [table] [name] [games]                         18-Oct-2026"""
import random, sys, time, urllib.request
import ckrules as R

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://lisa-gw1.tailc2f141.ts.net/checkers"
TABLE = sys.argv[2] if len(sys.argv) > 2 else "test"
NAME = sys.argv[3] if len(sys.argv) > 3 else "banana"
GAMES = int(sys.argv[4]) if len(sys.argv) > 4 else 1


def get(path):
    with urllib.request.urlopen("%s%s?table=%s&player=%s" % (BASE, path, TABLE, NAME), timeout=20) as r:
        st = {}
        for line in r.read().decode().splitlines():
            k, _, v = line.partition(" ")
            st[k] = v
        return st


def say(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def board_of(text):
    b = [0] * 33
    for i, c in enumerate(text[:32]):
        b[i + 1] = {".": 0, "b": 1, "B": 2, "w": -1, "W": -2}[c]
    return b


games, last, over_seen = 0, None, False
try:
    while games < GAMES:
        st = get("/state")
        key = (st.get("status"), st.get("turn"), st.get("moves"), st.get("black"), st.get("white"))
        if key != last:
            say("status", st.get("status"), "| I am", st.get("you"), "| turn", st.get("turn"), "| black", st.get("black"),
                "white", st.get("white"), "| moves", st.get("moves"), "| last", st.get("last"), "|", st.get("prompt"))
            last = key
        if st.get("status") == "play" and st.get("turn") == st.get("you"):
            side = R.BLACK if st["you"] == "black" else R.WHITE
            b = board_of(st["board"])
            legal = R.moves(b, side)
            if sorted(st.get("legal", "").split()) != sorted(R.text(m) for m in legal):
                say("WARNING: the server's legal list differs from mine")
            if legal:
                best = max(len(m[1]) for m in legal)
                mv = random.choice([m for m in legal if len(m[1]) == best])
                time.sleep(2)
                r = get("/move/" + R.text(mv))
                say("played", R.text(mv), "->", r.get("ERROR") or "ok")
        elif st.get("status") == "over":
            if not over_seen:                  # 19-Oct: count each game ONCE (it counted every look and left at once)
                over_seen = True
                say("GAME OVER:", st.get("result"))
                games += 1
                if games < GAMES:
                    get("/again")              # then wait, however long, for the other player's /again
        else:
            over_seen = False
        time.sleep(1.5)
finally:
    get("/leave")
    say("left the table")
