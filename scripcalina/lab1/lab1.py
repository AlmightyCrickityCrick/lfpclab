import pandas as pd

#Create a program that given a grammar outputs it's FA.


#Introduce the grammar either by input or directly

Vn = "{S, B, C, D}"
Vt="{a, b, c}"
P="{S->aB, B->bS, B->aC, B->b, C->bD, D->a, D->bC, D->cS}"
# Vn = input("Introduce Vn: ")
# Vt = input("Introduce Vt: ")
# P = input("Introduce P: ")


#Modify each part of the grammar so only the relevant characters are kept within a list  
Vn = Vn.replace(" ", "").replace("{", "").replace("}", "").split(",")
Vt = Vt.replace(" ", "").replace("{", "").replace("}", "").split(",")
P = P.replace(" ", "").replace("{", "").replace("}", "").split(",")

#Add the End notations for production rules that point to terminal only characters
Vn.append("End")

#Create the finite automata adjency matrix
FA = [["-"]*(len(Vn)) for i in range(len(Vn))]


#Populate the Finite Automata Matrix
#Within all variants the production rules have either the form X->yZ or X->y (regular grammar)
#This version is adapted specifically to fit this context

#For each rule in production
for rule in P:
    #If the left symbol points to another nonterminal symbol
    if rule[len(rule)-1].isupper():
        #Places the terminal symbol in FA such that the row is the variable on the left and the column is the variable on the right  
        FA[Vn.index(rule[0])][Vn.index(rule[len(rule)-1])]=rule[3]
    else:
        #Places the terminal symbol in FA such that row is variable on left and column is the End notation
        FA[Vn.index(rule[0])][-1]=rule[3]

#Places for commodity of visualisation the FA into a Dataframe, 
FiniteAutomata=pd.DataFrame(FA, index=Vn, columns=Vn)
print(FiniteAutomata)

word = input("Introduce a word to verify if accepted by FA")

var = 0
print(FA[0].index("a"))

for i in range(len(word)):
    if word[i] not in Vt:
        print("Not accepted")
        break
    if word[i] not in FA[var]:
        print("Not accepted")
        break
    else:
        var = FA[var].index(word[i])

print("In FA")

