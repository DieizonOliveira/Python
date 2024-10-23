import os
import random
import time

jogo = []        # Matriz que representa o tabuleiro do jogo
espaço = "⬜️"    
bomba = "🧨"      
vazio = "  "      


# Limpar o terminal e exibir o cabeçalho do jogo
def cabeçalho():
    os.system("cls" if os.name == "nt" else "clear")  # Limpa o terminal
    print("💣 CAMPO MINADO 🧨")                       
    print("_" * 30)                                   


# Função para preencher a matriz (tabuleiro) com bombas de forma aleatória
def preencheMatriz():
    cabeçalho()                              # Exibe o cabeçalho do jogo
    global jogo                              # Acessa à variável global jogo, Matriz
    jogo = [[espaço for _ in range(5)] for _ in range(5)]  # Cria uma matriz 5x5 com células vazias
    minas_colocadas = 0                      # Contador de bombas colocadas

    # Loop para colocar 5 bombas aleatoriamente no tabuleiro
    while minas_colocadas < 5:
        linha = random.randint(0, 4)         
        coluna = random.randint(0, 4)        
        if jogo[linha][coluna] != bomba:     # Verifica se a posição já não possui uma bomba
            jogo[linha][coluna] = bomba      # Coloca a bomba na posição aleatória
            minas_colocadas += 1             # Incrementa o contador de bombas colocadas


# Função para mostrar o tabuleiro atual do jogo
def mostraTabuleiro(revelar_minas=False):
    cabeçalho()                               # Exibe o cabeçalho do jogo
    print(f"Jogador: {nome_jogador}")          # Exibe o nome do jogador
    print("  1  2  3  4  5")                  # Numeração das colunas
    for i in range(5):
        print(f"{i+1} ", end="")               # Numeração da linha
        for j in range(5):
            if jogo[i][j] == bomba:
                if revelar_minas:
                    print(bomba + " ", end="")
                else:
                    print(espaço + " ", end="")
            else:
                # Ajuste para alinhar corretamente os números
                if jogo[i][j] == vazio or jogo[i][j] == espaço:
                    print(jogo[i][j] + " ", end="")
                else:
                    print(f"{jogo[i][j]} " if len(str(jogo[i][j])) == 1 else f"{jogo[i][j]}", end=" ")
        print("")


# Função para contar quantas bombas estão ao redor de uma célula específica
def contaBombas(linha, coluna):
    direções = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  # Direções vizinhas
    bombas_ao_redor = 0                      # Contador de bombas ao redor
    for d in direções:
        nova_linha, nova_coluna = linha + d[0], coluna + d[1]  # Calcula a nova posição vizinha
        if 0 <= nova_linha < 5 and 0 <= nova_coluna < 5:       # Verifica se a posição é válida no tabuleiro
            if jogo[nova_linha][nova_coluna] == bomba:        # Verifica se há uma bomba na posição vizinha
                bombas_ao_redor += 1                          # Incrementa o contador de bombas ao redor
    return bombas_ao_redor                                   # Retorna o número de bombas ao redor


# Função para revelar células vazias e seus vizinhos
def revelaCelulas(linha, coluna):
    if jogo[linha][coluna] != espaço:         # Verifica se a célula já foi revelada
        return
    bombas_ao_redor = contaBombas(linha, coluna)  
    if bombas_ao_redor == 0:                  # Se não há bombas ao redor, revela as células vizinhas
        jogo[linha][coluna] = vazio           # Marca a célula como vazia revelada
        direções = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]  
        for d in direções:
            nova_linha, nova_coluna = linha + d[0], coluna + d[1]  
            if 0 <= nova_linha < 5 and 0 <= nova_coluna < 5:       
                revelaCelulas(nova_linha, nova_coluna)           
    else:
        jogo[linha][coluna] = f"{bombas_ao_redor}"  # Se houver bombas ao redor, mostra quantas são


# Função para verificar se todas as células seguras foram reveladas (vitória)
def verificaVitoria():
    for i in range(5):
        for j in range(5):
            if jogo[i][j] == espaço:           # Verifica se ainda há células vazias não reveladas
                return False                    # Se encontrar uma célula vazia não revelada, não há vitória
    return True                                 # Se todas as células seguras foram reveladas, há vitória


# Função para salvar o recorde do jogador no arquivo "recordes.txt"
def salvarRecorde(nome, tempo):
    with open("recordes.txt", "a") as arquivo:   # Abre o arquivo em modo de adição
        arquivo.write(f"{nome} – {tempo:.2f} segundos\n")  # Escreve o nome do jogador e o tempo de jogo


# Função para mostrar os recordes salvos no arquivo "recordes.txt"
def mostrarRecordes():
    try:
        with open("recordes.txt", "r") as arquivo:  # Abre o arquivo em modo de leitura
            recordes = arquivo.readlines()          # Lê todas as linhas do arquivo
            if recordes:
                recordes_formatados = []
                for recorde in recordes:
                    nome, tempo = recorde.rsplit(" – ", 1)  # Separa o nome e o tempo
                    recordes_formatados.append((nome.strip(), float(tempo.strip().split()[0])))

                # Ordena os recordes pelo tempo (segundo elemento da tupla)
                recordes_ordenados = sorted(recordes_formatados, key=lambda x: x[1])

                print("💣 CAMPO MINADO 🧨® \n Recordes:")
                for i, recorde in enumerate(recordes_ordenados, start=1):
                    print(f"{i}. {recorde[0]} – {recorde[1]:.2f} segundos")
            else:
                print("Nenhum recorde encontrado.")  # Se não houver recordes, exibe mensagem
    except FileNotFoundError:
        print("Nenhum recorde encontrado.")          # Se o arquivo não existir, exibe mensagem


# Função principal que controla o fluxo do jogo
def jogada():
    inicio = time.time()                           # Marca o tempo de início do jogo
    while True:
        try:
            x = int(input("Digite o número da linha (De 1 a 5): ")) - 1  # Solicita a linha ao jogador
            y = int(input("Digite o número da coluna (De 1 a 5): ")) - 1  # Solicita a coluna ao jogador
            if 0 <= x < 5 and 0 <= y < 5:           # Verifica se as coordenadas estão dentro dos limites do tabuleiro
                linha = x
                coluna = y
                if jogo[linha][coluna] == bomba:    # Se a célula escolhida for uma bomba, o jogador perde
                    mostraTabuleiro(revelar_minas=True)  # Mostra todas as bombas
                    print("\n💣💣💣 Você explodiu! 💀⚰️")
                    jogo_novo = input("Jogar novamente? (s/n): ").upper()
                    if jogo_novo == "S":           # Opção para jogar novamente
                        preencheMatriz()          # Reinicia o jogo com um novo tabuleiro
                        mostraTabuleiro()
                    else:                          # Se não quiser jogar novamente, encerra o jogo
                        print("💣 CAMPO MINADO 🧨®")
                        return
                elif jogo[linha][coluna] == espaço:
                    revelaCelulas(linha, coluna)
                    mostraTabuleiro()
                    if verificaVitoria():
                        mostraTabuleiro(revelar_minas=True)
                        fim = time.time()
                        tempo_total = fim - inicio
                        print(f"\n Parabéns, {nome_jogador}! Você venceu!")
                        salvarRecorde(nome_jogador, tempo_total)
                        return
        except ValueError:
            print("Erro! ⚠️ Verifique o valor digitado!")


# Função para exibir o menu inicial e controlar as opções do jogo
def menuInicial():
    while True:
        cabeçalho()  # Exibe o cabeçalho do jogo
        print("1. Jogar")
        print("2. Ver recordes")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":  #Inicia o Jogo
            global nome_jogador
            nome_jogador = input("Digite seu nome: ")  
            preencheMatriz()  
            mostraTabuleiro()  
            jogada()  
        elif escolha == "2":  # Visualiza os recordes
            mostrarRecordes() 
            input("Pressione Enter para voltar ao menu...")  
        elif escolha == "3":  # Sai do jogo
            print("💣 CAMPO MINADO 🧨®")  # Mensagem de saída
            break  # Encerra o loop e finaliza o jogo
        else:
            print("Opção inválida!! Tente novamente.")  # Mensagem de erro se a opção digitada não existir


# Inicialização do jogo chamando o menu inicial
menuInicial()
