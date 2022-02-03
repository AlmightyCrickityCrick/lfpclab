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



#Verifying if a word belongs to the alphabet

word = input("Introduce a word to verify if accepted by FA")

#word = "abab"

#Flag if a vital condition is not respected
flag = 0
#Var that keeps track which is the current neterminal symbol. Default value = strating Vn (which is S, index 0)
var = 0

#Verification process for each letter of the word
for i in range(len(word)):
    #If the word contains letter not part of terminal symbols the word is not in language
    if word[i] not in Vt:
        print("Not accepted")
        flag = 1
        break
    #If the last letter is not in the terminal column of current row, the word cant exist in the language
    if i == len(word)-1 and not FA[var][-1] == word[i]:
        print("Not accepted")
        flag = 1
        break
    else:
        #Find the next neterminal variable based on the connecting letter 
        if word[i] in FA[var][:-1]:
            var = FA[var].index(word[i])

if flag ==0:
    print("Accepted")