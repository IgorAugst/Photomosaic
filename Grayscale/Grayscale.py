import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape
from os import listdir

'''
imagem = cv.imread("images\cube.jpg")
gray = cv.cvtColor(imagem, cv.COLOR_BGR2GRAY)
gray = cv.cvtColor(gray,cv.COLOR_GRAY2RGB)

imagem = np.concatenate((imagem, gray), axis=1)
#cv.imshow("imagem",imagem)
plt.imshow(cv.cvtColor(imagem, cv.COLOR_BGR2RGB))
plt.show()
cv.waitKey(0)
'''

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
        




listaDir = listdir('images')
imagens = Converter(listaDir)
plt.imshow(cv.cvtColor(imagens, cv.COLOR_BGR2RGB))
plt.show()