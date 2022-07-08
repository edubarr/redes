import socket
import select
import sys

# start g


class JogoDaVelha:
    tabuleiro = {
        "1": "-",
        "2": "-",
        "3": "-",
        "4": "-",
        "5": "-",
        "6": "-",
        "7": "-",
        "8": "-",
        "9": "-",
    }
    simbolo = None

    def exibir_tabuleiro(self):
        print("Situação atual do tabuleiro:\n")
        print(
            f"│ {self.tabuleiro['1']} │ {self.tabuleiro['2']} │ {self.tabuleiro['3']} │"
        )
        print(
            f"│ {self.tabuleiro['4']} │ {self.tabuleiro['5']} │ {self.tabuleiro['6']} │"
        )
        print(
            f"│ {self.tabuleiro['7']} │ {self.tabuleiro['8']} │ {self.tabuleiro['9']} │"
        )

    def verificar_jogada(self, jogada):
        if jogada in self.tabuleiro.keys():
            if self.tabuleiro[jogada] == " ":
                return True
        return False

    def verificar_tabuleiro(self):
        # Vertical
        if self.tabuleiro["1"] == self.tabuleiro["4"] == self.tabuleiro["7"] != " ":
            return self.tabuleiro["1"]
        elif self.tabuleiro["2"] == self.tabuleiro["5"] == self.tabuleiro["8"] != " ":
            return self.tabuleiro["2"]
        elif self.tabuleiro["3"] == self.tabuleiro["6"] == self.tabuleiro["9"] != " ":
            return self.tabuleiro["3"]

        # Horizontal
        elif self.tabuleiro["1"] == self.tabuleiro["2"] == self.tabuleiro["4"] != " ":
            return self.tabuleiro["1"]
        elif self.tabuleiro["4"] == self.tabuleiro["5"] == self.tabuleiro["6"] != " ":
            return self.tabuleiro["4"]
        elif self.tabuleiro["7"] == self.tabuleiro["8"] == self.tabuleiro["9"] != " ":
            return self.tabuleiro["7"]

        # Diagonais
        elif self.tabuleiro["1"] == self.tabuleiro["5"] == self.tabuleiro["9"] != " ":
            return self.tabuleiro["1"]
        elif self.tabuleiro["3"] == self.tabuleiro["5"] == self.tabuleiro["7"] != " ":
            return self.tabuleiro["3"]

        # Os retornos até aqui são ou "X" ou "O"

        # Empate
        if [*self.tabuleiro.values()].count(" ") == 0:
            return "empate"
        else:
            return [*self.tabuleiro.values()].count(" ")

    def jogar(self, jogada, simbolo):

        # print("Posições no tabuleiro:\n")
        # print(f"│ 1 │ 2 │ 3 │")
        # print(f"│ 4 │ 5 │ 6 │")
        # print(f"│ 7 │ 8 │ 9 │")
        # print("\n")

        self.tabuleiro[jogada] = self.simbolo

        self.exibir_tabuleiro()


# finish g

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print("Uso correto: 'python client.py ip_addr port")
    exit()
ip_addr = str(sys.argv[1])
port = int(sys.argv[2])
server.connect((ip_addr, port))

welcome = str(server.recv(2048))

print(welcome)

player = welcome[0]

your_turn = False
if player == 1:
    symbol = "O"
    op_symbol = "X"
elif player == 2:
    symbol = "X"
    op_symbol = "O"

game = JogoDaVelha()

game.exibir_tabuleiro()

while True:

    data = str(server.recv(2048))

    if data.startswith("Jogador"):
        print(data)
        if symbol == "O":
            your_turn = True

    elif data.startswith("jg"):
        play = int(data.replace("jg", ""))
        game.jogar(play, op_symbol)
        your_turn = True

        game.exibir_tabuleiro()
        print("O adversario jogou!")

        estado = game.verificar_tabuleiro()

        if estado == "O":
            print("Jogador 1 e o vencedor!")
            break
        elif estado == "X":
            print("Jogador 2 e o vencedor!")
            break
        elif estado == "empate":
            print("Deu velha!!!")
            break

    if your_turn:
        print(
            "E a sua vez! Escolha uma casa entre 1 e 9 que ainda nao tenha sido jogada!"
        )
        play = input("Jogada: ")

        while True:
            if game.verificar_jogada(play):
                break
            else:
                print(
                    "Jogada invalida! Tente novamente! Escolha uma casa entre 1 e 9 que ainda nao tenha sido jogada!"
                )

        game.jogar(play, symbol)
        your_turn = False

        game.exibir_tabuleiro()

        estado = game.verificar_tabuleiro()

        if estado == "O":
            print("Jogador 1 é o vencedor!")
            break
        elif estado == "X":
            print("Jogador 2 é o vencedor!")
            break
        elif estado == "empate":
            print("Deu velha!!!")
            break
