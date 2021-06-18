import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import jsons as json
from numpy.core.fromnumeric import shape, size
from os import listdir
import sys

class Imagem:
    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def __str__(self):
        return f"({self.nome}, {self.valor})"

class GrupoImagens:
    def __init__(self):
        self.imagens = []
        
    def adicionar(self, im):
        self.imagens.append(im)

    def __str__(self):
        text = ""
        for im in self.imagens:
            text += f"({im.nome}, {im.valor})\n"
        return text

def processGrayImages(diretorio, dirSaida, quantidade, tamanho):
    valores = GrupoImagens()

    listaDir = listdir(diretorio)

    for file in listaDir:
        imagem = cv.imread(diretorio + file)
        imagemGray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        valorBruto = cv.mean(imagemGray[0])
        valores.adicionar(Imagem(dirSaida + file, valorBruto[0]))
        imagemGray = cv.cvtColor(imagemGray, cv.COLOR_GRAY2BGR)
        imagemGray = cv.resize(imagemGray, tamanho)
        cv.imwrite(dirSaida + file, imagemGray)
    valores.imagens.sort(key=lambda x: x.valor, reverse=False)
    return valores


if size(sys.argv) < 3:
    print("Digite o diretorio com as imagens e o diretorio de saida")
    exit(1)

diretorio = sys.argv[1]
dirSaida = sys.argv[2]
quantImage = 80
imageSize = 800

diretorio = diretorio.replace("\\", "/")
dirSaida = dirSaida.replace("\\", "/")

if diretorio[-1] != "/":
    diretorio += "/"

if dirSaida[-1] != "/":
    dirSaida += "/"

valores = processGrayImages(diretorio, dirSaida, quantImage, (imageSize, imageSize))
txtJson = json.dumps(valores)
file = open("indices.json", "w")
file.write(txtJson)
file.close()