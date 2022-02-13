from dfa import DFA
from nfa import NFA

fa = NFA("{q0, q1, q2, q3}", "{a, b, c}", "d(q0, a)=q0, d(q0, a)=q1, d(q1, b)=q2, d(q2, c)=q3, d(q3, c)=q3, d(q2, a)=q2")
fa.to_dictionary()
print("----------------------------------------------------")
print("NFA is ", fa.dictFA)
fa.to_grammar()
print("----------------------------------------------------")
my_dfa = fa.to_dfa()
print("----------------------------------------------------")
print("DFA is ", my_dfa.dictFA)
print("----------------------------------------------------")

