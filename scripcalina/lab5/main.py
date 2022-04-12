from spp import *

def normalize_var(V):
    return V.replace(" ", "").replace("{", "").replace("}", "").split(",")

Vn = normalize_var("{S, A, C, D}")
Vt = normalize_var("{b, e, f, g}")
Prod = normalize_var("{S->Ag, A->AbD, A->C, C->e, C->CfD, D->e}")

parser = Simple_PP(Vn, Vt, Prod)

parser.create_parser()