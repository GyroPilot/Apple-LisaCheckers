# LisaCheckers changelog

## 0.2 REV F -- 20 Oct 2026 -- RELEASE
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
