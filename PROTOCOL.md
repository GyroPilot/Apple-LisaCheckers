# The LisaCheckers table server: protocol

One small server, plain HTTP, text replies. Any machine that can make a GET request and read lines can play:
a Lisa or an Apple II with a FujiNet, a modern computer, a script. Every player dials *out* to the server, so
nobody has to open a port at home.

A public server runs at **`https://lisa-gw1.tailc2f141.ts.net/checkers`** (Tim's Raspberry Pi). The server is
`server/ckr_server.py` in this repository: Python 3, standard library only, about 200 lines. Run your own with
`python3 ckr_server.py 8090`.

## Requests

Every request is a GET. All of them except `/tables` take two query parameters:

| parameter | meaning |
|---|---|
| `table=<id>` | the table, from the `/tables` list (`c1`, `c2`, `c3`) |
| `player=<name>` | your name: letters and digits only, lower case, 8 characters at most (anything else is dropped) |

| request | what it does |
|---|---|
| `/tables` | lists the tables, one a line |
| `/state` | sits you at the table if a seat is free (black first, then white) and returns the state. Call it again to poll. |
| `/move/<move>` | your move, e.g. `/move/11-15` or `/move/22x15x8`; the state comes back |
| `/resign` | you resign; the other player wins |
| `/draw` | offer a draw; when the other player sends `/draw` too, the game is a draw |
| `/leave` | stand up (if a game is on, you lose it). Replies `BYE`. |
| `/again` | after a game: ready for another. When both players have sent it, the colours swap and a new game starts. |

Examples:

    GET /tables
    GET /state?table=c1&player=tim
    GET /move/11-15?table=c1&player=tim

## The table list

One line per table, fields separated by `|`:

    T|c1|Checkers 1|0/2|lobby
    T|c2|Checkers 2|1/2|lobby
    T|c3|Checkers 3|2/2|play

`<id>|<name>|<seated>/2|<lobby|play|over>`.

## The state

Every request except `/tables` and `/leave` answers with the state: one fact per line, `key value`, ASCII, lines
ending in `\n`. The first line is `CK1` (the format version). A client can read it line by line and ignore keys
it does not know.

    CK1
    status play
    you black
    turn white
    black tim
    white banana
    board bbbbbbbbbbb.b.......wwwwwwwwwwww
    last 11-15
    moves 1
    draw -
    legal 21-17 22-17 22-18 23-18 23-19 24-19 24-20
    result -
    prompt Waiting for banana

| key | values |
|---|---|
| `status` | `lobby` (waiting for two players), `play`, `over` |
| `you` | `black`, `white`, or `watch` (both seats were taken: you see the game but cannot move) |
| `turn` | `black`, `white`, or `-` when no game is on |
| `black`, `white` | the player in that seat, or `-` |
| `board` | 32 characters, squares 1 to 32 in order: `.` empty, `b` black man, `B` black king, `w` white man, `W` white king |
| `last` | the last move played, or `-` |
| `moves` | how many moves have been played in this game |
| `draw` | who has offered a draw: `black`, `white`, or `-` |
| `legal` | the moves of the player to move, space separated (empty when no game is on). A client need not know the rules: it can offer exactly these. |
| `result` | how the game ended, or `-` |
| `prompt` | one line of plain words for the screen, e.g. `Your move: you must jump` |

### Errors

A refused move answers with `ERROR <why>` as the **first** line, followed by the state as usual:

    ERROR 11-16 is not a legal move
    CK1
    status play
    ...

A request without a valid table and player answers with just `ERROR give a table and a player name`. An unknown
path answers `ERROR unknown request` with HTTP status 404. Everything else is HTTP 200.

## The board and the moves

The standard checkers numbering: the 32 dark squares are numbered 1 to 32 from Black's side, four per row.
Black's men start on 1 to 12 and move toward 32; White's start on 21 to 32 and move toward 1.

    Black's back row:    1   2   3   4
                       5   6   7   8
                         9  10  11  12
                      13  14  15  16
                        17  18  19  20
                      21  22  23  24
                        25  26  27  28
    White's back row:  29  30  31  32

Square *n* is in row `(n-1) div 4` (row 0 = Black's back row). In even rows the dark squares are columns
1, 3, 5, 7; in odd rows, columns 0, 2, 4, 6.

A move is written `from-to` for a plain move and `from x over x ... x to` for a jump, listing every square the
piece lands on: `11-15`, `22x15`, `22x15x8`. Send it exactly as it appears in `legal`.

## The rules the server enforces

American checkers (English draughts): men move one square diagonally forward; kings move one square in any
diagonal direction; captures are compulsory and a capturing piece keeps jumping while it can (the player chooses
among capture sequences, not necessarily the longest); a man reaching the far row is crowned and its move ends
there; a player with no legal move loses. Forty moves by each side with only kings moving and nothing taken is
a draw. The rules are `server/ckrules.py` (checked against the published perft counts) and the same in Lisa
Pascal in `sources/CKR-RULES.TEXT`.

## Timing and seats

- Poll `/state` every few seconds while waiting (LisaCheckers polls every 3 s, and every 15 s during its own
  move).
- A seat whose player has not sent any request for **300 seconds** is given up; if a game was on, that player
  loses it. The idle time is `IDLE` in the server.
- When both seats are empty and no game is on, the table resets to the lobby.
- There is no authentication: a name is just a name. Don't take a seat that shows someone else's name.

## Writing a client

The whole game loop is: `/state` until `status play` and `turn` is your colour, pick one of `legal`, send
`/move/<it>`, repeat. `server/ckr_opponent.py` is a 60-line Python client that does exactly that (it plays a
capture when it can, otherwise a random legal move); `server/ckr_peer.py` plays whole games to test a server.

A client that wants to show the board draws the 32 characters of `board`; one that wants to check moves itself
can port `ckrules.py`.

## Changes

- 18 Oct 2026, format `CK1`: first version. The format version line will change if the state ever becomes
  incompatible; new keys may be added without changing it.
