from dfa import DFA

class NFA:
    states = list() # Stores the states
    trans = list() # Stores the transitions
    dictFA= {} # Stores the FA as hashmap/dictionary
    rules = [] #Stores the cleaned up analytical description of the NFA 


    # Initialization function
    def __init__(self, states, trans, automaton):
        self.states = self.clean_language(states)
        self.trans = self.clean_language(trans)
        self.clean_rules(automaton)
        #self.to_dictionary(automaton)

    # Transforms string NFA descriptors into lists
    def clean_language(self, data):
        return  data.replace(" ", "").replace("{", "").replace("}", "").split(",")


    def set_transition(self, src, transition, dest):
        # Redundant. Could simplify wiithout the if-else. But leaving in case empty string not accepted as a valid value for no transition
        if self.dictFA[src][transition] == "":
            self.dictFA[src][transition] = dest
        else:
            self.dictFA[src][transition] = self.dictFA[src][transition] + dest
    
    # Transforms the list of rules into a dictionary
    def to_dictionary(self):
        for rule in self.rules:
            # Divides each rule into source, destination state and transition variable
            src = rule[1:3]
            transition = rule[4]
            dest = rule[7:9]
            # If the source already in variable then places the transitions described by the rules in the dictionary
            if src in self.dictFA.keys():
                self.set_transition(src, transition, dest)
            else:
                # If the source not in dictionary, creates a key with the source and maps it into an empty dictionary
                self.dictFA[src] = {}
                # Populates the inner dictionary with empty string mapped to trnasition variables 
                for t in self.trans:
                    self.dictFA[src][t] = ""
                # Places transitions in the rules into the inner dictionary
                self.set_transition(src, transition, dest)

    # Cleans up the FA rules. Shocker, fellas, I know!
    def clean_rules(self, automaton):
        # Replaces the empty spaces and splits the string into a list. If u have d as transition variable, rip, i guess?
        rules = automaton.replace(" ", "").split("d")
        rules = rules[1:]
        # Places the cleaned up rules in a list pertaining to the class
        for rule in rules:
            if rule[-1] == ",":
                self.rules.append(rule[:-1])
            else:
                self.rules.append(rule)

    # Transforms the NFA to DFA (duh)
    def to_dfa(self):
        return DFA(self)