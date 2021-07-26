import sys
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import jsons as json
import os
from numpy.core.fromnumeric import shape, size
from os import X_OK, listdir

class Imagem:
    def __init__(self, valor, valorR, valorG, valorB, local):
        self.valor = valor
        self.valorR = valorR
        self.valorG = valorG
        self.valorB = valorB
        self.diretorio = local

    def __str__(self):
        return f"({self.valor}, {self.valorR}, {self.valorG},{self.valorB} {self.diretorio})"

class GrupoImagens:
    def __init__(self):
        self.imagens = []
        
    def adicionar(self, im):
        self.imagens.append(im)

    def __str__(self):
        text = ""
        for im in self.imagens:
            text += f"({im.valor}, {im.valorR},{im.valorG},{im.valorB}, {im.diretorio})\n"
        return text

def getGrayMeanValue(imagem, x1, x2, y1, y2): #calcula o valor médio em escala de cinza da imagem entre os pontos
    soma = 0

    for x in range(x1, x2):
        for y in range(y1, y2):
            soma += imagem[x][y]

        
    return soma / ((x2 - x1)*(y2-y1))

def getIntColor(imagem, x1, x2, y1, y2):    #calcula o a cor média da imagem entre os pontos
    soma = [0,0,0]

    for x in range(x1, x2):
        for y in range(y1, y2):
            soma[0] += imagem[x][y][0]
            soma[1] += imagem[x][y][1]
            soma[2] += imagem[x][y][2]

    tamanho = (x2 - x1)*(y2-y1)
    media = [soma[2] / tamanho, soma[1] / tamanho, soma[0] / tamanho]
    return media

def mergeImages(imagem1, imagem2, eixo):             #realiza a concatenação entre duas imagens
    return np.concatenate((imagem1, imagem2), eixo)

def getNearestImage(valor, listaJson):               #realiza busca binaria no json, procurando o valor em cinza mais proximo
    ini = 0
    fim = len(listaJson) - 1
    meio = 0

    while ini<=fim:
        meio = (ini + fim) // 2
        if listaJson[meio]['valor'] == valor:
            return cv.imread(listaJson[meio]['diretorio'])
        else:
            if valor < listaJson[meio]['valor']:
                fim = meio - 1
            else:
                ini = meio + 1

    return cv.imread(listaJson[meio]['diretorio'])

def getNearestImageRGB(valor, listaJson):           #realiza a busca no json, para encontrar a imagem com cor mais proxima
    count = 0
    fim = len(listaJson) - 1
    proximo = 0
    menorDist = float("inf")
    while count<=fim:
        r = listaJson[count]['valorR'] - valor[0]
        g = listaJson[count]['valorG'] - valor[1]
        b = listaJson[count]['valorB'] - valor[2]
        distancia = (r**2 + g**2 + b**2)            #utiliza a distancia entre os valores RGB para definir o mais proximo
        if(distancia < menorDist):
            menorDist = distancia
            proximo = count
            
        count += 1
    return cv.imread(listaJson[proximo]['diretorio'])

def update(porcentagem):                            #exibe o progresso do programa
    print(f"{(porcentagem*100):.2f}%")

def photomosaicRGB(imagem, listaJson, Rx, Ry, resolução=800, pretoBranco = False):       #funcao que gera o mosaico
    formato = shape(imagem)
    nx = formato[0]//Rx
    ny = formato[1]//Ry
    imagem = cv.resize(imagem, (nx * Rx, ny * Ry))      #calcula a quantidade de imagens que ira compor a imagem final, e redimensiona a original

    if pretoBranco:                 
        imagem = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)

    imagemFinal = None
    count = 0
    total = Rx * Ry

    for y in range(Ry):
        imagemProv = None
        for x in range(Rx):                          #percorre todos os blocos da imagem
        
            if pretoBranco:
                valor = getGrayMeanValue(imagem, y*ny, (y+1)*ny, x*nx, (x+1) * nx)
                imagemSub = getNearestImage(valor, listaJson)
            else:
                valor = getIntColor(imagem, y*ny, (y+1)*ny, x*nx, (x+1) * nx)
                imagemSub = getNearestImageRGB(valor, listaJson)                  #calcula a cor media da imagem e busca a mais proxuma

            imagemSub = cv.resize(imagemSub, (resolução, resolução))               #redimendiona a imagem para o tamanho desejado
            if pretoBranco:
                imagemSub = cv.cvtColor(imagemSub, cv.COLOR_BGR2GRAY)
            if imagemProv is None:
                imagemProv = imagemSub
                continue
            else:
                imagemProv = mergeImages(imagemProv, imagemSub, 1)                #concatena a imagem anterior com o proximo bloco

            count += 1
            
        if imagemFinal is  None:
            imagemFinal = imagemProv
            continue
        else:
            imagemFinal = mergeImages(imagemFinal, imagemProv, 0)

        update(count / total)              #exibe na tela o progresso

    return imagemFinal


imagemDir = "/testes/render6.jpg"   #diretorio da imagem a ser processada
imagemOut = "saidas/"            #diretorio de destino da imagem. ELE PRECISA EXISTIR
imagemRes = 60                   #quantidade de imagens para compor a final
imagemScale = 10                 #fator de redução das imagens individuais
pretoeBranco = False
conjunto = "images/"

sizeArg = size(sys.argv)

if sizeArg > 1:
    imagemDir = sys.argv[1] 

if sizeArg > 2:
    imagemOut = sys.argv[2]  

if sizeArg > 3:
    imagemRes = int(sys.argv[3])

if sizeArg > 4:
    imagemScale = int(sys.argv[4])

if sizeArg > 5:
    pretoeBranco = sys.argv[5] == "True"

if sizeArg > 6:
    conjunto = sys.argv[6]

imagemDir = imagemDir.replace("\\", "/")
imagemOut = imagemOut.replace("\\", "/")

if imagemDir[-1] != "/":
    imagemDir += "/"

if conjunto[-1] != "/":
    conjunto += "/"

imagemOut += os.path.basename(imagemDir[:-1]) 

imagem = cv.imread(imagemDir)
file = open(conjunto + "indices.json", "r")
objJson = json.loads(file.read())
imagemFinal = photomosaicRGB(imagem, objJson['imagens'], imagemRes, imagemRes, imagemScale, pretoeBranco)
cv.imwrite(imagemOut, imagemFinal)