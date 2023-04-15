import string

SYM_ADD = '+'
SYM_SUB = '-'
SYM_MUL = '*'
SYM_DIV = '/'

SYM_L_BRACKET = '('
SYM_R_BRACKET = ')'

SET_OP_SYMS = {SYM_ADD, SYM_SUB, SYM_MUL, SYM_DIV, SYM_L_BRACKET, SYM_R_BRACKET}

ALPHABET = set(string.digits).union(SET_OP_SYMS).union('. ')

STACK_END_SYM = '$'