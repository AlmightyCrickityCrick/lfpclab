from spp import *

def normalize_var(V):
    return V.replace(" ", "").replace("{", "").replace("}", "").split(",")

Vn = normalize_var("{S, A, C, D}")
Vt = normalize_var("{b, e, f, g}")
Prod = normalize_var("{S->Ag, A->AbD, A->C, C->e, C->CfD, D->e}")


# Vn = normalize_var("{S, A, B, D, T}")
# Vt = normalize_var("{a ,b ,c , d }")
# Prod = normalize_var("{S->dB, B->a, B->aA, A->D, A->TcA, D->bB, T->D}")

# Vn = normalize_var("{S, B, D, A}")
# Vt = normalize_var("{c,g,d, f }")
# Prod = normalize_var("{S->BfD, B->Bc, B->D, D->Ag, D->A, A->d, A->c}")

parser = Simple_PP(Vn, Vt, Prod)

parser.create_parser()

parser.parse("efefebeg")

# parser.parse("dabacba")

#parser.parse("dgcfdg")