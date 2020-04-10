''' Rascunho 2

LIMIARIZAÇÕES

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Img8.jpg',0)
img=img.astype('int')

a = len(img)
b = len(img[0])
print('a',a)
print('b',b)
'''# Limiarização Global
T=sum(sum(img))/(a*b)
print('T inicial',T)
M1=0
M2=0
dt=100
while dt > 0.5:
    print('erro',dt)
    m1=sum(sum(img<T))
    m2=sum(sum(img>T))
    M1=sum(img[img<T])/m1
    M2=sum(img[img>T])/m2
    T1=(M1+M2)/2
    dt=abs(T-T1)
    T=T1
print('erro final',dt)    
print('T final',T)    

mascara=img
mascara[mascara<T]=0
mascara[mascara>T]=255
'''        

# Limiarização de Otsu

hist=np.zeros([255])
for i in range(255):
    hist[i]=sum(sum(img==i))

hist=hist/(a*b)

mg=0
m=np.zeros([255])
P1=np.zeros([255])
var=np.zeros([255])
for i in range(254):
    mg=mg+(i+1)*hist[i+1]

for k in range(255):
    for i in range(k):
        P1[k]=P1[k]+hist[i]
    
    for i in range(k):
        m[k]=m[k]+(i+1)*hist[i+1]
    if k>2:
        var[k]=(mg*P1[k]-m[k])**2/(P1[k]*(1-P1[k]))

#print('var:',var[k])  
s,z = np.where([var==var.max()])
print(z)


fig = plt.figure()
fig.canvas.set_window_title('Visão Computacional - Histograma')
plt.title('Histograma')
plt.xlabel('Pixels')
plt.ylabel('Probabilidade')
plt.plot(hist)
fig2=plt.figure()
plt.plot(var)
plt.show()

T=z[0]
mascara=img
mascara[mascara<T]=0
mascara[mascara>T]=255

im_res=mascara.astype('uint8')
cv2.imshow('img_nova teste',im_res)
cv2.waitKey(0)
cv2.destroyAllWindows()

