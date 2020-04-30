#EQUALIZAÇÃO DE HISTOGRAMA

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('img3.jpg',0)


imagem=img.astype('int')

a= len(imagem)
b= len(imagem[0])
hist=np.zeros([255])
for i1 in range(255):
    hist[i1]=sum(sum(imagem==i1))

hist=hist/(a*b)
k=255
prob=np.zeros([k])
b=int(255/(k-1))

nivel_map=np.arange(0,k)/k

for i in range(0,k,1):
    prob[i]=np.sum(hist[i*b:b+i*b])+prob[i-1]

print(prob)

p=0



for l in range(img.shape[0]):
    for j in range(img.shape[1]):
        p=int(imagem[l,j]*k/255)-1
        idx = (np.abs(nivel_map-prob[p])).argmin()
        print(prob[p],nivel_map[idx])
        print(idx)
        imagem[l,j]=idx#prob[p]*imagem[l,j]


hist2=np.zeros([255])
for i in range(255):
    hist2[i]=sum(sum(imagem==i))

hist2=hist2/(a*b)


cdf=np.zeros([255])

for i in range(255):
    if i > 2:
        cdf[i]= cdf[i-1] + hist[i]

    
fig = plt.figure()
fig.canvas.set_window_title('Visão Computacional - CDF')
plt.title('Equalização')
plt.xlabel('Pixels')
plt.ylabel('Probabilidade Acumulada') 
plt.plot(cdf)
plt.show()


'''
fig = plt.figure()
fig.canvas.set_window_title('Visão Computacional - Histograma')
plt.title('Histograma')
plt.xlabel('Pixels')
plt.ylabel('Probabilidade')
plt.plot(hist2)
plt.plot(hist)
plt.show()
'''
cv2.imwrite('IMG5editada.jpg',imagem)
#----------EXIBIÇÃO--------------
img=img.astype('uint8')
cv2.imshow('Original',img)

imagem=imagem.astype('uint8')
cv2.imshow('Original2',imagem)

cv2.waitKey(0)
cv2.destroyAllWindows()

