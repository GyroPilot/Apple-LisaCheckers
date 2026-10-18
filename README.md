# LisaCheckers

American checkers (English draughts) for the Apple Lisa Office System: against the Lisa at four levels, or against
people on other Lisas and FujiNet machines through a small table server.

Tool number **419317** in the GyroPilot series. Lisa Pascal, Workshop 3.0, Lisa Office System 3.1.

## Status

**0.2 (REV B)** -- built and tested in LisaEm: play against the Lisa, and network play against a scripted player on the
public server (table list, moves both ways, reconnecting, resign, another game). Waiting for the Lisa 2/10, where
the levels' thinking times will be set (`releases/LISACHECKERS_0_2_TEST.dc42`).

## Playing

- Standard rules: men move diagonally forward; jumps are compulsory and a piece keeps jumping while it can; a man
  reaching the far row is crowned and its move ends; a side that cannot move loses; 40 moves each with only kings
  moving and nothing taken is a draw.
- Click a piece, then where it goes (for a jump, where it lands; when two jump routes end on the same square, each
  landing square). Or the keypad 4 6 8 2 and RETURN. Dots show where the picked piece can go (D); # shows the square
  numbers 1-32 that checkers books use; the panel writes moves as 11-15 or 22x15x8.
- N new game, U undo, S switch sides, Apple-1 to Apple-4 the level.
- **Network menu:** a list of tables on the checkers server; sit down with the table number. The server keeps the
  board and checks every move; colours swap each game. Offer or accept a draw, resign, another game, your name.

## The checkers server

`server/ckr_server.py` -- Python 3, standard library only; one plain GET per request, text replies a FujiNet machine
can read line by line (the format is in its header). Every player dials out to it, so nobody opens a router port.
Tim runs it on a Raspberry Pi behind Tailscale Funnel. `server/ckr_peer.py` checks a server by playing whole games;
`server/ckr_opponent.py` is a patient test opponent. The rules (`server/ckrules.py`, and `CKR-RULES.TEXT` on the Lisa)
match the published perft counts (7, 49, 302, 1469, 7361, 36768, 179740, 845931).

## Credits

Tim O'Connor (bmwcyclist on LisaList2, GyroPilot on GitHub), with Claude (Anthropic). Lisa Pascal with the Lisa
Workshop 3.0 for Lisa Office System 3.1; built in LisaEm and proven on a Lisa 2/10 and a LisaFPGA with a FutureVision
Research FujiNet for RS-232.
