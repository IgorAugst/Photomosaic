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

def processGrayImages(listaDiretorios, size):
    valores = GrupoImagens()
    for dir, file in zip(listaDiretorios, listaDiretorios):
        imagem = cv.imread("images\\" + file)
        imagemGray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        valorBruto = cv.mean(imagemGray[0])
        valores.adicionar(Imagem("ImageGray/" + dir,valorBruto[0]))
        imagemGray = cv.cvtColor(imagemGray, cv.COLOR_GRAY2BGR)
        imagemGray = cv.resize(imagemGray, size)
        cv.imwrite("ImageGray/" + dir, imagemGray)
    valores.imagens.sort(key=lambda x: x.valor, reverse=False)
    return valores


listaDir = listdir('images')
valores = processGrayImages(listaDir[0:80],(800,800))
txtJson = json.dumps(valores)
file = open("indices.json", "w")
file.write(txtJson)
file.close()