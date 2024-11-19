# client.py
import socket

HOST = 'localhost'  # Endereço do servidor
PORT = 8888        # Porta usada pelo servidor

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        program_name = input("Escreva o nome do programa desejado:\n")
        inputs = []

        if program_name == 'program1-client.mp':
            input1 = input("Escreva o input1:\n")
            inputs.append(input1)
            input2 = input("Escreva o input2:\n")
            inputs.append(input2)
            cond = input('Escreva o condicional ("-","+","*","/"):\n')
            inputs.append(cond)
        else:
            # Para outros programas, você pode adicionar lógica semelhante
            print("Programa não reconhecido ou não há entradas adicionais necessárias.")

        message = '\n'.join([program_name] + inputs)
        s.sendall(message.encode())

        data = s.recv(4096)
        print('Resultado:')
        print(data.decode())

if __name__ == '__main__':
    main()
