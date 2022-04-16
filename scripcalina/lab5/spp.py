import pandas as pd
class Simple_PP:
    Vn = []
    Vt = []
    P = {}

    first_last_table = pd.DataFrame()
    first_rule = []
    second_rule = []
    third_rule = []
    matrix = pd.DataFrame()

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

    #Driving function for creating parser
    def create_parser(self):
        self.create_first_last()
        self.create_rules()
        self.create_matrix()

    #Function to create the simple precedence Matrix
    def create_matrix(self):
        #Adds all Vn, Vt and $ sign to a list
        elem = self.Vn.copy()
        elem.extend(self.Vt)
        elem.append("$")

        #Creates the Matrix itself and fills it with -
        sp_matrix = [["-" for i in range(len(elem))]for j in range(len(elem))]
        for row in range(len(elem)-1):
            sp_matrix[row][-1] = ">"
            sp_matrix[-1][row] = "<"

        
        #Places the symbols of precedence according to the rules
        rules = self.first_rule.copy()
        rules.extend(self.second_rule)
        rules.extend(self.third_rule)

        for rule in rules:
            sp_matrix[elem.index(rule[0])][elem.index(rule[2])] = rule[1]
        
        #Makes the matrix an attribute and transforms it into a Dtaframe for ease of access
        self.matrix = pd.DataFrame(data = sp_matrix, index=elem, columns=elem)
        print("\nSimple Precedence Matrix\n")
        print(self.matrix)



    #Function that iterates through each transition to assign rules
    def create_rules(self):
        for k, v in self.P.items():
            for trans in v:
                self.create_first_rule(trans)
                self.create_second_rule(trans)
                self.create_third_rule(trans)
        print("\n The three rules:\n")
        print("First Rule: ", self.first_rule)
        print("Second Rule: ", self.second_rule)
        print("Third Rule :", self.third_rule)


    #Creates the rule for = sign
    def create_first_rule(self, trans):
        if len(trans) < 2:
            return 
        c = 0
        #If a transition has 2 or more characters adds a rule with = between each 2 neighbors
        while c <len(trans) - 1:
            self.first_rule.append(trans[c] + "=" +trans[c + 1])
            c+=1
    
    
    #Creates the rule for < sign
    def create_second_rule(self, trans):
        if len(trans) < 2:
            return
        #Starting with second character in transition, checks if current character is a Nonterminal
        c = 1
        while c <len(trans):
            if trans[c] in self.Vn:
                #If it is a nonterminal, assigns the < between the character previous to the nonterminal
                #and each of the characters in the first column of first-last table of the nonterminal
                for char in self.first[trans[c]]:
                    self.second_rule.append(trans[c-1] + "<" +char)
            c+=1
    
    #Creates the rule for > sign
    def create_third_rule(self, trans):
        if len(trans) < 2:
            return
        #Checks if the current character is a nonterminal
        c = 0
        while c <len(trans) -1:
            if trans[c] in self.Vn:
                #It it is a nonterminal, for each of the characters in it's last column in first-last table
                for char in self.last[trans[c]]:
                    #Assigns the > sign between it and the character after the nonterminal, if the next is terminal
                    if trans[c + 1] in self.Vt: 
                        self.third_rule.append(char + ">" + trans[c+1] )
                    else:
                        #Asigns the > sign between it and each of the characters within first column of the character after the nonterminal, if the next in nonterminal
                        for charf in self.first[trans[c+1]]:
                            if charf in self.Vt: self.third_rule.append(char + ">" + charf)
            c+=1
    #Function that starts the finding of first last for each Nonterminal in Vn
    def create_first_last(self):
        self.first = {}
        self.last = {}

        for key in self.P.keys():
            if key not in self.first:
                self.first[key] = self.get_first_last(key, 0, self.first)
            if key not in self.last:
                self.last[key] = self.get_first_last(key, -1, self.last)

        #Dataframe for printing the table for vanity's sake 
        self.first_last_table = pd.DataFrame.from_records(data=[self.first, self.last], index=["First", "Last"]).T.reindex(self.Vn)
        print("First-Last Table:\n")
        print(self.first_last_table)
    
    #Function that finds the characters of last or first column, with i indicating the position of first or last character
    #For first column, the function receives the first set and i = 0 as position for first searching
    #For last column receives the last set as column and i = -1 for index of searching
    def get_first_last(self, key, i, column):
        if key not in column: column[key] = set()
        #For each tansition of the Vn
        for trans in self.P[key]:
            if trans[i] in column[key]: continue 
            #Adds character in index to the set
            column[key].add(trans[i])
            if trans[i] in self.Vn:
                #If its a nonterminal whose column has already been found, adds all the characters to the set
                if trans[i] in column.keys():
                    column[key] = column[key].union(column[trans[i]])
                #If it's a nonterminal that hasnt been found, it is searched and then it's values are added to the set
                elif trans[i] != key:
                    column[key] = column[key].union(self.get_first_last(trans[i], i, column))

        #The set that was found is added directly to the column and then returned, to minimize the need
        # of rechecking the same symbols the same symbols during recursive call
        return column[key]

    #Parses a word to check if it's part of the grammar
    def parse(self, init_word):
        print("\nParsing word " + init_word)
        word = self.first_normalize(init_word)
        print(word)
        is_parsed = False
        is_error = False

        while not (is_parsed or is_error):
            #Checks if the root has been reached
            if word == "$<S>$": 
                is_parsed = True
                break
            #Finds first occurence of >, last occurence as <, as well as the characters before and after them
            stop = word.index(">")
            start = word.rindex("<", 0, stop)
            prev = word[start - 1]
            next = word[stop+1]
            
            #Selects the transition included within <>
            trans = word[start + 1:stop]
            #Cleans it of = sign for checking in grammar transitions dictionary
            if "=" in trans: trans = trans.replace("=", "")
            
            #Finds candidates or errors, if word is not in language 
            new, is_error = self.find_candidates(trans, prev, next)
            if is_error: break
            #Substitutes the transition between <> with it's nonterminal symbol
            word = word[:start] + self.matrix.loc[prev, new] + new + self.matrix.loc[new, next] + word[stop + 1:]
            print(word)
        
        if is_error: print("Word " + init_word+  " is not part of Language")
        if is_parsed: print("Word " + init_word + " is part of Language")


    #Function to populate the word with precedence symbols
    def first_normalize(self, word):
        word = "$" + word + "$"
        
        normalized_word = ""
        for c in range(len(word)-1):
            normalized_word+= word[c] + self.matrix.loc[word[c], word[c+1]]
        
        normalized_word+="$"
        return normalized_word

    #Finds candidates for the new symbol
    def find_candidates(self, trans, prev, next):
        candidates = []
        #Searches a transition in grammar contains the given segment    
        for k, v in self.P.items():
            if trans in v: 
                #Checks if there is precedence betwen a possible candidate and its neighbouring symbols
                if self.matrix.loc[prev, k]!="-" and self.matrix.loc[k, next]!="-":
                    candidates.append(k)
        #Checks if any candidates have been found
        if len(candidates) == 0:
            return None, True 
        elif len(candidates) == 1:
            return candidates[0], False
        else:
            #If 2 or more candidates, checks which of them has = relationship with both neighbours
            for cand in candidates:
                if self.matrix.loc[prev, cand]=="=" and self.matrix.loc[cand, next]=="=":
                    return cand, False

            #If 2 or more candidates, checks which of them has = relationship with its right neighbour
            for cand in candidates:
                if self.matrix.loc[cand, next]=="=":
                    return cand, False
            #If 2 or more candidates, checks which of them has = relationship with its left neighbour
            for cand in candidates:
                if self.matrix.loc[prev, cand]=="=":
                    return cand, False
            #If neither, for now, returns the first candidate
            return candidates[0]
            
        
                




