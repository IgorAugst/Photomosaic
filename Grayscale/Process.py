import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import jsons as json
import colorsys
from numpy.core.fromnumeric import shape, size
from os import listdir
import sys

class Imagem:
    def __init__(self, nome, valor, valorH, local):
        self.nome = nome
        self.valor = valor
        self.valorInt = valorH
        self.diretorio = local

    def __str__(self):
        return f"({self.nome}, {self.valor}, {self.valorInt}, {self.diretorio})"

class GrupoImagens:
    def __init__(self):
        self.imagens = []
        
    def adicionar(self, im):
        self.imagens.append(im)

    def __str__(self):
        text = ""
        for im in self.imagens:
            text += f"({im.nome}, {im.valor}, {im.valorInt}, {im.diretorio})\n"
        return text

def processGrayImages(diretorio, dirSaida):
    valores = GrupoImagens()

    listaDir = listdir(diretorio)

    for file in listaDir:
        imagem = cv.imread(diretorio + file)
        mediaBrutaRGB = cv.mean(imagem)
        corInt = mediaBrutaRGB[2]*256**2 + mediaBrutaRGB[1]*256 + mediaBrutaRGB[0]
        imagemGray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        mediaBrutaCinza = cv.mean(imagemGray[0])
        valores.adicionar(Imagem(dirSaida + file, mediaBrutaCinza[0], int(corInt), diretorio + file))
        imagemGray = cv.cvtColor(imagemGray, cv.COLOR_GRAY2BGR)
        cv.imwrite(dirSaida + file, imagemGray)
    valores.imagens.sort(key=lambda x: x.valor, reverse=False)
    return valores


diretorio = './images/'
dirSaida = './ImagensProc/'

if size(sys.argv) >= 3:
    diretorio = sys.argv[1]
    dirSaida = sys.argv[2]

diretorio = diretorio.replace("\\", "/")
dirSaida = dirSaida.replace("\\", "/")

if diretorio[-1] != "/":
    diretorio += "/"

if dirSaida[-1] != "/":
    dirSaida += "/"

valores = processGrayImages(diretorio, dirSaida)
txtJson = json.dumps(valores)
file = open("indices.json", "w")
file.write(txtJson)
file.close()

valores.imagens.sort(key=lambda x: x.valorInt, reverse=False)
txtJson = json.dumps(valores)
file = open("indicesCor.json", "w")
file.write(txtJson)
file.close()