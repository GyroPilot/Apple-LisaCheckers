{$V+}
program CkTest;
uses UnitStd, UnitHz, Storage, QuickDraw, CkrRules;
var bdS : array [0..12] of CkBoard;
    lsS : array [0..12] of CkList;
    d, i, n, mvno, lvlB, lvlW, v : integer;
    mv : CkMove;
    s : Str255;
    side : integer;
    ws, bs, dr : integer;
    g : integer;

function Perft (ply, depth, side : integer) : longint;
var n, i : integer; t : longint;
begin
  if depth = 0 then begin Perft := 1; exit end;
  CkGen(bdS[ply], side, lsS[ply], n);
  t := 0;
  for i := 1 to n do begin
    bdS[ply+1] := bdS[ply];
    CkDo(bdS[ply+1], lsS[ply][i]);
    t := t + Perft(ply+1, depth-1, -side)
  end;
  Perft := t
end;

procedure Show;
var r, c, sq : integer;
begin
  for r := 0 to 7 do begin
    for c := 0 to 7 do begin
      sq := CkSq(r, c);
      if sq = 0 then write(' ') else
      case ckBd[sq] of 0: write('.'); 1: write('b'); 2: write('B'); -1: write('w'); -2: write('W'); end
    end;
    writeln
  end
end;

begin
  CkInit;
  bdS[0] := ckBd;
  for d := 1 to 8 do writeln('perft ', d, ' = ', Perft(0, d, ckBlack));
  { self play: level lvlB for black vs lvlW for white, a few games }
  ws := 0; bs := 0; dr := 0;
  for g := 1 to 6 do begin
    CkStart; ckSeed := g * 77;
    if odd(g) then begin lvlB := 6; lvlW := 2 end else begin lvlB := 2; lvlW := 6 end;
    mvno := 0;
    repeat
      if ckSide = ckBlack then n := CkThink(lvlB, 100000, mv) else n := CkThink(lvlW, 100000, mv);
      if n > 0 then begin
        if g = 1 then begin CkText(mv, s); write(s, ' ') end;
        CkDo(ckBd, mv); ckSide := -ckSide; mvno := mvno + 1
      end
    until (n = 0) or (mvno >= 200);
    if g = 1 then begin writeln; Show end;
    if n = 0 then begin
      if ckSide = ckBlack then begin ws := ws + 1; writeln('game ', g, ' (B',lvlB,' W',lvlW,'): White wins in ', mvno) end
      else begin bs := bs + 1; writeln('game ', g, ' (B',lvlB,' W',lvlW,'): Black wins in ', mvno) end
    end else begin dr := dr + 1; writeln('game ', g, ': 200 plies, no result') end
  end;
  CkStart; ckNodes := 0; n := CkThink(8, 10000000, mv); writeln('depth 8 from start nodes=', ckNodes)
end.
