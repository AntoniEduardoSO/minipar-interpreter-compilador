# main.py
import socket
import threading
import syntax_analyzer as ps
import lexical_analyzer as lexic
from Executor import Executor
import sys
import os

HOST = 'localhost'
PORT = 8888

def handle_client(conn, addr):
    print(f"Conexão estabelecida com {addr}")
    try:
        data = conn.recv(4096)
        if not data:
            return
        message = data.decode('utf-8')
        lines = message.split('\n')
        program_file = lines[0]
        inputs = lines[1:]  # As entradas fornecidas pelo cliente

        if not os.path.exists(program_file):
            response = f"Erro: O arquivo '{program_file}' não foi encontrado."
            conn.sendall(response.encode('utf-8'))
            return

        entrada = read_program_from_file(program_file)

        lexer = lexic.lexer
        result = ps.parser.parse(entrada, lexer=lexer)

        if result:
            executor = Executor(inputs=inputs)
            executor.execute_stmt(result)
            output = ''.join(executor.outputs)
            conn.sendall(output.encode('utf-8'))
        else:
            conn.sendall("Erro ao executar o programa.".encode('utf-8'))

    finally:
        conn.close()

def read_program_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        program = file.read()
    return program

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Servidor iniciado em {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
