"""ckrules.py -- American checkers rules for the checkers table server: the same rules and the same square
numbering as LisaCheckers' CKR-RULES.TEXT (1-32, Black on 1-12 moving toward 32, Black moves first,
compulsory captures, a capturing piece keeps jumping, a man crowned ends its move).  18-Oct-2026."""

BLACK, WHITE = 1, -1


def row(sq):
    return (sq - 1) // 4


def col(sq):
    r = row(sq)
    return 2 * ((sq - 1) % 4) + (1 if r % 2 == 0 else 0)


def at(r, c):
    if 0 <= r <= 7 and 0 <= c <= 7 and (r + c) % 2 == 1:
        return r * 4 + c // 2 + 1
    return 0


# NB[sq][d]: d 0 = toward row 7, column - 1; 1 = row 7, column + 1; 2 = row 0, column - 1; 3 = row 0, column + 1
NB = [None] + [[at(row(s) + 1, col(s) - 1), at(row(s) + 1, col(s) + 1),
                at(row(s) - 1, col(s) - 1), at(row(s) - 1, col(s) + 1)] for s in range(1, 33)]


def start():
    b = [0] * 33
    for s in range(1, 33):
        b[s] = BLACK if s <= 12 else (WHITE if s >= 21 else 0)
    return b


def crowns(sq, side):
    return sq >= 29 if side == BLACK else sq <= 4


def moves(b, side):
    """All legal moves for side: lists of squares [from, landing, landing ...] and whether they capture."""
    caps = []

    def jumps(at_sq, piece, path, taken):
        dirs = (0, 1, 2, 3) if abs(piece) == 2 else ((0, 1) if piece > 0 else (2, 3))
        more = False
        for d in dirs:
            m = NB[at_sq][d]
            if m and m not in taken and b[m] * piece < 0:
                land = NB[m][d]
                if land and b[land] == 0:
                    more = True
                    if abs(piece) == 1 and crowns(land, side):
                        caps.append((path + [land], taken + [m]))
                    else:
                        jumps(land, piece, path + [land], taken + [m])
        if not more and taken:
            caps.append((path, taken))

    for s in range(1, 33):
        p = b[s]
        if p * side > 0:
            b[s] = 0
            jumps(s, p, [s], [])
            b[s] = p
    if caps:
        return [(path, taken) for path, taken in caps]
    out = []
    for s in range(1, 33):
        p = b[s]
        if p * side > 0:
            dirs = (0, 1, 2, 3) if abs(p) == 2 else ((0, 1) if side == BLACK else (2, 3))
            for d in dirs:
                t = NB[s][d]
                if t and b[t] == 0:
                    out.append(([s, t], []))
    return out


def play(b, mv):
    path, taken = mv
    p = b[path[0]]
    b[path[0]] = 0
    for t in taken:
        b[t] = 0
    end = path[-1]
    if p == BLACK and end >= 29:
        p = 2
    elif p == WHITE and end <= 4:
        p = -2
    b[end] = p


def text(mv):
    path, taken = mv
    return ("x" if taken else "-").join(str(s) for s in path)


def parse(b, side, s):
    """The legal move written s ("11-15", "22x15x8", or just "22x8" when only one route ends there)."""
    s = s.strip().lower()
    legal = moves(b, side)
    for mv in legal:
        if text(mv) == s:
            return mv
    nums = [int(x) for x in s.replace("x", "-").split("-") if x.isdigit()]
    if len(nums) >= 2:
        fits = [mv for mv in legal if mv[0][0] == nums[0] and mv[0][-1] == nums[-1]]
        if len(fits) == 1:
            return fits[0]
    return None


def board_text(b):
    return "".join({0: ".", 1: "b", 2: "B", -1: "w", -2: "W"}[b[s]] for s in range(1, 33))


if __name__ == "__main__":
    def perft(b, side, d):
        if d == 0:
            return 1
        n = 0
        for mv in moves(b, side):
            c = b[:]
            play(c, mv)
            n += perft(c, -side, d - 1)
        return n
    for d in range(1, 8):
        print("perft", d, perft(start(), BLACK, d))
