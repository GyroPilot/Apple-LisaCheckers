# LisaCheckers changelog

## 1.2 REV K-O -- 28-30 Oct 2026 -- RELEASE (REV O = REV N with the version 1.2)
- The ESProFile mailbox as a third back end beside the RS-232 FujiNet and LisaNet: FnBus finds MAILBOX.DATA on the
  tool's own volume (an ESPFuji drive) and uses it; otherwise Serial B as before. The first complete game through an
  ESProFile: Lisa 2/10, 29 Oct 2026, 34 moves against the table server. (REV K-L)
- A Lisa whose clock is unset (12:00 am 01/01/80 after a power loss) stalled the network polls, which were timed by
  GET_TIME; polls are nap-counted now. C offers to set the Lisa's clock from the network (opt-in: never unasked,
  after a LisaFPGA report that SetDateTime does not take there). TwcUnit (the twin-year clock) joins the sources
  as CKR-TWUNIT.TEXT. (REV M)
- Failure lines say why in words: "no mailbox on -#13- (ec 948): put it beside ESPFuji" / "mailbox did not answer:
  ESPFuji?"; COPY past the end of a short string returns '' on the Lisa, so truncations are guarded. (REV N)
## 1.1 REV H / REV I -- 22-23 Oct 2026 -- RELEASE (staged)
- The Network menu's Use 9600 / Use 19200 baud sets the FujiNet too (web page over N:, reset, port again); the
  first port open of each launch probes for the speed (FnFind) and keeps what answers. FnBus at LisaFuji's REV S
  level. The one-line result fits the panel. REV I = REV H with the version shown as 1.1. LisaEm-tested 22 Oct.
## 1.0 REV G -- 21 Oct 2026 -- RELEASE
- Version 1.0 (About box 21 October 2026); the program is 0.2 REV F.  A 48-move network game in LisaEm against
  the Pi's server; opens from its floppy.  The server protocol is documented in PROTOCOL.md.
## 0.2 REV F -- 20 Oct 2026 -- RELEASE 0.2
- After a move only the squares that changed are redrawn (no whole-board wipe).
- Tested on a Lisa 2/10: against the Lisa (level 2), and a whole network game through the Pi's table
  server, with the game-over alert and Save & Put Away.
## 0.2 REV E -- 20 Oct 2026
- Network games: the window is repainted only when something changed (it flashed every few seconds on
  the 2/10 while waiting); a 'Game over -- you win!' / lose / draw alert at the end; a look at the server
  that fails part-way no longer leaves an old board on the screen.  Two whole network games in LisaEm.
- The release floppy opens on the Lisa (the previous one was made on the Reversi floppy).
## 0.2 REV D -- 19 Oct 2026
- After a failed network reply to a move the game no longer freezes: it looks at the server again at once.
  Six network moves in LisaEm against the Pi's server, captures included.
## 0.2 REV C -- 18 Oct 2026
- Network reads of 128 bytes, not 256 (in LisaEm a 256-byte read took 9-12 s and could time out).
## 0.2 REV B -- 18 Oct 2026 -- built, tested in LisaEm
- Network play through the checkers table server (Network menu). Tested against a scripted player on the public
  server: table list, moves both ways, reconnecting after a crash, resign, another game with colours swapped.
## 0.1 REV A -- 17 Oct 2026
- You against the Lisa: the rules checked by perft, four levels, undo, switch sides, dots, square numbers.
