# otimização de trnasformações geométricas

import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('Img4.jpg', 0)

img=img.astype('int')
im_res=np.zeros(img.shape)

a = len(img)
b = len(img[0])

a1=int(-a/2)
b1=int(-b/2)

graus=25
theta=(3.14/180)*graus #rad

x=np.tile(np.arange(0,a),b)
y=np.repeat(np.arange(0,b),a)

x1=np.floor((x+a1)*np.cos(theta)-(y+b1)*np.sin(theta)-a1).astype('int')
y1=np.floor((x+a1)*np.sin(theta)+(y+b1)*np.cos(theta)-b1).astype('int')

coor1 = np.array([x,y])
coor = np.array([x1,y1])

for i in range(len(x1)):
    if (coor[0,i] >= 0) and (coor[0,i] < a) and (coor[1,i] >= 0) and (coor[1,i] < b):
        im_res[coor1[0,i],coor1[1,i]]=img[coor[0,i],coor[1,i]]

print('foi')


im_final=im_res.astype('uint8')
cv2.imshow('Original1',im_final)

img=img.astype('uint8')
cv2.imshow('Original2',img)

cv2.waitKey(0)
cv2.destroyAllWindows()
