{$V+}
program CkDepth;
uses UnitStd, UnitHz, Storage, QuickDraw, CkrRules;
const nl = 4;
var lv, n, mvno, g, side : integer; mv : CkMove;
    dep : array [1..nl] of integer; bud : array [1..nl] of longint;
    tot, mx, dsum : array [1..nl] of longint; cnt : array [1..nl] of longint;
    wins : array [1..nl] of integer;
begin
  CkInit;
  dep[1] := 2; bud[1] := 100000; dep[2] := 4; bud[2] := 1500; dep[3] := 6; bud[3] := 4000; dep[4] := 10; bud[4] := 10000;
  for lv := 1 to nl do begin tot[lv] := 0; mx[lv] := 0; cnt[lv] := 0; dsum[lv] := 0; wins[lv] := 0 end;
  { each level plays the next level up, both colours }
  for lv := 1 to nl - 1 do
    for g := 1 to 4 do begin
      CkStart; ckSeed := g * 31 + lv; mvno := 0;
      repeat
        if (ckSide = ckBlack) = odd(g) then begin
          n := CkThink(dep[lv], bud[lv], mv); tot[lv] := tot[lv] + ckNodes; cnt[lv] := cnt[lv] + 1; dsum[lv] := dsum[lv] + ckDone; if ckNodes > mx[lv] then mx[lv] := ckNodes end
        else begin
          n := CkThink(dep[lv+1], bud[lv+1], mv); tot[lv+1] := tot[lv+1] + ckNodes; cnt[lv+1] := cnt[lv+1] + 1; dsum[lv+1] := dsum[lv+1] + ckDone; if ckNodes > mx[lv+1] then mx[lv+1] := ckNodes end;
        if n > 0 then begin CkDo(ckBd, mv); ckSide := -ckSide; mvno := mvno + 1 end
      until (n = 0) or (mvno >= 160);
      if n = 0 then begin
        if (ckSide = ckBlack) = odd(g) then wins[lv+1] := wins[lv+1] + 1 else wins[lv] := wins[lv] + 1
      end
    end;
  for lv := 1 to nl do writeln('level ', lv, ': average ', tot[lv] div cnt[lv], ' positions, most ', mx[lv], ', average depth x10 ', dsum[lv]*10 div cnt[lv], ', wins ', wins[lv]);
end.
