import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Img10.jpg',0)#Img10.jpg

img=img.astype('int')

img[img >= 127] = 255
img[img <= 127] = 0

a1,a2 = np.shape(img) # dimensões da imagem

masc = np.zeros([a1,a2]) # imagem de marcação de região
regiao=0
flag={} #para marcar pixels com regiões multiplas
x=0

for i in range(2,a1-1,1):
    for j in range(2,a2-1,1):
        if (img[i,j] == 255) and (masc[i,j] == 0) :  # ativo e não marcado
            vizi=masc[i-1:i+2,j-1:j+2]
            if any(vizi[vizi!=0]):
                #repete a região
                b=(img[i-1:i+2,j-1:j+2]) != 0 #mascara para associação de valores
                value_reg=(vizi[vizi!=0])
                masc[i-1:i+2,j-1:j+2] = b.astype('int')*value_reg[0]

            else:
                #ver ser em masc se vai acontecer multipla marcação
                vizi_16=masc[i-3:i+4,j-3:j+4]
                if any(vizi_16[vizi_16!=0]):
                    x= (vizi_16[vizi_16!=0])
                    x=x.astype('int')
                    flag[x[0]]=regiao+1

                regiao=regiao+1
                b=(img[i-1:i+2,j-1:j+2]) != 0
                masc[i-1:i+2,j-1:j+2] = b.astype('int')*regiao
                #região nova

#correção de multipla marcação
for x in flag:
    regiao= regiao - 1
    masc[masc==x]=flag[x]


#corrigir diferentes regiões conectadas
for i in range(2,a1-1,1):
    for j in range(2,a2-1,1):
        if (img[i,j] == 255):
            vizinhanca=masc[i-1:i+1,j-1:j+1] #procurar numa vizinhança de 8 pixels 
            valores=np.unique(vizinhanca) # numeração de região que não sejam únicos
            if (any(vizinhanca[vizinhanca!=0]) and (valores.shape[0]>2)) :#or (any(vizinhanca[vizinhanca==0]) and (valores.shape[0]>2))  : # concertar q tá errado, e quando tem 0,1,2 ?
                for k in range(1,valores.shape[0]-1):
                    masc[masc==valores[k]]= valores[k+1]


#organizar valores das regiões
values=np.unique(masc)
d=0
for l in values:
    masc[masc==l]=d
    d=d+1


print(np.unique(masc))
#exibição de regiões
a=np.unique(masc).shape[0]
#exibição de regiões
img_res=masc*(255/a)

'''img=img.astype('uint8')
cv2.imshow('Original',img)

img=imagem.astype('uint8')
cv2.imshow('segmentada',img)

cv2.waitKey(0)
cv2.destroyAllWindows()'''

label=np.unique(masc)
a=label.shape[0]
#exibição de regiões
img_res=masc*(255/a)
label=label
print(label)


