# -*- coding: utf-8 -*-
import pygame
import sys
from collections import deque
from heapq import heappop, heappush
import math
import os
from time import sleep
import time
pygame.init()

## Ler o labirinto ##
def lerLabirinto(nomeArquivo):

	arquivoLabirinto = open(nomeArquivo, 'r')

	labirintoLido = []

	linhas = 0
	colunas = 0
	i = 0

	for linha in arquivoLabirinto:
		if(i == 0):
			linhas = int(linha.split(" ")[0])
			colunas = int(linha.split(" ")[1])
			i += 1
		else:
			labirintoLido.append(linha)
			i += 1

	arquivoLabirinto.close()

	return (linhas, colunas), labirintoLido

## Encontrar o final ##
def encontrarObjetivo(labirintoObj):

	i=0
	for linha in labirintoObj:
		objetivo = linha.find("$")
		if(objetivo > -1):
			objetivoLinha = i
			objetivoColuna = objetivo
		i += 1

	return objetivoLinha, objetivoColuna

## Encontrar o inicio ##
def encontrarInicio(labirintoIni):

	i=0
	for linha in labirintoIni:
		inicio = linha.find("#")
		if(inicio > -1):
			linhaInicio = i
			colunaInicio = inicio
		i += 1

	return linhaInicio, colunaInicio


## Converter labirinto em um grafo ##
def converterParaGrafo(labirinto):

    altura = len(labirinto)
    largura = len(labirinto[1]) - 1

    grafo = {(i, j): [] for j in range(largura) for i in range(altura) if not (labirinto[i][j] == "-")}

    # Direções
    # 1 - Norte
    # 2 - Leste
    # 3 - Sul
    # 4 - Oeste
    # 5 - Nordeste
    # 6 - Sudeste
	# 7 - Sudoeste
	# 8 - Noroeste

    for linha, coluna in grafo.keys():
        if linha < altura - 1 and not (labirinto[linha + 1][coluna]  == "-"):
            grafo[(linha, coluna)].append(("3", (linha + 1, coluna)))
            grafo[(linha + 1, coluna)].append(("1", (linha, coluna)))
        if coluna < largura - 1 and not (labirinto[linha][coluna + 1]  == "-"):
            grafo[(linha, coluna)].append(("2", (linha, coluna + 1)))
            grafo[(linha, coluna + 1)].append(("4", (linha, coluna)))
        if linha < altura - 1 and coluna < largura - 1 and not (labirinto[linha - 1][coluna + 1]  == "-") and linha > 0 and coluna >= 0:
            grafo[(linha, coluna)].append(("5", (linha - 1, coluna + 1)))
            grafo[(linha - 1, coluna + 1)].append(("7", (linha, coluna)))
        if coluna < largura - 1 and linha < altura - 1 and not (labirinto[linha + 1][coluna + 1]  == "-") and linha >= 0 and coluna >= 0:
            grafo[(linha, coluna)].append(("6", (linha + 1, coluna + 1)))
            grafo[(linha + 1, coluna + 1)].append(("8", (linha, coluna)))
    return grafo

## Função para mostrar o caminho ##
def converterSaida(caminhoSaida):
	listaSaida = []
	tamanho = len(caminhoSaida)

	posicao = encontrarInicio(labirinto)
	listaSaida.append(posicao)

	for i in range(0,tamanho):
		direcao = caminhoSaida[i]
		if direcao == "1":
			posicao = list(posicao)
			posicao[0] = posicao[0]-1
			posicao = tuple(posicao)
		elif direcao == "3":
			posicao = list(posicao)
			posicao[0] = posicao[0]+1
			posicao = tuple(posicao)
		elif direcao == "2":
			posicao = list(posicao)
			posicao[1] = posicao[1]+1
			posicao = tuple(posicao)
		elif direcao == "4":
			posicao = list(posicao)
			posicao[1] = posicao[1]-1
			posicao = tuple(posicao)
		elif direcao == "5":
			posicao = list(posicao)
			posicao[0] = posicao[0]-1
			posicao[1] = posicao[1]+1
			posicao = tuple(posicao)
		elif direcao == "6":
			posicao = list(posicao)
			posicao[0] = posicao[0]+1
			posicao[1] = posicao[1]+1
			posicao = tuple(posicao)
		elif direcao == "7":
			posicao = list(posicao)
			posicao[0] = posicao[0]+1
			posicao[1] = posicao[1]-1
			posicao = tuple(posicao)
		elif direcao == "8":
			posicao = list(posicao)
			posicao[0] = posicao[0]-1
			posicao[1] = posicao[1]-1
			posicao = tuple(posicao)

		listaSaida.append(posicao)

	return listaSaida

## Imprime o caminho ##
def imprimeSaida(caminhoFinal):
	caminhoFinal = converterSaida(caminhoFinal)
	print ("Caminho do algoritmo:")
	print (caminhoFinal)


"""
## Passo a  passo dos algoritmos ##
def passoApasso(labirintoPAP, caminhoPAP):
	linhas = len(labirintoPAP)
	colunas = len(labirintoPAP[0])-1

	caminhoPAP = converterSaida(caminhoPAP)

	os.system('cls' if os.name == 'nt' else 'clear')
	tamanho = len(caminhoPAP)

	for k in range (0, tamanho):
		for i in range(0, linhas):
			ln = ""
			for j in range (0, colunas):
				if i == caminhoPAP[k][0] and j == caminhoPAP[k][1]:
					ln += "0"
				else:
					ln += labirintoPAP[i][j]
			print (ln)
		sleep(0.5)
		os.system('cls' if os.name == 'nt' else 'clear')
"""

def passoApasso(labirinto, caminho):
	
	#montando a visualização em pygame
	#squareX/squareY = tamanho do quadrado padrão em pixels
	squareX = 50
	squareY = 50
	mapX = (int(len(labirinto[0]))-1)
	mapY = (len(labirinto))

	passo = 0
	
	for item in range(mapX):
			for char in range(mapY):
				if(labirinto[char][item] == '#'):
					posX = item*squareX
					posY = char*squareY

	


	win = pygame.display.set_mode((mapX*squareX,mapY*squareY))
	pygame.display.set_caption("Caminho")

	run = True
	while run:
		pygame.time.delay(150) #tempo entre os frames
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
		'''
		bloco para navegação manual do tabuleiro
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			if(posX <=0):
				posX = posX
			else:
				posX = posX - squareX
		if keys[pygame.K_RIGHT]:
			if(posX >= (mapX*squareX)-squareX):
				posX = posX
			else:
				posX = posX + squareX
		if keys[pygame.K_UP]:
			if(posY<=0):
				posY = posY
			else:
				posY = posY - squareY 
		if keys[pygame.K_DOWN]:
			if(posY>=(mapY*squareY)-squareY):
				posY = posY
			else:
				posY = posY + squareY

		'''
		#pinta todo o mapa de cinza claro
		win.fill((50,50,50))

		#pinta as paredes, o quadrado inicial, o quadrado final e a região que já foi percorrida
		for item in range(mapX):
			for char in range(mapY):
				if(labirinto[char][item] == '*'): #muros
					pygame.draw.rect(win,(200,200,200),(item*squareX,char*squareY,squareX,squareY))
				elif(labirinto[char][item] == '#'): #começo do labirinto
					pygame.draw.rect(win,(200,50,50),(item*squareX,char*squareY,squareX,squareY))
				elif(labirinto[char][item] == '$'): #saída do labirinto
					pygame.draw.rect(win,(50,200,50),(item*squareX,char*squareY,squareX,squareY))
				elif(labirinto[char][item] == '&'): #por onde já passou, pinta de amarelo
					pygame.draw.rect(win,(200,200,0),(item*squareX,char*squareY,squareX,squareY))

		#calculo da posição atual:
		# Direções
	    # 1 - Norte
	    # 2 - Leste
	    # 3 - Sul
	    # 4 - Oeste
	    # 5 - Nordeste
	    # 6 - Sudeste
		# 7 - Sudoeste
		# 8 - Noroeste
		
		if(caminho[passo] == '1'):
			posY = posY - squareY
		elif(caminho[passo] == '2'):
			posX = posX + squareX
		elif(caminho[passo] == '3'):
			posY = posY + squareY
		elif(caminho[passo] == '4'):
			posX = posX - squareX
		elif(caminho[passo] == '5'):
			posX = posX + squareX
			posY = posY - squareY
		elif(caminho[passo] == '6'):
			posX = posX + squareX
			posY = posY + squareY
		elif(caminho[passo] == '7'):
			posX = posX - squareX
			posY = posY	+ squareY
		elif(caminho[passo] == '8'):
			posX = posX - squareX
			posY = posY - squareY



		#incrementa o passo 
		if(passo < len(caminho)-1):
			passo = passo + 1
		else: #se for o último passo, ele pausa por X segundos e fecha o programa
			passo = passo + 1
			sleep(2)
			pygame.quit()

		temp = list(labirinto[int(posY/50)])
		
		temp[int(posX/50)] = '&'
		labirinto[int(posY/50)] = "".join(temp)
		
		
		pygame.draw.rect(win, (100,100,200), (posX,posY,squareX,squareY))
		pygame.display.update()

	pygame.quit()



## Busca em Largura ##
def buscaLargura(labirintoL):

    inicio, objetivo = encontrarInicio(labirintoL), encontrarObjetivo(labirintoL)
    fila = deque([("", inicio)])
    visitado = set()
    grafo = converterParaGrafo(labirintoL)
    Expansoes = 0

    while fila:
        caminhoBFS, atual = fila.popleft()
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminhoBFS)
        	return caminhoBFS
        if atual in visitado:
        	continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
            fila.append((caminhoBFS + direcao, vizinho))
            Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"

## Busca em Profundidade ##
def buscaProfundidade(labirintoP):

    inicio, objetivo = encontrarInicio(labirintoP), encontrarObjetivo(labirintoP)
    pilha = deque([("", inicio)])
    visitado = set()
    grafo = converterParaGrafo(labirintoP)
    Expansoes = 0
    while pilha:
        caminhoDFS, atual = pilha.pop()
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminhoDFS)
        	return caminhoDFS
        if atual in visitado:
            continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
            pilha.append((caminhoDFS + direcao, vizinho))
            Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"


## heuristica para A* (Euclidiana) ##
def heuristicas(atual, objetivo):
	return (math.sqrt(math.pow(atual[0] - objetivo[0],2) + math.pow(atual[1] - objetivo[1],2)))


## Best first ##
def bestFirst(labirintoBF):

    inicio, objetivo = encontrarInicio(labirintoBF), encontrarObjetivo(labirintoBF)
    pr_queue = []
    heappush(pr_queue, (0, 0, "", inicio))

    visitado = set()
    grafo = converterParaGrafo(labirintoBF)
    Expansoes = 0

    while pr_queue:
        _, custo, caminhoBF, atual = heappop(pr_queue)
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminhoBF)
        	return caminhoBF
        if atual in visitado:
            continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
        	if int(direcao) >= 5:
        		dist = 14
        	else:
        		dist = 10
        	heappush(pr_queue, (custo, custo + dist, caminhoBF + direcao, vizinho))
        	Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"


## Busca A* ##
def aEstrela(labirintoA):

    inicio, objetivo = encontrarInicio(labirintoA), encontrarObjetivo(labirintoA)
    pr_queue = []
    heappush(pr_queue, (heuristicas(inicio, objetivo), 0, "", inicio))

    visitado = set()
    grafo = converterParaGrafo(labirintoA)
    Expansoes = 0

    while pr_queue:
        _, custo, caminhoA, atual = heappop(pr_queue)
        if atual == objetivo:
        	print ("Expansoes: %s" %Expansoes)
        	imprimeSaida(caminhoA)
        	return caminhoA
        if atual in visitado:
            continue
        visitado.add(atual)
        for direcao, vizinho in grafo[atual]:
            heappush(pr_queue, (custo + heuristicas(vizinho, objetivo), custo + 10, caminhoA + direcao, vizinho))
            Expansoes += 1
    print ("Expansoes: %s" %Expansoes)
    return "IMPOSSIVEL!"


## Main ##
if __name__ == "__main__":
	info = lerLabirinto(sys.argv[1])
	labirinto = info[1]
	caminho = "a"

	print ("Qual o tipo de busca?")
	print("1 - Busca em Largura \n2- Busca em Profundidade \n3- Best-First\n4- A*\n")
	print("Opção: ")

	tipoBusca = input()

	print("\nDeseja ver passo a passo?")
	print("1- Sim\n2- Não\n")
	print("Opção: ")

	mostraPassos = input()

	os.system('cls' if os.name == 'nt' else 'clear')

	tempoInicial = time.time()

	if tipoBusca == "1":
		print ("Busca em largura:\n")
		caminho = buscaLargura(labirinto)
	elif tipoBusca == "2":
		print ("Busca em profundidade:\n")
		caminho = buscaProfundidade(labirinto)
	elif tipoBusca == "3":
		print ("Best-First:")
		caminho = bestFirst(labirinto)
	elif tipoBusca == "4":
		print ("A*:")
		caminho = aEstrela(labirinto)
	else:
		print("Opção inválida!")
		sys.exit()

	tempoFinal = time.time()

	if caminho == "IMPOSSIVEL!":
		print ("Não existe um caminho possível!")
		sys.exit()
	else:
		if int(mostraPassos) == 1:
			passoApasso(labirinto,caminho)
		elif int(mostraPassos) != 2:
			print("Opção inválida!")

	print("Tempo: %s segundos" % (tempoFinal - tempoInicial))
