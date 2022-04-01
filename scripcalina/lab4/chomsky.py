from graibach import *

class Chomsky:
    Vn = []
    Vt = []
    P = {}
    
    def __init__(self, Vn, Vt, P):
        self.Vn = Vn
        self.Vt = Vt
        self.P = self.create_P(P)

    #Creates the dictionary representation of original grammar
    def create_P(self, P):
        P1 = {}

        for key in self.Vn:
            P1[key] = []
        
        for el in P:
            P1[el[0]].append(el[(el.index("->") + 2):])
        
        return P1
    
    #Main function responsible for the transition to normal form
    def normalize_grammar(self):
        print("Original grammar\nVn =", self.Vn, "\nVt=", self.Vt, "\nP=", self.P)
        P1 = self.eliminate_empty(self.P)
        print("---------------------------\n","Empty-elimination \n", P1)
        P2 = self.eliminate_renaming(P1)
        print("Unit production elimination\n", P2)
        P3, Vn, Vt = self.eliminate_inaccessible(P2)
        print("Inaccesible elimination \n",P3)
        P4, Vn = self.eliminate_non_productive(P3, Vn, Vt)
        print("Non-Productive elimination \n", P4)
        P5, Vn = self.bring_to_chomsky(P4, Vn, Vt)
        print("Chomsky normal form transformation\n", P5)

        print("-------------------------------")
        self.P = P5
        self.Vn = Vn
        self.Vt = Vt
        print("Chomsky normal form grammar\n Vn=", self.Vn, "\nVt=", self.Vt, "\nP=", self.P)

    
    #First Step towards Chomsky Normal form
    def eliminate_empty(self, P):
        P1 = P
        empty_set = ["empty"]

        #Finds empty transitions and unit productions that lead to them
        self.find_empty(P1, empty_set)

        #Adds transition variants without the Vn that lead to empty
        for k, v in P1.items():
            for trans in v:
                if len(trans) >= 2: self.substitute_empty(empty_set[1:], k, trans, P1)

        return P1

    #Finds empty transitions and unit productions that lead to them
    def find_empty(self, P, empty_set):
        em = 0
        #Finds Vn that might lead to empty
        while em < len(empty_set):
            for k, v in P.items():
                 #Marks the renamings that lead to Vn that leads to empty 
                if (empty_set[em] in v) and (k not in empty_set):
                    empty_set.append(k)
                #Marks the Vn that leads to empty and deletes the empty transition
                if "empty" in v:
                    P[k].remove(empty_set[em])
               
            em += 1
    
    #Adds transition variants without the Vn that lead to empty
    def substitute_empty(self, empty_set, k, trans, P):
        for i in range(len(trans)):
            if trans[i] in empty_set:
                if i == (len(trans) -1): tmp = trans[:-1] 
                else: tmp = trans[:i] + trans[(i + 1):]
                if tmp not in P[k]: P[k].append(tmp)
    
    #Second Step for Chomsky Normal Form
    def eliminate_renaming(self, P):
        P2 = P.copy()
        #Iterates through Production dictionary and each transition to find transitions that lead to single Vn
        for k, v in P2.items():
            P2[k].extend(self.check_unit_transition(P2, k, v))
            P2[k] = list(set(P2[k]))
        
        return P2

    #Recursive function that checks for unit transitions.
    def check_unit_transition(self, P2, k, v):
        unit = []
        transitions = []
        
        #Verifies is a transition is in Vn (meaning has a single Vn within it)
        for trans in v:
            if trans in self.Vn: 
                unit.append(trans)
                P2[k].remove(trans)
        
        #Verifies if the unit production does not contain another unit production within it
        for u in unit:
            transitions.extend(P2[u])
            transitions.extend(self.check_unit_transition(P2, u, P2[u]))
        
        return transitions
        
    #Third Step for Chomsky Normal Form
    def eliminate_inaccessible(self, P):
        P3 = {}
        #The starting point is by default accesible
        access_vn = ["S"]
        access_tn = []

        #Iterates through each accesible variable and appends each Vn, Vt and Production it encounters
        i = 0
        while i < len(access_vn):
            tmp = str(P[access_vn[i]])
            P3[access_vn[i]] = P[access_vn[i]]
            for v in self.Vn:
                if v in tmp and v not in access_vn:
                    access_vn.append(v)
            for v in self.Vt:
                if v in tmp and v not in access_tn:
                    access_tn.append(v)
            i+=1

        return P3, access_vn, access_tn

    #Fourth Step for Chomsky Normal form
    def eliminate_non_productive(self, P, Vn, Vt):
        P4 = P.copy()
        productive = []
        non_prod = Vn.copy()
        no_change_flag = False

        #Checks for productive until symbols until no further additions can be made
        while not no_change_flag:
            tmp = productive.copy()
            for v in non_prod:
                tmp.extend(self.find_productive(P4, Vt, non_prod, v)) 
            
            if len(tmp) == len(productive) or len(tmp) == len(Vn): 
                no_change_flag = True
            productive = tmp

        #If al are productive, return as it is            
        if len(productive) == len(Vn) : return P4, Vn

        #If there are non-productive variables, delete their mentions
        for np in non_prod:
            self.delete_non_productive(P4, np)
        
        return P4, productive

    #Check wherever a Vn is productive 
    def find_productive(self, P, Vt, non_prod, v):
        #Filters and creates a list of all terminals for a certain Vn in production
        direct_prod = list(filter(lambda x: x in Vt, P[v]))
        if len(direct_prod) > 0:
            non_prod.remove(v)
            return [v]
        else:
            for trans in P[v]:
                #Check each transition of the Vn to look for transition to terminal + productive Vn
                indirect_prod = list(filter(lambda x: x in non_prod, trans))
                if len(indirect_prod) == 0:
                    non_prod.remove(v)
                    return [v]
        return []

    #Gets rid of all productions that contain non-productive symbols
    def delete_non_productive(self, P, np):
        P.pop(np)
        for k, v in P.items():
            for trans in v:
                if np in trans: P[k].remove(trans)

    #Last Step for Chomsky Normal Form
    def bring_to_chomsky(self, P, Vn, Vt):
        P5 = {}
        self.aux = {}
        self.y = 0

        #Creates X for the terminal symbols
        self.create_X(Vt)
        
        #Converts to Chomsky normal form
        for k, v in P.items():
            P5[k] = []
            for trans in v:
                #If transition to single terminal variable - appends it as it is
                if trans in Vt:
                    P5[k].append(trans)
                #If more than 1 terminal variable, prepares the transition
                else:
                    tmp = self.prepare_transition(trans, Vt, Vn)
                    #If more than 2 variables, converts recursively from end to begin
                    if len(tmp) > 4: tmp = tmp[:2] + self.convert_transition(tmp[2:])
                    #Gets rid of spare spaces if possible and appends to grammar
                    try: P5[k].append(tmp.replace(" ", ""))
                    except: P5[k].append(tmp)

        #Appends the auxiliary transitions to grammar from the aux dictionary           
        for k, v in self.aux.items():
            lst = []
            try: lst.append(k.replace(" ", ""))
            except: lst.append(k)
            P5[v] = lst
        #Adds auxiliary variables to Vn                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        Vn.extend(list(self.aux.values()))
        return P5, Vn
    
    #Creates the X auxiliary variable for terminal symbols
    def create_X(self, Vt):
        for i in range(len(Vt)):
            self.aux[Vt[i]] = ("X" + str(i))

    #Creates the Y auxiliary variable for groups of symbols
    def create_Y(self, trans):
        self.aux[trans] = "Y" + str(self.y)
        self.y += 1

    #Omogenize the transitions for conversion            
    def prepare_transition(self, trans, Vt, Vn):
        transition = trans
        #Transforms terminal symbols into auxiliary Non-terminal
        for i in Vt:
            if i in transition: transition = transition.replace(i, self.aux[i])
        #Pads the Non-terminal symbols with space
        for i in Vn:
            if i in transition: transition = transition.replace(i , i + " ")
        return transition
    
    #Recursive function converts the grammar into Chomsky normal form
    def convert_transition(self, trans): 
        #If receives less than 3 symbols, returns a Y.
        if len(trans) <= 4:
            #If the Y doesnt exist, creates one.
            if trans not in self.aux.keys():
                self.create_Y(trans)
            return self.aux[trans]
        #If it receives more than 2, it searates the first symbol, 
        #Converts the rest recursively, then merges them and converts the solution one last time
        else:
            return self.convert_transition(trans[0:2] + self.convert_transition(trans[2:]))


    def bring_to_graibach(self):
        return Graibach(self.Vn, self.Vt, self.aux, self.P)
