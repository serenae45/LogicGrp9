CONJECTUREPANEL Theorems
PROOF "¬¬P ⊢ P"
INFER ¬¬P 
     ⊢ P 
FORMULAE
0 ⊥,
1 ¬¬P,
2 ¬P,
3 P 
IS
SEQ ("contra (classical)"[A\3]) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL MostEpicSequents
PROOF "R(x,z), (R(x,z)∧R(y,z))→E(x,y) ⊢ ¬E(x,y)→¬R(y,z)"
INFER R(x,z),
     (R(x,z)∧R(y,z))→E(x,y)
     ⊢ ¬E(x,y)→¬R(y,z)
FORMULAE
0 ⊥,
1 ¬E(x,y),
2 E(x,y),
3 R(x,z)∧R(y,z),
4 R(x,z)∧R(y,z)→E(x,y),
5 R(y,z),
6 R(x,z),
7 ¬R(y,z),
8 (R(x,z)∧R(y,z))→E(x,y),
9 ¬¬R(y,z)
IS
SEQ ("→ intro"[A,B\1,7]) ("contra (classical)"[A\7]) (cut[B,C\5,0]) ("¬¬P ⊢ P"[P\5]) (cut[B,C\3,0]) ("∧ intro"[A,B\6,5]) (hyp[A\6]) (hyp[A\5]) (cut[B,C\2,0]) ("→ elim"[A,B\3,2]) (hyp[A\4]) (hyp[A\3]) (cut[B,C\2,0]) (hyp[A\2]) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Theorems
PROOF "P→Q ⊢ ¬Q→¬P"
INFER P→Q 
     ⊢ ¬Q→¬P 
FORMULAE
0 ⊥,
1 ¬Q,
2 Q,
3 P,
4 P→Q,
5 ¬P 
IS
SEQ ("→ intro"[A,B\1,5]) ("¬ intro"[A\3]) (cut[B,C\2,0]) ("→ elim"[A,B\3,2]) (hyp[A\4]) (hyp[A\3]) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL MostEpicSequents
PROOF "∀x.∀y.∀j.(S(x,z,j)→¬S(y,z,j)), ∃x.∃j.S(x,z,j) ⊢ ∀y.∃j.¬S(y,z,j)"
INFER ∀x.∀y.∀j.(S(x,z,j)→¬S(y,z,j)),
     ∃x.∃j.S(x,z,j)
     ⊢ ∀y.∃j.¬S(y,z,j)
FORMULAE
0 actual i2,
1 ¬S(i1,z,i2),
2 ¬S(i1,z,j),
3 i2,
4 j,
5 ∃j.¬S(i1,z,j),
6 S(i,z,i2),
7 S(i,z,i2)→¬S(i1,z,i2),
8 ∀j.(S(i,z,j)→¬S(i1,z,j)),
9 S(i,z,j)→¬S(i1,z,j),
10 ∃j.S(i,z,j),
11 S(i,z,j),
12 actual i1,
13 ∀y.∀j.(S(i,z,j)→¬S(y,z,j)),
14 ∀j.(S(i,z,j)→¬S(y,z,j)),
15 i1,
16 y,
17 ∃j.¬S(y,z,j),
18 actual i,
19 ∀x.∀y.∀j.(S(x,z,j)→¬S(y,z,j)),
20 ∀y.∀j.(S(x,z,j)→¬S(y,z,j)),
21 i,
22 x,
23 ∀y.∃j.¬S(y,z,j),
24 ∃x.∃j.S(x,z,j),
25 ∃j.S(x,z,j)
IS
SEQ ("∃ elim"[i,C,P,x\21,23,25,22]) (hyp[A\24]) (cut[B,C\13,23]) ("∀ elim"[P,i,x\20,21,22]) (hyp[A\19]) (hyp[A\18]) ("∀ intro"[i,P,x\15,17,16]) (cut[B,C\8,5]) ("∀ elim"[P,i,x\14,15,16]) (hyp[A\13]) (hyp[A\12]) ("∃ elim"[i,C,P,x\3,5,11,4]) (hyp[A\10]) (cut[B,C\7,5]) ("∀ elim"[P,i,x\9,3,4]) (hyp[A\8]) (hyp[A\0]) (cut[B,C\1,5]) ("→ elim"[A,B\6,1]) (hyp[A\7]) (hyp[A\6]) (cut[B,C\1,5]) (hyp[A\1]) ("∃ intro"[P,i,x\2,3,4]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Theorems
PROOF "P→Q, ¬Q ⊢ ¬P"
INFER P→Q,
     ¬Q 
     ⊢ ¬P 
FORMULAE
0 ⊥,
1 ¬Q,
2 Q,
3 P,
4 P→Q 
IS
SEQ ("¬ intro"[A\3]) (cut[B,C\2,0]) ("→ elim"[A,B\3,2]) (hyp[A\4]) (hyp[A\3]) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL MostEpicSequents
PROOF "(¬C∨∃x.∃y.¬Q(x,y))∨R ⊢ (C∧∀x.∀y.Q(x,y))→R"
INFER (¬C∨∃x.∃y.¬Q(x,y))∨R 
     ⊢ (C∧∀x.∀y.Q(x,y))→R 
FORMULAE
0 R,
1 ⊥,
2 ¬Q(i,i1),
3 Q(i,i1),
4 actual i1,
5 ∀y.Q(i,y),
6 Q(i,y),
7 i1,
8 y,
9 ∃y.¬Q(i,y),
10 ¬Q(i,y),
11 actual i,
12 ∀x.∀y.Q(x,y),
13 ∀y.Q(x,y),
14 i,
15 x,
16 ∃x.∃y.¬Q(x,y),
17 ∃y.¬Q(x,y),
18 ¬C,
19 C,
20 ¬C∨∃x.∃y.¬Q(x,y),
21 ¬C∨∃x.∃y.¬Q(x,y)∨R,
22 C∧∀x.∀y.Q(x,y),
23 (¬C∨∃x.∃y.¬Q(x,y))∨R 
IS
SEQ ("→ intro"[A,B\22,0]) (cut[B,C\19,0]) (LAYOUT "∧ elim" (0) ("∧ elim(L)"[A,B\19,12]) (hyp[A\22])) (cut[B,C\12,0]) (LAYOUT "∧ elim" (0) ("∧ elim(R)"[A,B\19,12]) (hyp[A\22])) ("∨ elim"[A,B,C\20,0,0]) (hyp[A\21]) ("∨ elim"[A,B,C\18,16,0]) (hyp[A\20]) (cut[B,C\1,0]) ("¬ elim"[B\19]) (hyp[A\19]) (hyp[A\18]) ("contra (constructive)"[B\0]) (hyp[A\1]) ("∃ elim"[i,C,P,x\14,0,17,15]) (hyp[A\16]) (cut[B,C\5,0]) ("∀ elim"[P,i,x\13,14,15]) (hyp[A\12]) (hyp[A\11]) ("∃ elim"[i,C,P,x\7,0,10,8]) (hyp[A\9]) (cut[B,C\3,0]) ("∀ elim"[P,i,x\6,7,8]) (hyp[A\5]) (hyp[A\4]) (cut[B,C\1,0]) ("¬ elim"[B\3]) (hyp[A\3]) (hyp[A\2]) ("contra (constructive)"[B\0]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Theorems
PROOF "P∨¬P"
INFER P∨¬P 
FORMULAE
0 ⊥,
1 ¬(P∨¬P),
2 P∨¬P,
3 P,
4 ¬P,
5 ¬(P∨¬P)
IS
SEQ ("contra (classical)"[A\2]) (cut[B,C\3,0]) ("contra (classical)"[A\3]) (cut[B,C\2,0]) (LAYOUT "∨ intro" (0) ("∨ intro(R)"[B,A\3,4]) (hyp[A\4])) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0]) (cut[B,C\2,0]) (LAYOUT "∨ intro" (0) ("∨ intro(L)"[B,A\4,3]) (hyp[A\3])) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
CONJECTUREPANEL Theorems
PROOF "P ⊢ ¬¬P"
INFER P 
     ⊢ ¬¬P 
FORMULAE
0 ⊥,
1 ¬P,
2 P 
IS
SEQ ("¬ intro"[A\1]) (cut[B,C\0,0]) ("¬ elim"[B\2]) (hyp[A\2]) (hyp[A\1]) (hyp[A\0])
END
