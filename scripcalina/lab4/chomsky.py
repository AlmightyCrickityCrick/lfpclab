class Chomsky:
    Vn = []
    Vt = []
    P = {}
    
    def __init__(self, Vn, Vt, P):
        self.Vn = Vn
        self.Vt = Vt
        self.P = self.create_P(P)
        print(self.P)

    def create_P(self, P):
        P1 = {}

        for key in self.Vn:
            P1[key] = []
        
        for el in P:
            P1[el[0]].append(el[(el.index("->") + 2):])
        
        return P1

    def normalize_grammar(self):
        P1 = self.eliminate_empty(self.P)
        P2 = self.eliminate_renaming(P1)
        P3, Vn, Vt = self.eliminate_inaccessible(P2)
        P4, Vn = self.eliminate_non_productive(P3, Vn, Vt)
        print(P4)

        P5, Vn = self.bring_to_chomsky(P4, Vn, Vt)
        print(P5)
    
    def eliminate_empty(self, P):
        P1 = P
        empty_set = ["empty"]
        em = 0
        #Eliminates Vn that might lead to empty
        while em < len(empty_set):
            for k, v in P1.items():
                #Marks the Vn that leads to empty and deletes the empty transitin
                if "empty" in v:
                    empty_set.append(k)
                    P1[k].remove(empty_set[em])
                    #Marks the renamings that lead to empty 
                if (empty_set[em] in v) and (k not in empty_set):
                    empty_set.append(k)
            em += 1
        #Adds transition variants without the Vn that lead to empty
        self.substitute_empty(empty_set[1:], P1)

        return P1

    def substitute_empty(self, empty_set, P):
        for k, v in P.items():
            for trans in v:
                if len(trans) < 2:
                    continue
                else:
                    for i in range(len(trans)):
                        if trans[i] in empty_set:
                            if i == (len(trans) -1): tmp = trans[:-1] 
                            else: tmp = trans[:i] + trans[(i + 1):]
                            if tmp not in P[k]: P[k].append(tmp)
    
    def eliminate_renaming(self, P):
        P2 = P.copy()
        for k, v in P2.items():
            for trans in v:
                if trans in self.Vn:
                    tmp = trans
                    P2[k].remove(tmp)
                    P2[k].extend(P2[tmp])
                    P2[k] = list(set(P2[k]))
                        
        return P2
                    
    def eliminate_inaccessible(self, P):
        P3 = {}
        access_vn = ["S"]
        access_tn = []

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

    def eliminate_non_productive(self, P, Vn, Vt):
        P4 = P.copy()
        productive = []

        no_change_flag = False
        while not no_change_flag:
            tmp = []
            for v in Vn:
                #Filters and creates a list of all terminals for a certain Vn in production
                direct_prod = list(filter(lambda x: x in Vt, P4[v]))
                indirect_prod = list(filter(lambda x: x in str(P4[v]), productive))
                res = direct_prod
                res.extend(indirect_prod)
                if len(res) > 0:
                    tmp.append(v)
                
            if len(tmp) == len(productive) or len(tmp) == len(Vn): 
                no_change_flag = True
                productive = tmp
            else:
                productive = tmp

                    
        if len(productive) == len(Vn) : return P4, Vn

        non_prod = list(set(Vn).difference(set(productive)))

        for np in non_prod:
            P4.pop(np)
            for k, v in P4:
                for trans in v:
                    if np in trans: P4[k].remove(trans)

        return P4, productive

    def bring_to_chomsky(self, P, Vn, Vt):
        pass
        