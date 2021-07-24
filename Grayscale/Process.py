import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import jsons as json
import colorsys
from numpy.core.fromnumeric import shape, size
from os import listdir
import sys

class Imagem:
    def __init__(self, diretorioGray, valor, valorR, valorG, valorB, local):
        self.diretorioGray = diretorioGray
        self.valor = valor
        self.valorR = valorR
        self.valorG = valorG
        self.valorB = valorB
        self.diretorio = local

    def __str__(self):
        return f"({self.diretorioGray}, {self.valor}, {self.valorR}, {self.valorG},{self.valorB} {self.diretorio})"

class GrupoImagens:
    def __init__(self):
        self.imagens = []
        
    def adicionar(self, im):
        self.imagens.append(im)

    def __str__(self):
        text = ""
        for im in self.imagens:
            text += f"({im.diretorioGray}, {im.valor}, {im.valorR},{im.valorG},{im.valorB}, {im.diretorio})\n"
        return text

def processGrayImages(diretorio, dirSaida, tamanho):
    valores = GrupoImagens()

    listaDir = listdir(diretorio)

    for file in listaDir:
        imagem = cv.imread(diretorio + file)
        imagem = cv.resize(imagem, (tamanho, tamanho))
        cv.imwrite(dirSaida + "color_" + file, imagem)
        mediaBrutaRGB = cv.mean(imagem)
        imagemGray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        mediaBrutaCinza = cv.mean(imagemGray[0])
        valores.adicionar(Imagem(dirSaida + file, mediaBrutaCinza[0], int(mediaBrutaRGB[2]), int(mediaBrutaRGB[1]), int(mediaBrutaRGB[0]), dirSaida + "color_" + file))
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

valores = processGrayImages(diretorio, dirSaida, 800)
txtJson = json.dumps(valores)
file = open("indices.json", "w")
file.write(txtJson)
file.close()