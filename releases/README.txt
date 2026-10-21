LisaCheckers 1.0 for the Apple Lisa Office System       October 2026 (release build REV G)
American checkers (English draughts).  Tool 419317.

PLAY
  Against the Lisa at four levels (Apple-1 to Apple-4), or against people on other Lisas and
  FujiNet machines through a small table server.

  Click a piece, then where it goes (for a jump, where it lands).  The keypad 4 6 8 2 and RETURN
  work too.  Jumps are compulsory and a piece keeps jumping while it can; a man reaching the far row
  is crowned; a side that cannot move loses.

    N  new game          U  undo            S  switch sides
    D  dots (where the picked piece can go)  #  the square numbers 1-32
    H  help

NETWORK
  Needs an RS-232 FujiNet on Serial B.  Network menu > Play on the Network (or T) lists the
  tables on the checkers server; type a table's number to sit down.  The server keeps the board and
  checks every move; the colours swap each game.  Offer or accept a draw, resign, or ask for another
  game from the Network menu.  At the end an alert says who won.
  The server's protocol is public (PROTOCOL.md on GitHub): any FujiNet machine can join in.

SOURCE
  Lisa Pascal, Workshop 3.0.  github.com/GyroPilot/Apple-LisaCheckers  (the table server is in
  server/: Python 3, standard library only).
  Tim O'Connor (bmwcyclist), with Claude.  Tested on a Lisa 2/10, October 2026: against the Lisa,
  and a whole network game through the server.

WHAT'S IN THIS RELEASE
  LISACHECKERS_1_0.dc42          the release floppy
  LisaCheckers_1.0_source.zip    Lisa Pascal sources, exec files, and the server
