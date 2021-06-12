import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import jsons as json
from numpy.core.fromnumeric import shape
from os import listdir

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

def Converter(listaDiretorios):
    i = 0
    imagens = []
    gray = []
    for file in listaDiretorios:
        imagens.append(cv.imread("images\\" + file))
        gray.append(cv.cvtColor(imagens[i], cv.COLOR_BGR2GRAY))
        gray[i] = cv.cvtColor(gray[i], cv.COLOR_GRAY2RGB)
        i += 1

    imSaida = np.concatenate((imagens.pop(0),gray.pop(0)), axis=1)
    for original, manip in zip(imagens, gray):
        imAux = np.concatenate((original, manip), axis=1)
        imSaida = np.concatenate((imSaida, imAux), axis=0)


    return imSaida

def getGrayMeanValues(listaDiretorios):
    valores = GrupoImagens()
    for dir, file in zip(listaDiretorios, listaDiretorios):
        imagem = cv.imread("images\\" + file)
        valorBruto = cv.mean(cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)[0])
        valores.adicionar(Imagem(dir,valorBruto[0]))

    return valores

listaDir = listdir('images')
valores = getGrayMeanValues(listaDir)
txtJson = json.dumps(valores)
print(txtJson)