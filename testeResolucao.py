import cv2 as cv
import numpy as np

imagem = cv.imread("images/myke.jpg")
imagemSaida = None

size = (320,320)
print(np.shape(imagem))
imagem = cv.resize(imagem, size)
print(np.shape(imagem))
cv.imshow("a", imagem)
cv.waitKey(0)