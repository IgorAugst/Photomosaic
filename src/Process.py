import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import jsons as json
import colorsys
from numpy.core.fromnumeric import shape, size
from os import listdir
import sys

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

def processImages(diretorio):
    valores = GrupoImagens()

    listaDir = listdir(diretorio)
    try:
        listaDir.remove("indices.json")
    except:
        pass 

    for file in listaDir:
        imagem = cv.imread(diretorio + file)
        mediaBrutaRGB = cv.mean(imagem)
        imagemGray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        mediaBrutaCinza = cv.mean(imagemGray[0])
        valores.adicionar(Imagem(mediaBrutaCinza[0], int(mediaBrutaRGB[2]), int(mediaBrutaRGB[1]), int(mediaBrutaRGB[0]), diretorio + file))
        imagemGray = cv.cvtColor(imagemGray, cv.COLOR_GRAY2BGR)
    valores.imagens.sort(key=lambda x: x.valor, reverse=False)
    return valores


diretorio = './images/'

if size(sys.argv) >= 2:
    diretorio = sys.argv[1]

diretorio = diretorio.replace("\\", "/")

if diretorio[-1] != "/":
    diretorio += "/"

valores = processImages(diretorio)
txtJson = json.dumps(valores)
file = open(diretorio + "indices.json", "w")
file.write(txtJson)
file.close()