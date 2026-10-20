"""ckr_lisa_driver.py  19-Oct-2026: makes LisaCheckers (in LisaEm) play legal moves in a network game, for testing.
It reads the table's state from the checkers server as the Lisa's player, picks a legal move with ckrules (the most
captures first), and clicks its squares on the Lisa's screen through LisaEm's mouse file; then it waits until the
server has the move.  Board on screen: 8 x 8 squares of 34 pixels from (35, 58); your side is at the bottom, so as
black the board is turned round (CKR-MAIN ScrSq/SqScr).
    python ckr_lisa_driver.py <LisaEm run dir> <moves> [base-url] [table] [player]"""
import os, sys, time, urllib.request
import ckrules as R

RUN = sys.argv[1]
N = int(sys.argv[2])
BASE = sys.argv[3] if len(sys.argv) > 3 else "https://lisa-gw1.tailc2f141.ts.net/checkers"
TABLE = sys.argv[4] if len(sys.argv) > 4 else "test"
NAME = sys.argv[5] if len(sys.argv) > 5 else "lisa"


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


def screen_xy(sq, black):
    r, c = R.row(sq), R.col(sq)
    if black:
        r, c = 7 - r, 7 - c
    return 52 + 34 * c, 75 + 34 * r


def click(x, y):
    with open(os.path.join(RUN, "mouse.txt"), "a") as f:
        f.write("click %d %d\n" % (x, y))


made, t0 = 0, time.time()
LIMIT = float(os.environ.get("CKR_DRIVER_SECS", "3600"))   # 19-Oct: a whole game takes longer
while made < N and time.time() - t0 < LIMIT:
    st = get("/state")
    if st.get("status") == "play" and st.get("turn") == st.get("you"):
        black = st["you"] == "black"
        side = R.BLACK if black else R.WHITE
        legal = R.moves(R.board_of(st["board"]) if hasattr(R, "board_of") else board_of(st["board"]), side)
        if not legal:
            say("no legal move")
            break
        best = max(len(m[1]) for m in legal)
        mv = [m for m in legal if len(m[1]) == best][0]
        before = st.get("moves")
        # 19-Oct: the Lisa must have FETCHED this position first (LisaEm's link takes ~20 s): wait for its next
        # request to the server to finish (a CLOSE in pcfuji.log after now), and a little more for the drawing
        log = os.path.join(RUN, "pcfuji.log")
        c0 = open(log, encoding="latin-1").read().count("<- CLOSE")
        w = time.time()
        while open(log, encoding="latin-1").read().count("<- CLOSE") < c0 + 2 and time.time() - w < 120:
            time.sleep(1)
        time.sleep(5)
        say("Lisa plays", R.text(mv), "(%s)" % ("black" if black else "white"))
        for sq in mv[0]:
            x, y = screen_xy(sq, black)
            click(x, y)
            time.sleep(6)                     # LisaEm draws each click before the next
        w = time.time()
        tries = 1                             # 19-Oct night: click the move again if the server has not got it
        while get("/state").get("moves") == before and time.time() - w < 180:
            time.sleep(3)
            if tries < 3 and time.time() - w > 60 * tries:
                tries += 1
                say("no move at the server after %d s: clicking it again (try %d)" % (int(time.time() - w), tries))
                for sq in mv[0]:
                    x, y = screen_xy(sq, black)
                    click(x, y)
                    time.sleep(6)
        if get("/state").get("moves") == before:
            say("the server did not get the move in 3 minutes")
            break
        made += 1
        say("server has it; moves so far", get("/state").get("moves"))
    elif st.get("status") == "over":
        say("game over:", st.get("result"))
        break
    time.sleep(3)
say("driver done: %d moves made" % made)
