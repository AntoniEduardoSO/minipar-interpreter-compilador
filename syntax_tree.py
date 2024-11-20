# syntax_tree.py
import sys
import os
from syntax_analyzer import parser
from lexical_analyzer import lexer

def read_program_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        program = file.read()
    return program

def print_ast(node, indent=0):
    prefix = '    ' * indent
    if node is None:
        return
    if hasattr(node, 'nodetype'):
        print(f"{prefix}{node.nodetype}: {node.leaf if node.leaf is not None else ''}")
        for child in node.children:
            print_ast(child, indent + 1)
    elif isinstance(node, list):
        for item in node:
            print_ast(item, indent)
    else:
        print(f"{prefix}{node}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python syntax_tree.py <nome_do_programa.mp>")
        sys.exit(1)

    program_file = sys.argv[1]

    if not os.path.exists(program_file):
        print(f"Erro: O arquivo '{program_file}' não foi encontrado.")
        sys.exit(1)

    entrada = read_program_from_file(program_file)

    result = parser.parse(entrada, lexer=lexer)

    if result:
        print("Árvore Sintática:")
        print_ast(result)
    else:
        print("Erro ao gerar a árvore sintática.")

if __name__ == "__main__":
    main()
