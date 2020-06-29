import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Img14.jpg',0)#Img10.jpg

img=img.astype('int')

img[img > 127] = 255
img[img < 127] = 0

#img=np.zeros([100,100])
#img[25:75,25:75]=255

a1,a2 = np.shape(img) # dimensões da imagem

masc = np.zeros([a1,a2]) # imagem de marcação de região
regiao=0
flag={} #para marcar pixels com regiões multiplas


for i in range(2,a1-1,1):
    for j in range(2,a2-1,1):
        if (img[i,j] == 255) : #and masc[i,j] == 0
            if (img[i,j-1] == 0) and (img[i-1,j] == 0) and (img[i-1,j-1] == 0) :#and (img[i+1,j-1] == 0):
                if (masc[i,j]!= 0) or (masc[i+1,j]!= 0) or (masc[i,j+1]!= 0) or (masc[i,j-1]!= 0) or (masc[i-1,j]!= 0) or (masc[i-1,j-1]!= 0) or (masc[i-1,j+1]!= 0) :
                #if (masc[i+1,j] != 0) or (masc[i,j+1] != 0) :
                    flag[regiao] = regiao + 1
                    print(flag)
                regiao=regiao + 1
                test2=masc[i,j]
                test=[img[i,j],img[i-1,j],img[i,j-1]]
                masc[i,j] = regiao
                masc[i+1,j] = regiao
                masc[i,j+1] = regiao
                masc[i+1,j+1] = regiao
                #masc[i+1,j-1] = regiao

            if img[i-1,j-1] != 0 :
                masc[i,j] = masc[i-1,j-1]
                masc[i+1,j] = masc[i-1,j-1]
                masc[i,j+1] = masc[i-1,j-1]
                masc[i+1,j+1] = masc[i-1,j-1]
                #masc[i+1,j-1] = masc[i-1,j-1]
            if img[i-1,j+1] != 0 :
                masc[i,j] = masc[i-1,j+1]
                masc[i+1,j] = masc[i-1,j+1]
                masc[i,j+1] = masc[i-1,j+1]
                masc[i+1,j+1] = masc[i-1,j+1]       
                #masc[i+1,j-1] = masc[i-1,j+1]   
            if img[i-1,j] != 0 :
                masc[i,j] = masc[i-1,j]
                masc[i+1,j] = masc[i-1,j]
                masc[i,j+1] = masc[i-1,j]
                masc[i+1,j+1] = masc[i-1,j]
                #masc[i+1,j-1] = masc[i-1,j]
            if img[i,j-1] != 0 :
                masc[i,j] = masc[i,j-1]
                masc[i+1,j] = masc[i,j-1]
                masc[i,j+1] = masc[i,j-1]
                masc[i+1,j+1] = masc[i,j-1]
                #masc[i+1,j-1] = masc[i,j-1]                
            

            
            #imagem[i,p]= np.sum([mascara[:,:]*img[i:i+b1,p:p+b2]])

cont={}
for x in flag:
    masc[masc==flag[x]]=x

reg={}
d=0
for k in range(regiao):
    cont[k]=np.count_nonzero(masc == k)
    if cont[k] < 0.01*a1*a2:
        masc[masc == k] = 0
    else:
        reg[d]=cont[k]
        d=d+1

print('reg:',reg)
print('cont:',cont)

#print(flag)
#print(masc)

imagem = masc*255


a=imagem.max()
b=imagem.min()

#imagem = (imagem/a)*255

img=img.astype('uint8')
cv2.imshow('Original',img)

img=imagem.astype('uint8')
cv2.imshow('segmentada',img)

cv2.waitKey(0)
cv2.destroyAllWindows()


