from chomsky import *

def normalize_var(V):
    return V.replace(" ", "").replace("{", "").replace("}", "").split(",")

Vn = normalize_var("{S, A, B, C, D}")
Vt = normalize_var("{a, b, d}")
Prod = normalize_var("{S-> dB, S->AC, A->d,  A->dS, A-> aBdB, B->a, B->aA, B->C, D->C, B->AC, D->ab, C->bC, C->empty}")

print(Vn)
print(Vt)
print(Prod)

grammar = Chomsky(Vn, Vt, Prod)
grammar.normalize_grammar()