import numpy as np
import cv2

Sobelx =(1/4)* np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
Sobely=(1/4)* np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

Laplaciano_3x3= np.array([[0, -1, 0], [-1, -4, -1], [0, -1, 0]])



Sx=Sobelx
Sy=Sobely

'''
imagem = np.zeros([600,700])

imagem[0:300,0:300] = 50
imagem[0:600,300:700] = 100
imagem[300:600,0:300] = 200
'''

imagem=cv2.imread('Img6.jpg',2)

imagem=imagem.astype('int')

a1,a2 = np.shape(imagem) # dimensões da imagem
b1,b2 = np.shape(Sx) #dimensões da máscara

im_resx = np.zeros([a1,a2])
im_resy = np.zeros([a1,a2])

#Convolução tipo varredura:

for i in range(a1):
    for p in range(a2):
        if i <= a1-b1 and p <= a2-b2 :
            im_resx[i,p]= np.sum([Sx[:,:]*imagem[i:i+b1,p:p+b2]])
            im_resy[i,p]= np.sum([Sy[:,:]*imagem[i:i+b1,p:p+b2]])

theta=abs(np.arctan2(im_resy,im_resx)*180/np.pi)

for i in range(a1):
    for p in range(a1):
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

im_res=abs(im_resx)+abs(im_resy)



for i in range(a1):
    for p in range(a2):
        if i+1<a1 and p+1<a2:
            if theta[i,p] == 0 or theta[i,p] == 360 :
                if im_res[i-1,p] < im_res[i,p]:
                    im_res[i-1,p] == 0
                if im_res[i+1,p] < im_res[i,p]:
                    im_res[i-1,p] = 0
                    
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
pix_forte=80
pix_fraco=20

for i in range(a1):
    for p in range(a2):
        if im_res[i,p]<=pix_fraco:
            im_res[i,p]=0
        elif im_res[i,p]>=pix_fraco and im_res[i,p]<=pix_forte:
            im_res[i,p]=pix_fraco
        else:
            im_res[i,p]=pix_forte





im_final=np.zeros([a1,a2])
a=np.empty([3,3])
pixel=0

for i in range(a1):
    for p in range(a2):
        if (i>2 & i+1<a1 & i-1 > 0) and (p>2 & p+2<a2 & p-1>0) is True:
            a=im_res[i-1:i+2,p-1:p+2]
            pixel = a.flat[np.abs(a-pix_forte).argmin()]
            if pixel == pix_forte is True:
                im_final[i,p] = 255

print(im_final)






                    


res_max=im_final.max()
#limiar=127
#im_res[im_res<127]=0
im_final=im_final*(255/res_max)
#im_resy=im_resy.astype('uint8')
im_final=im_final.astype('uint8')

#cv2.imshow('resultado1',im_resy)
#cv2.imshow('resultado2',im_res)
cv2.imshow('imagem',im_final)
cv2.waitKey() 
cv2.destroyAllWindows()

'''
im_res2=im_res.copy()
maximo=im_res.max()
im_res2[im_res2<=maximo-1]=0


im_res=im_res.astype('uint8')
im_res2=im_res2.astype('uint8')
imagem = imagem.astype('uint8')

cv2.imshow('imagem',imagem)
cv2.imshow('resultado',im_res)
cv2.imshow('resultado2',im_res2)
cv2.waitKey() 
cv2.destroyAllWindows()
'''


