# otimização de trnasformações geométricas

import cv2
import numpy as np
import matplotlib.pyplot as plt


img = cv2.imread('img4.jpg',0).astype('int')

im1 = img

im_res = np.zeros(np.shape(im1))

a = len(im1)
b = len(im1[0])


a1 = int(-px)
b1 = int(-py)


x=0
y=0

graus=-angulo
theta=(3.14/180)*graus #rad

x=np.arange(0,a)
y=np.arange(0,b)

coor=[x,y]



'''for j in range(b):
    for i in range(a):
        x= (i+a1)*np.cos(theta)-(j+b1)*np.sin(theta)-a1
        y= (i+a1)*np.sin(theta)+(j+b1)*np.cos(theta)-b1
        if -a<x<a and -b<y<b:
            im_res[i,j]= im1[int(np.floor(x)),int(np.floor(y))]
        if x<=0 or y<=0:
            im_res[i,j] = 0'''


im_final=im_final.astype('uint8')
cv2.imshow('Original1',im_final)

im_res=im_res.astype('uint8')
cv2.imshow('Original2',im_res)


cv2.waitKey(0)
cv2.destroyAllWindows()
