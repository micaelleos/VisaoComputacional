#cálculo de projeção
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Img17.jpg',0)#Img10.jpg

img=img.astype('int')

img[img >= 127] = 255
img[img <= 127] = 0

a1,a2 = np.shape(img)

teta=-37*np.pi/180

x=np.zeros(a1)
y=np.zeros(a2)

for i in range(a1):
    for j in range(a2):
        if img[i,j] == 255:
            r=np.sqrt(i**2+j**2)
            alfa=np.arcsin(i/r)
            py=int(np.floor(r*np.sin(teta+alfa)))
            px=int(np.floor(r*np.cos(teta+alfa)))
            x[px]=1
            y[py]=1

t_x=np.count_nonzero(x == 1)
t_y=np.count_nonzero(y == 1)

print(t_x,t_y)

img=img.astype('uint8')
cv2.imshow('segmentada',img)

cv2.waitKey(0)
cv2.destroyAllWindows()