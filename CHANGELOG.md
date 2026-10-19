# LisaCheckers changelog

## 0.2 REV C -- 18 Oct 2026
- Network reads of 128 bytes, not 256 (in LisaEm a 256-byte read took 9-12 s and could time out).
## 0.2 REV B -- 18 Oct 2026 -- built, tested in LisaEm
- Network play through the checkers table server (Network menu). Tested against a scripted player on the public
  server: table list, moves both ways, reconnecting after a crash, resign, another game with colours swapped.
## 0.1 REV A -- 17 Oct 2026
- You against the Lisa: the rules checked by perft, four levels, undo, switch sides, dots, square numbers.
