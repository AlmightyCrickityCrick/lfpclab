from lexer import *

#Driving code. Opens document. Creates Lexer. Creates Tokens. And brings back either the result or the error
text = open(r'C:\Users\Dickenson\Documents\lfpclab\scripcalina\lab3\my_language.txt') #This looks ugly in the editor. It is correct, tho.
lexer = Lexer('<my_language.txt>', text.read())
result, error = lexer.make_tokens()

if error: 
    print(error.as_string())
else:
    print(result)