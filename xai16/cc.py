src = '''
main() {
    int d;
    d = f(3, 4);
}

int f(int a, int b) {
    int c;
    c = a + b / a * b % a - b | a ^ b & a ? b : (a ~ b);
    return c;
}
'''

tokens = ["main", "(", ")", "{", "int", "d", ";", '"hello"', ";" "d", "=", "f", "(", "3", "4", ")", ";", "}"]

'''
PROG = (FNDEF, PROG)
FNDEF = (ID, OPEN_PAREN, CLOSE_PAREN, OPEN_BRACE, BODY, CLOSE_BRACE)
BODY = (STATEMENT, BODY)
STATEMENT = (LOCAL, ASSIGNMENT, EXPRESSION, SEMICOLON)
ASSIGNMENT = (ID, EQUALS, EXPRESSION)
EXPRESSION = '??'
LOCAL = TYPE, ID  (, EQUALS, EXPRESSION)?
EQUALS = '='
ID = 'a-z[a-z0-9_]+'
'''



def lex(src):
    sep = '(){};,+/*%-'
    prev = None
    for char in src:
        try:
            char
        finally:
            prev = char

for token in lex(src):
    print(token)
