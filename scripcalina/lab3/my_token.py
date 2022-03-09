import string

#Declare constants in language

DIGITS = '0123456789'
LETTERS = string.ascii_letters

LETTERS_DIGITS = LETTERS + DIGITS

CHARACTERS = string.printable

NUMBER = 'NUMBER'
STRING = 'STRING'
IDENT = 'IDENTIFIER'

ASSIGN = 'ASSIGN'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MODULO = 'MODULO'

COMPARISON_SIGNS = '=<>'
COMPARISON = [('==', 'EQUALS'), ('>>', 'GREATER'), ('<<','LESSER'), ('<=', 'LESSER OR EQUALS'), ('>=','GREATER OR EQUALS'), ('<>', 'NOT EQUALS')]

LPARAN = 'LPARAN'
RPARAN = 'RPARAN'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'

COMMA = 'COMMA'

KEYWORDS = [('nya', 'VAR'), ('quack', 'IF'), ('hjonk', 'ELSE',), ('*=*', 'RETURN',), ('pikachu','FUNC'), ('owo', 'AND'), ('uwu', 'OR')]
BUILT_IN_FUNCTIONS = [('konnichiwa', 'PRINT')]

#Declaring the class token that will represent the blueprint for tokenization within th elexer

class Token:
    def __init__(self, type_, value = None):
        self.type = type_
        self.value = value

#Function for specifying the formatting of each token    
    def __repr__(self):
        if self.value:
            return f'\n{self.type} : {self.value} '
        return f'\n{self.type}'