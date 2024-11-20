# syntax_analyzer.py
import ply.yacc as yacc
from lexical_analyzer import tokens

class ASTNode:
    def __init__(self, nodetype, children=None, leaf=None):
        self.nodetype = nodetype
        self.children = children if children is not None else []
        self.leaf = leaf

    def __repr__(self):
        return f'ASTNode({self.nodetype}, {self.children}, {self.leaf})'

# Definir precedência dos operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('nonassoc', 'LESS_THAN', 'GREATER_THAN', 'LESS_THAN_EQUALS', 'GREATER_THAN_EQUALS', 'EQUALS_EQUALS', 'NOT_EQUALS'),
)

# Tabela de símbolos local para o analisador sintático
symbol_table = {}
has_error = False

# Definir as regras sintáticas
def p_programa_minipar(p):
    '''programa_minipar : bloco_stmt'''
    p[0] = p[1]

def p_bloco_stmt(p):
    '''bloco_stmt : bloco_SEQ
                  | bloco_PAR
                  | bloco_stmt bloco_SEQ
                  | bloco_stmt bloco_PAR'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2])

def p_bloco_SEQ(p):
    '''bloco_SEQ : SEQ stmts'''
    p[0] = ASTNode('SEQ', children=p[2])

def p_bloco_PAR(p):
    '''bloco_PAR : PAR stmts'''
    p[0] = ASTNode('PAR', children=p[2])

def p_bloco_IF(p):
    '''bloco_IF : IF LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ASTNode('IF', children=[p[3], ASTNode('STMTS', children=p[6])])

def p_bloco_WHILE(p):
    '''bloco_WHILE : WHILE LPAREN bool RPAREN LBRACE stmts RBRACE'''
    p[0] = ASTNode('WHILE', children=[p[3], ASTNode('STMTS', children=p[6])])

def p_bloco_INPUT(p):
    '''bloco_INPUT : INPUT LPAREN RPAREN'''
    p[0] = ASTNode('INPUT')

def p_bloco_OUTPUT(p):
    '''bloco_OUTPUT : OUTPUT LPAREN output_args RPAREN'''
    p[0] = ASTNode('OUTPUT', children=p[3])

def p_output_args(p):
    '''output_args : expr
                   | output_args COMMA expr'''
    if len(p) == 2:
        p[0] = (p[1],)
    else:
        p[0] = p[1] + (p[3],)

def p_stmts(p):
    '''stmts : stmt
             | stmts stmt'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_stmt(p):
    '''stmt : atribuicao
            | bloco_IF
            | bloco_WHILE
            | bloco_INPUT
            | bloco_OUTPUT
            | c_channel
            | c_channel_stmt'''
    p[0] = p[1]

def p_atribuicao(p):
    '''atribuicao : ID EQUALS expr
                  | ID EQUALS STRING
                  | ID EQUALS bloco_INPUT
                  | ID EQUALS receive_stmt'''
    p[0] = ASTNode('ASSIGN', children=[ASTNode('ID', leaf=p[1]), p[3]])
    symbol_table[p[1]] = p[3]

def p_expr(p):
    '''expr : INT
            | STRING
            | expr PLUS expr
            | expr MINUS expr
            | expr TIMES expr
            | expr DIVIDE expr
            | expr LESS_THAN expr
            | expr GREATER_THAN expr
            | expr LESS_THAN_EQUALS expr
            | expr GREATER_THAN_EQUALS expr
            | expr EQUALS_EQUALS expr
            | expr NOT_EQUALS expr
            '''
    if len(p) == 2:
        p[0] = ASTNode('CONST', leaf=p[1])
    else:
        p[0] = ASTNode('BIN_OP', children=[p[1], p[3]], leaf=p[2])

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ASTNode('ID', leaf=p[1])

def p_bool(p):
    '''bool : expr'''
    p[0] = p[1]

def p_comment(p):
    '''comment : COMMENT'''
    pass  # Comentários são ignorados

def p_c_channel(p):
    '''c_channel : C_CHANNEL ID LPAREN STRING COMMA STRING RPAREN'''
    p[0] = ('C_CHANNEL', p[2], p[4], p[6])

def p_c_channel_stmt(p):
    '''c_channel_stmt : send_stmt
                      | receive_stmt'''
    p[0] = p[1]

def p_send_stmt(p):
    '''send_stmt : ID DOT SEND LPAREN args RPAREN'''
    p[0] = (p[1], 'SEND', p[5])

def p_receive_stmt(p):
    '''receive_stmt : ID DOT RECEIVE LPAREN args RPAREN'''
    p[0] = (p[1], 'RECEIVE', p[5])

def p_args(p):
    '''args : expr
            | args COMMA expr'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    global has_error
    has_error = True
    if p:
        print(f"Erro sintático na linha {p.lineno}, token '{p.value}'")
    else:
        print("Erro sintático: fim de arquivo inesperado")

# Criar o analisador sintático
parser = yacc.yacc()
