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

def processGrayImages(listaDiretorios):
    valores = GrupoImagens()
    for dir, file in zip(listaDiretorios, listaDiretorios):
        imagem = cv.imread("images\\" + file)
        imagemGray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
        valorBruto = cv.mean(imagemGray[0])
        valores.adicionar(Imagem("ImageGray/" + dir,valorBruto[0]))
        cv.imwrite("ImageGray/" + dir, cv.cvtColor(imagemGray, cv.COLOR_GRAY2BGR))
    valores.imagens.sort(key=lambda x: x.valor, reverse=False)
    return valores

def getGrayMeanValue(imagem):
    valorBruto = cv.mean(cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)[0])
    return valorBruto[0]

def mergeImages(imagem1, imagem2, eixo):
    return np.concatenate((imagem1, imagem2), eixo)

def getNearestImage(valor, listaJson):
    ini = 0
    fim = len(listaJson) - 1
    meio = 0

    while ini<=fim:
        meio = (ini + fim) // 2
        if listaJson[meio]['valor'] == valor:
            return cv.imread(listaJson[meio]['nome'])
        else:
            if valor < listaJson[meio]['valor']:
                fim = meio - 1
            else:
                ini = meio + 1

    return cv.imread(listaJson[meio]['nome'])

def photomosaic(imagem, listaJson, Rx, Ry, resolução=1):
    formato = shape(imagem)
    nx = formato[0]//Rx
    ny = formato[1]//Ry
    imagemFinal = None

    for y in range(Ry):
        imagemProv = None
        for x in range(Rx):
            valor = getGrayMeanValue(imagem[y*ny : (y+1)*ny, x*nx : (x+1) * nx])
            imagemSub = getNearestImage(valor, listaJson)
            dst = (shape(imagemSub)[0]//resolução, shape(imagemSub)[1]//resolução)
            imagemSub = cv.resize(imagemSub, dst)
            if imagemProv is None:
                imagemProv = imagemSub
                continue
            else:
                imagemProv = mergeImages(imagemProv, imagemSub, 1)
            
        if imagemFinal is  None:
            imagemFinal = imagemProv
            continue
        else:
            imagemFinal = mergeImages(imagemFinal, imagemProv, 0)

    return imagemFinal




imagemDir = "teste5.jpg"
imagem = cv.imread("testes/" + imagemDir)
file = open("indices.json", "r")
objJson = json.loads(file.read())
imagemFinal = photomosaic(imagem, objJson['imagens'], 100, 100, 128)
cv.imwrite("saidas/" + imagemDir, imagemFinal)


'''
listaDir = listdir('images')
valores = processGrayImages(listaDir)
txtJson = json.dumps(valores)
file = open("indices.json", "w")
file.write(txtJson)
file.close()
'''