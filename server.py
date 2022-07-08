# Servidor para o jogo da velha em python
import socket
import sys

from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Verifica se foi executado com ip e porta personalizada e define
if len(sys.argv) != 1 and len(sys.argv) != 3:
    print(
        "Uso correto: 'python server.py' para iniciar o servidor localmente com a porta 3100 (127.0.0.1:3100), ou 'python server.py ip_addr port' para iniciar em outro ip/porta"
    )
    exit()

elif len(sys.argv) == 1:
    print("Sem IP e Porta personalizados teste você será, iniciando em 127.0.0.1:3100")
    ip_addr = "127.0.0.1"
    port = 3100

elif len(sys.argv) == 3:
    ip_addr = str(sys.argv[1])
    port = int(sys.argv[2])

"""
Faz o bind do servidor no ip e porta. O cliente usará estes dados para se conectar
"""
server.bind((ip_addr, port))

"""
Servidor aguarda por 2 conexões
"""
server.listen(100)

clients = []

# Executa cada thread dos clientes
def clientthread(conn, addr):

    with conn:
        if conn == clients[0]:
            welcome = "1 - Bem vindo ao jogo da velha! Você será o Jogador 1! Seu símbolo é o O! Aguarde o Jogador 2 se conectar!"
        elif conn == clients[1]:
            welcome = "2 - Bem vindo ao jogo da velha! Você será o Jogador 2! Seu símbolo é o X! O jogo já vai começar!"

            connect_warn = "Jogador 2 conectado! O jogo já vai começar!"
            clients[0].send(connect_warn.encode())
            print("Jogadores conectados. Começando jogo...")

        # Envia uma mensagem de boas vindas
        conn.sendall(welcome.encode())

        while True:
            try:
                data = conn.recv(2048)

                if not data:
                    print("Erro de conexão! Encerrando...")
                    break

                play = data.decode("UTF-8")

                play = "jg" + play

                if conn == clients[0]:
                    clients[1].sendall(play.encode())
                    print("Jogada recebida do Jogador 1, enviando para Jogador 2...")
                else:
                    clients[0].sendall(play.encode())
                    print("Jogada recebida do Jogador 2, enviando para Jogador 1...")
            except:
                continue


while True:

    # Aceita a conexão e recebe o socket e o IP
    conn, addr = server.accept()

    # Cria uma lista de sockets clientes
    clients.append(conn)

    # Printa o endereço de quem conectou
    print(addr[0] + " conectado")

    # Cria uma thread para cada cliente
    start_new_thread(clientthread, (conn, addr))
