# redes
Projeto de comunicação com Sockets para a disciplina de redes - ECOM029-T

O projeto consiste de um jogo da velha de dois jogadores, utilizando comunicação com sockets para ser possível jogar em rede.

O servidor deve ser inicializado executando o arquivo "server.py" da pasta src:

python server.py

Obs: Ao executar o servidor sem nenhum argumento o servidor será inicializado em 127.0.0.1:3100, para iniciar em outro ip ou porta, pode se usar:

python server.py ip_addr port


Os clientes podem ser inicializados executando o arquivo "client.py" da pasta src:

python client.py server_ip server_port

O primeiro cliente a se conectar será o jogador 1, e o segundo o jogador 2. O jogador 1 sempre começa e sempre será o círculo, assim como o jogador 2 sempre será o X.

Após o jogo ser finalizado, tanto os clientes como o servidor será encerrado.