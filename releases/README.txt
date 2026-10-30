LisaCheckers 1.2 for the Apple Lisa Office System       30 October 2026 (release build REV O)
American checkers (English draughts).  Tool 419317.

New in this build: plays through an ESPFuji ESProFile (https://github.com/GyroPilot/ESPFuji) as well as an RS-232
FujiNet: put the tool on the ESProFile's volume and it finds the mailbox by itself, no serial adapter.  C sets the
Lisa's clock from the network when it is unset; the network polls no longer depend on the clock; failure lines say why.
Floppy image LISACHECKERS_1_2.dc42; the source zip has the Lisa Pascal sources and the exec files.
Needs an ESPFuji ESProFile, an RS-232 FujiNet (FutureVision Research) on Serial B, or a LisaNet.  Built with the Lisa
Workshop 3.0 in LisaEm; the mailbox game tested on a Lisa 2/10 (29 Oct 2026), the clock offer in LisaEm.
