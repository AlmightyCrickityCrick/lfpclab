from my_token import *
from my_error import *

#The lexer itself
class Lexer:
    #Declaration of initial values for position, name file, the text of the program, and current character 
    def __init__(self, fn,  text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current = None
        self.advance()

#Function to move to the next character
    def advance(self):
        #Moves the position using specification from Position Class
        self.pos.advance(self.current)
        #Checks if there are any more characters left to be tokenized
        if self.pos.ind < len(self.text):
            self.current = self.text[self.pos.ind]
        else:
            self.current = None

    #Creates the tokens themselves by comparing the current character with characters described by rules of grammar 
    def make_tokens(self):
        tokens = []

        #The switch for checking current character. I forgot python was version 3.10 so enjoy the if-else statements
        while self.current != None:
            if self.current in ['\t', ' ', '\n']:
                self.advance()
            elif self.current in DIGITS:
                number, error = self.make_number()
                if error:
                    return [], error
                else:
                    tokens.append(number)
            elif self.current in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current == '"':
                tokens.append(self.make_string())
            elif self.current == '+':
                tokens.append(Token(PLUS, '+'))
                self.advance()
            elif self.current == '-':
                tokens.append(Token(MINUS, '-'))
                self.advance()
            elif self.current == ':':
                tokens.append(Token(ASSIGN, ':'))
                self.advance()
            elif self.current == '/':
                tokens.append(self.make_div())
            elif self.current == '*':
                tokens.append(self.make_mul())
            elif self.current == ',':
                tokens.append(Token(COMMA, ','))
                self.advance()
            elif self.current == '{':
                tokens.append(Token(LBRACE, '{'))
                self.advance()
            elif self.current == '}':
                tokens.append(Token(RBRACE, '}'))
                self.advance()
            elif self.current == '(':
                tokens.append(Token(LPARAN, '('))
                self.advance()
            elif self.current == ')':
                tokens.append(Token(RPARAN, ')'))
                self.advance()
            elif self.current in COMPARISON_SIGNS:
                number, error = self.make_comparison()
                if error:
                    return [], error
                else:
                    tokens.append(number)
            else:
                pos_start = self.pos.copy()
                char = self.current
                self.advance()            
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

            

        return tokens, None 
    #Set of functions for analysis of groups of 2 or more characters

    #Creates and matches the comparison operations
    def make_comparison(self):
        seq = ''
        seq += self.current
        pos_start = self.pos.copy()
        
        self.advance()
        seq+=self.current

        token_type = None

        for comp in COMPARISON:
            if seq == comp[0]:
                token_type = comp[1]
        
        if token_type:
            self.advance()
            return Token(f'COMPARISON[{token_type}]', seq), None
        else:
             return [], IllegalCharError(pos_start, self.pos, "'" + self.current + "'")

    #Creates and matches the token to the string type
    def make_string(self):
        seq= ''
        pos_start = self.pos.copy()

        seq += self.current
        self.advance()

        while self.current != None and self.current!= '"' and self.current in CHARACTERS:
            seq += self.current
            self.advance()
        
        seq += self.current
        self.advance()
        
        return Token(STRING, seq)

    #Checks wherever the operator is a return keyword or multiplication
    def make_mul(self):
        seq= ''
        pos_start = self.pos.copy()

        while self.current!=None and self.current in "*=":
            seq += self.current
            self.advance()
        
        if seq == '*': return Token(MUL, seq)
        else: return Token("KEYWORD[RETURN]", seq)

    #Checks if it's a division or a modulo operation
    def make_div(self):
        seq = ''
        pos_start = self.pos.copy()

        while self.current == "/":
            seq += self.current
            self.advance()
        
        if seq == '/': return Token(DIV, seq)
        else: return Token(MODULO, seq)

    #Check and matches a group of characters to identifier, keyword or built in function
    def make_identifier(self):
        id_string = ''
        pos_start = self.pos.copy()

        while self.current != None and self.current in LETTERS_DIGITS:
            id_string+=self.current
            self.advance()

        token_type = IDENT

        for keyw in KEYWORDS:
            if id_string in keyw[0]:
                token_type = f'KEYWORD[{keyw[1]}]'
                break
        
        for word in BUILT_IN_FUNCTIONS:
            if id_string in word[0]:
                token_type = f'BUILT_IN_FUNCTION[{word[1]}]'
                break
        
        return Token(token_type, id_string)
    
    #Checks wherever it's a legal number and matches it to float or int for comfort of further operations
    def make_number(self):
        num_str = ''
        pos_start = self.pos.copy()
        dot_count = 0

        while self.current not in [' ', '\t', '\n'] and self.current in CHARACTERS + '.':
            if self.current == '.':
                if dot_count == 1:
                    return [], IllegalCharError(pos_start, self.pos, "'" + self.current + "'")
                dot_count +=1
                num_str +='.'
            elif self.current not in DIGITS:
                return [], IllegalCharError(pos_start, self.pos, "'" + self.current + "'")

            else:
                num_str += self.current
            self.advance()

        if dot_count == 0:
            return Token(NUMBER, num_str), None # Doesn't copy 0 if transformed in int
        else:
            return Token(NUMBER, float(num_str)), None

#Miscellaneous class for positions
class Position:
    #Takes notice of file name, text, line, column and number id (for error's sake)
    def __init__(self, ind, ln, col, fn, ftxt):
        self.ind = ind
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
    #Advances the position. Checks wherever column has changed
    def advance(self, current):
        self.ind+=1
        self.col+=1

        if current == '\n':
            self.ln+=1
            self.col = 0
        return self

    #Copies the current position (again, used for errors)
    def copy(self):
         return Position(self.ind, self.ln, self.col, self.fn, self.ftxt)