import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('img4.jpg',0)

mascara=np.array([[0,-1,0],
                    [-1,4,-1],
                    [0,-1,0]])

img=img.astype('int')


b1,b2 = np.shape(mascara) #dimensões da máscara
a1,a2 = np.shape(img) # dimensões da imagem

imagem = np.zeros([a1,a2])

#Convolução tipo varredura:

for i in range(a1):
    for p in range(a2):
        if i <= a1-b1 and p <= a2-b2 :
            imagem[i,p]= np.sum([mascara[:,:]*img[i:i+b1,p:p+b2]])


a=imagem.max()
b=imagem.min()

im = (imagem - b)*(255/(a-b+1)) -127

im_res=img-im

im_res[im_res > 255] = 255
im_res[im_res < 0] = 0

# tenho que fazer a inerpolação ainda


imagem=im_res.astype('uint8')
cv2.imshow('Original2',imagem)

img=img.astype('uint8')
cv2.imshow('Original1',img)

cv2.waitKey(0)
cv2.destroyAllWindows()