class Graibach:
    Vn =[]
    Vt = []
    aux = []
    P ={}
    GNF ={}
    Z_count = 0

    def __init__(self, Vn, Vt, aux, P ):
        self.Vn = Vn
        self.Vt = Vt
        self.aux = list(aux.values())
        self.P= P

        #Start Transformation into GNF
        self.get_graibach()

    def get_graibach(self):
        P1 = {}
        k = list(self.P.keys())
        i = 0
        while i < len(k):
            #Check for left Recursion + Form normalization
            self.check_left(k, i, P1)
            #Check for left factoring
            self.check_right(k, i, P1)

            i += 1
        #Removes Vn that are not used anymore
        self.remove_non_accesible(P1, k)
        self.P = P1
        self.Vn = k
        
        self.print_gnf()

    #Function to print the GNF
    def print_gnf(self):
         print("Graibach normal form grammar\n Vn=", self.Vn, "\nVt=", self.Vt, "\nP=", self.P)

    #Function that checks for Inaccesible
    def remove_non_accesible(self, P, k):
        #If a Vn is not used in production anymore, deletes it
        for vn in k[1:]:
            count = 0
            for key, val in P.items():
                for trans in val:
                    if vn in trans: count+=1
            if count == 0:
                P.pop(vn)
                k.remove(vn)

    #Function to initiate checking the left side
    def check_left(self, k, i , P1):
        #Transform start returns GNF production and new Vn if recursion was found
        P1[k[i]], rec = self.transform_start(k[i], self.P[k[i]])
        #If there was a recursion, it creates new Z in Vn and P and adds the corresponding values
        if rec != 0:
            k.append('Z' + str(self.Z_count))
            self.P['Z' + str(self.Z_count)] = rec
            self.Z_count+=1
        #Deletes duplicates
        P1[k[i]] = list(set(P1[k[i]]))
    
    #Function to check for "Left factoring"
    def check_right(self, k, i, P1):
        left_fact = []
        term = set()

        #Searches if there is right recursion
        for trans in P1[k[i]]:
            if trans[-1] == k[i]:
                left_fact.append(trans)
                term.add(trans[0])
        #Checks if the the first term is met more than once
        for c in term:
            if str(left_fact).count(c) < 2:
                for trans in left_fact:
                    if trans[0] == c: left_fact.remove(trans)
        #If the first term is met more than once gets rid of left factoring
        if len(left_fact) != 0:
            for c in term:
                self.solve_left_factoring(c, list(filter(lambda x: x[0] == c ,left_fact)), k, i, P1)

    def solve_left_factoring(self, c, left_fact, k, i, P1):
        #Creates a new z and a list to hold its candidate values
        current_z = 'Z' + str(self.Z_count)
        z_trans = []
        #Adds the terms that are not repeated to Z candidates and removes from original list
        for trans in left_fact:
            print(trans)
            z_trans.append(trans[1:-1])
            if z_trans[-1]!= '': P1[k[i]].remove(trans) #Not sure what to do with candidates that result in empty string
        
        #If the candidates do not result in empty strings and list not empty, adds the Z to the production 
        z_trans = list(set(z_trans))
        if '' in z_trans: z_trans.remove('')
        if len(z_trans) >0:
            P1[k[i]].append(c + current_z)
            k.append(current_z)
            self.P[current_z] = z_trans
            self.Z_count+=1

    #Function to transform the start
    def transform_start(self, k, v):
        temp_v = v
        good_transitions = []
        recursive_transitions = []
        for trans in temp_v:
            #If Production has only terminal, or begins with terminal, appends it tost of normalized transitions
            if len(trans) == 1 or trans[0] in self.Vt:
                good_transitions.append(trans)
            #If it starts with symbol that leads to pure terminal, substitutes the Vn and appends to list
            elif trans[0] == 'X':
                good_transitions.append(self.P[trans[0:2]][0] + trans[2:])
            #If it encounters recursion adds to list of recursions
            elif trans[0] == k:
                recursive_transitions.append(trans[1:])
            else:
            #If its a simple Vn symbol, substitutes it and removes the original transition
                temp_v.extend(self.substitute_vn(trans, trans[0]))
                temp_v.remove(trans)

        #If recursives found, treats them and returns list of normalized and list of treated recursions
        if len(recursive_transitions) > 0:
            self.solve_left_recursion(recursive_transitions, good_transitions)
            return good_transitions, recursive_transitions
        
        return good_transitions, 0
    
    #Function to substitute the non terminal leading Vn
    def substitute_vn(self, trans, k):
        temp = []
        
        for t in self.P[k]:
            temp.append(t + trans[1:])
        
        return temp
    #Function to solve recursion
    def solve_left_recursion(self, rec_trans, good_transitions):
        #Creates a Z
        current_z = 'Z' + str(self.Z_count)
        n = len(good_transitions)
        
        #Appends to end of normalized a copy of normalized that ends with Z 
        for i in range(n):
            good_transitions.append(good_transitions[i] + current_z)
        
        n = len(rec_trans)

        #Adds to the list of treated recursions the recursion sans the recursive symbol and with Z at the end
        for t in range(n):
            rec_trans.append(rec_trans[t] + current_z)
            






    



