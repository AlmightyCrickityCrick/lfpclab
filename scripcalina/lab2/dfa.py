
class DFA:
    states = [] # Keeps track on which states have been explored yet. Redundant. Could be checked just from keys of dictionary, but meh.
    trans = [] # Contains trasition variables
    dictFA = {} # Contains the DFA itself
    source_nfa = {} # Contains the source NFA dictionary. Also kinda redundant.
    
    # Initialisation method
    def __init__(self, nfa):
        self.source_nfa = nfa.dictFA
        self.trans = nfa.trans
        self.transform_nfa()

    # Creates the dictionary for all possible transitions 
    def add_transition_dict(self):
        temp = {}
        for t in self.trans:
            temp[t] = ""
        return temp
    
    # Sorts string of states
    def sort_string(self, dest):
        # Removes q and splits the original string into a list of strings containing only numbers
        temp = dest.replace("q", ",").split(",")
        temp = temp[1:]
        # Sorts list of numbers
        temp.sort()
        temp2 = ""
        # Prefixes each number from list with "q" and concatinates them together
        for state in temp:
            temp2 = temp2 + "q" + state
        return temp2

    #Checks if destination states need sorting. Sends to sorting if contain more than 1 state. 
    def sort_destination(self, current):
        for trans, dest in self.dictFA[current].items():
            if len(dest) <= 2:
                continue
            else:
                print("Destination state ", dest, " has multiple states. Begin sorting.") 
                self.dictFA[current][trans] = self.sort_string(dest)
                print("Sorting ended.")

    # Adds the transitions to the table
    def add_transitions(self, current):
        beg = 0
        end = 2
        # Takes every simple state within current state
        while end <= len(current):
            print("Viewing transitions for ", current[beg:end], " of ", current, "." )
            # Checks which other states current simple state is connected to in original NFA table
            for k, v in self.source_nfa[current[beg:end]].items():
                if v != "":
                    print(current[beg:end],", of ", current ," is connected to ", v," through transition variable ", k, ".")
                # If the found state is not already in the table for this transition varible and current state, adds it
                if v not in self.dictFA[current][k]:
                    print("Adding ", v, " to the table.")
                    self.dictFA[current][k] = self.dictFA[current][k] + v
            # Increments current simple state
            beg +=2
            end +=2
        # Sends the states obtained for current state to sorting
        self.sort_destination(current)
  
    # Explores a state
    def explore_state(self, current):
        print("Exploring state ", current, ".")
        # If the state has already been explored once (is in state list), it is skipped
        if current in self.states:
            print("This state is not new.")
            return
        else:
            # If state wasn't explored, it gets added to explored list
            print("This state is new. Adding it to table.")
            self.states.append(current)
            # State gets added to dictionary and mapped to a dictionary with transition variables
            self.dictFA[current] = self.add_transition_dict()
            # State gets mapped dictionary populated with destination states
            self.add_transitions(current)
            print("Checking for next new states.")
            # States the current state is connected to are sent to be explored
            for next in self.dictFA[current].values():
                if next != "":
                    self.explore_state(next)
              

    def transform_nfa(self):
        # Sets the Initial state as current state to be explored
        current = "q0" 
        print("Starting DFA creation.")       
        self.explore_state(current)
        print("DFA has been created.")

       
