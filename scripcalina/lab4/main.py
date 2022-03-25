from chomsky import *

def normalize_var(V):
    return V.replace(" ", "").replace("{", "").replace("}", "").split(",")

Vn = normalize_var("{S, A, B, C, D}")
Vt = normalize_var("{a, b, d}")
Prod = normalize_var("{S-> dB, S->AC, A->d, A->dS, A->aBdB, B->a, B->aA, B->AC, D->ab, C->bC, C->empty}")

# Vn = normalize_var("{S, B, H}")
# Vt = normalize_var("{0, 1}")
# Prod = normalize_var("{S->0S1, S->0SH, S->0, S->1B0, B->1H0, B->SH, H->1HB, H->SB}")

grammar = Chomsky(Vn, Vt, Prod)
grammar.normalize_grammar()


