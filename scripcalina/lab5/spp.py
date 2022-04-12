from operator import index
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

    def create_parser(self):
        self.create_first_last()
        self.first_last_table = pd.DataFrame.from_records(data=[self.first, self.last], index=["First", "Last"]).T.reindex(self.Vn)
        print(self.first_last_table)
        self.create_rules()
        print(self.first_rule)
        print(self.second_rule)
        print(self.third_rule)

        self.create_matrix()

    def create_matrix(self):
        pass


    def create_rules(self):
        for k, v in self.P.items():
            for trans in v:
                self.create_first_rule(trans)
                self.create_second_rule(trans)
                self.create_third_rule(trans)

    def create_first_rule(self, trans):
        if len(trans) < 2:
            return 
        c = 0
        while c <len(trans) - 1:
            self.first_rule.append(trans[c] + "=" +trans[c + 1])
            c+=1
    
    
    
    def create_second_rule(self, trans):
        if len(trans) < 2:
            return
        c = 1
        while c <len(trans):
            if trans[c] in self.Vn:
                for char in self.first[trans[c]]:
                    self.second_rule.append(trans[c-1] + "<" +char)
            c+=1
    

    def create_third_rule(self, trans):
        if len(trans) < 2:
            return
        c = 0
        while c <len(trans) -1:
            if trans[c] in self.Vn:
                for char in self.last[trans[c]]:
                    if trans[c + 1] in self.Vt: 
                        self.third_rule.append(char + ">" + trans[c+1] )
                    else:
                        for charf in self.first[trans[c+1]]:
                            self.third_rule.append(char + ">" + charf)
            c+=1

    def create_first_last(self):
        self.first = {}
        self.last = {}

        for key in self.P.keys():
            if key not in self.first:
                self.first[key] = self.get_first_last(key, 0, self.first)
            if key not in self.last:
                self.last[key] = self.get_first_last(key, -1, self.last)

        print(self.first)
        print(self.last)
    

    def get_first_last(self, key, i, column):
        fl_set = set()
        for trans in self.P[key]:
            if trans[i] in self.Vt:
                fl_set.add(trans[i])
            else:
                if trans[i] in column.keys():
                    fl_set = fl_set.union(column[trans[i]])
                    fl_set.add(trans[i])
                elif trans[i] == key:
                    fl_set.add(trans[i])
                else:
                    fl_set = fl_set.union(self.get_first_last(trans[i], i, column))
                    fl_set.add(trans[i])

        column[key] = fl_set
        return fl_set


