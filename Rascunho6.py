#Detector de borda de Canny

import cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st


def convolucao(mascara,img):
    imagem=img
        
    a1,a2 = np.shape(imagem) # dimensões da imagem
    b1,b2 = np.shape(mascara) #dimensões da máscara

    im_res_masc = np.zeros([a1,a2])

    #Convolução tipo varredura:

    for i in range(a1):
        for p in range(a2):
            if i <= a1-b1 and p <= a2-b2 :
                im_res_masc[i,p]= np.sum([mascara[:,:]*imagem[i:i+b1,p:p+b2]])

    return im_res_masc



def Gaussiano(tam,sig,img):

    intervalo = (2*sig+1.)/(tam)
    x = np.linspace(-sig-intervalo/2., sig+intervalo/2., tam+1)
    kern1d = np.diff(st.norm.cdf(x))
    kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
    mascara = kernel_raw/kernel_raw.sum()
    
    im_res=convolucao(mascara,img)
    return im_res

def Sobel(img):
    #Detecção de borda Sobel
    Sx=(1/4)*np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    Sy=(1/4)*np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

    resx = convolucao(Sx,img)
    resy = convolucao(Sy,img)

    theta=abs(np.arctan2(resy,resx)*180/np.pi)
    
    im_res = abs(resx)+abs(resy)

    res_max=im_res.max()
    limiar=30
    #im_res[im_res<limiar]=0
    im_res=im_res*(255/res_max)

    return im_res, theta


img = cv2.imread('img4.jpg',0).astype('int')

a1,a2 = np.shape(img)
        
img = Gaussiano(5,1.4,img)

im_res,theta = Sobel(img)

for i in range(a1):
    for p in range(a2):
        if 0<theta[i,p] and theta[i,p]<=22 :
            theta[i,p] = 0
        if 22<theta[i,p] and theta[i,p]<=67 :
            theta[i,p] = 45
        if 67<theta[i,p] and theta[i,p]<=112 :
            theta[i,p] = 90
        if 112<theta[i,p] and theta[i,p]<=157 :
            theta[i,p] = 135
        if 157<theta[i,p] and theta[i,p]<=202 :
            theta[i,p] = 180
        if 202<theta[i,p] and theta[i,p]<=247 :
            theta[i,p] = 225
        if 247<theta[i,p] and theta[i,p]<=292 :
            theta[i,p] = 270
        if 292<theta[i,p] and theta[i,p]<=337 :
            theta[i,p] = 315
        if 337<theta[i,p] and theta[i,p]<=360 :
            theta[i,p] = 360

for i in range(a1):
    for p in range(a2):
        if i+1<a1 and p+1<a2:
            if theta[i,p] == 0 or theta[i,p] == 360 or theta[i,p] == 180 :
                if im_res[i-1,p] < im_res[i,p]:
                    im_res[i-1,p] = 0
                if im_res[i+1,p] < im_res[i,p]:
                    im_res[i+1,p] = 0
                    
            if theta[i,p]==45 or theta[i,p]==225:
                if im_res[i-1,p+1] < im_res[i,p]:
                    im_res[i-1,p+1] = 0
                if im_res[i+1,p-1] < im_res[i,p]:
                    im_res[i+1,p-1] = 0

            if theta[i,p]==90 or theta[i,p]==270:
                if im_res[i,p-1] < im_res[i,p]:
                    im_res[i,p-1] = 0
                if im_res[i,p+1] < im_res[i,p]:
                    im_res[i,p+1] = 0

            if theta[i,p]==135 or theta[i,p]==315:
                if im_res[i-1,p-1] < im_res[i,p]:
                    im_res[i-1,p-1] = 0
                if im_res[i+1,p+1] < im_res[i,p]:
                    im_res[i+1,p+1] = 0
pix_forte=80#80
pix_fraco=20#20

for i in range(a1):
    for p in range(a2):
        if im_res[i,p]<=pix_fraco:
            im_res[i,p]=0
        elif im_res[i,p]>=pix_fraco and im_res[i,p]<=pix_forte:
            im_res[i,p]=pix_fraco
        else:
            im_res[i,p]=pix_forte

im_final=np.zeros([a1,a2])
a=0
pixel=0

n = im_res==80

m=n.any()

print(m)

for i in range(1,a1-2):
    for p in range(1,a2-2):
        a=im_res[i-1:i+2,p-1:p+2]
        #print(a)
        b1 = a == 80 #a.flat[np.abs(a-pix_forte).argmin()]
        b2 = b1.any()
        
        if b2 is True:
            im_final[i,p] = 255
            #print(im_final[i,p])

im_final=im_final.astype('uint8')
cv2.imshow('Original1',im_final)

im_res=im_res.astype('uint8')
cv2.imshow('Original2',im_res)


cv2.waitKey(0)
cv2.destroyAllWindows()