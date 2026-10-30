# LisaCheckers

American checkers (English draughts) for the Apple Lisa Office System: against the Lisa at four levels, or against
people on other Lisas and FujiNet machines through a small table server.

Tool number **419317** in the GyroPilot series. Lisa Pascal, Workshop 3.0, Lisa Office System 3.1.

## Status

**1.2 (REV O) -- released 30 October 2026.** Plays through an **ESPFuji** ESProFile as well as an RS-232 FujiNet:
when the tool sits on an ESProFile volume that runs ESPFuji (https://github.com/GyroPilot/ESPFuji) it finds the
mailbox by itself and needs no serial adapter. The first complete game through an ESProFile was played on a Lisa
2/10 on 29 October (34 moves, against the table server). C sets the Lisa's clock from the network when the clock is
unset (a Lisa that lost power reads 1980); the polls no longer depend on the clock. Failure lines say why in words.
Release floppy: `releases/LISACHECKERS_1_2.dc42`. The clock offer and the wording were checked in LisaEm after the
2/10 game; the mailbox code is the one that played it.

**1.0 (REV G) -- released 21 October 2026.**  The 0.2 REV F program with the version 1.0: tested on a Lisa 2/10
(against the Lisa, and a whole network game through the table server: 41 moves, the game-over alert, Save & Put
Away), and overnight in LisaEm as 1.0 (a 48-move network game, opened from its floppy).  Release floppy:
`releases/LISACHECKERS_1_0.dc42`.

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

**The protocol is documented in [PROTOCOL.md](PROTOCOL.md)**: plain GETs, text replies, so anyone can write a client in
any language.

`server/ckr_server.py` -- Python 3, standard library only; one plain GET per request, text replies a FujiNet machine
can read line by line (the format is in its header). Every player dials out to it, so nobody opens a router port.
Tim runs it on a Raspberry Pi behind Tailscale Funnel. `server/ckr_peer.py` checks a server by playing whole games;
`server/ckr_opponent.py` is a patient test opponent. The rules (`server/ckrules.py`, and `CKR-RULES.TEXT` on the Lisa)
match the published perft counts (7, 49, 302, 1469, 7361, 36768, 179740, 845931).

## Credits

Tim O'Connor (bmwcyclist on LisaList2, GyroPilot on GitHub), with Claude (Anthropic). Lisa Pascal with the Lisa
Workshop 3.0 for Lisa Office System 3.1; built in LisaEm and proven on a Lisa 2/10 and a LisaFPGA with a FutureVision
Research FujiNet for RS-232.

## The speed (phase 2, 23 October 2026)

The tool sets the FujiNet's speed too: Network > Use 19200 baud posts the new speed to the adapter's own web page through the
FujiNet's network device, presses its Reset button and opens the port again at the new speed (about 20 seconds;
the adapter's WiFi must be up). At its first port open of each launch the tool probes for the speed (the saved one,
then the other of 9600/19200) and keeps what answers, so after any one tool changes the adapter the others follow.
The choice is kept in CKRNAME.DATA beside the tool.
