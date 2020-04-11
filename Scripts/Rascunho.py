""" Rascunho de processamento de Imagens"""

import cv2
import numpy as np
import matplotlib.pyplot as plt



img = cv2.imread('Img3.jpg',0)
img=img.astype('int')
im1=np.zeros([500,500])

im1[0:250,0:250]=100
im1[251:500,0:250]=50
im1[0:250,251:500]=200
im1[251:500,251:500]=250


im1[0:2,0:2]=100
im1[2:5,0:2]=50
im1[0:2,2:5]=200
im1[2:5,2:5]=250

im_nova = np.zeros(np.shape(im1))
im_aux = np.zeros(np.shape(im1))
im_res=np.zeros(np.shape(im1))


a = len(im1)
b = len(im1[0])
'''
#======================================Translação==============================
#     MÉTODO1

a1 = 200
b1 =200


for j in range(b):
   if j+b1 <= b:
       im_aux[:,j] = im1[:,j+b1-1]
   if j+b1 <=0:
      im_aux[:,j] = 0
      
for i in range(a):
   if i+a1 <= a:
      im_res[i,:] = im_aux[i+a1-1,:]
   if i+a1 <=0:
      im_res[i,:] = 0
 '''
#  Método 2
'''
a1 =200
b1 =200

for i in range(a):
   for j in range(b):
      x=i+a1
      y=j+b1
      if x<a and y<b:
        im_res[x,y] = im1[i,j]
      if x<=0 or y<=0:
         im_res[i,j] = 0
    


#======================================Escalonamento===========================

sx=10
sy=0.6
 #     MÉTODO 1
for j in range(b):
   if j*sy <= b:
       im_aux[:,j] = im1[:,j*sy-1]
   if j*sy <=0:
      im_aux[:,j] = 0
      
for i in range(a):
   if i*sx <= a:
      im_nova[i,:] = im_aux[i*sx-1,:]
   if i*sx <=0:
      im_nova[i,:] = 0

'''
'''
 #Método 2
#Escalonamento em relação ao centro da imagem, ou ponto qualquer
p1=a
p2=b

a1 = int(-p1/2+p1/(2*sx))
b1 = int(-p2/2+p2/(sy*2))

for i in range(a-1):
   for j in range(b-1):
      x=(i+a1)*sx
      y=(j+b1)*sy
      if -a<x<a and -b<y<b:
         im_res[i,j] = im1[int(x),int(y)]
      if x<=0 or y<=0:
         im_res[i,j] = 0
'''

#===========================================rotação===========================

'''      MÉTODO 1

x=0
y=0
graus=5
theta=(3.14/180)*graus #rad

for j in range(b):
   for i in range(a):
      x= i*np.cos(theta)-j*np.sin(theta)
      y= i*np.sin(theta)+j*np.cos(theta)
      if x<a and y<b:
        im_res[i,j]= im1[int(np.floor(x)),int(np.floor(y))]
      if x<=0 or y<=0:
         im_res[i,j] = 0

 # Método 2
sx=1
sy=1

p1=a #coordenada de rotação para o eixo x
p2=b #coordenada de rotação para o eixo y

a1 = int(-p1/(2*sx))
b1 = int(-p2/(sy*2))
#a1=0
#b1=0

x=0
y=0
graus=30
theta=(3.14/180)*graus #rad

for j in range(b):
   for i in range(a):
      x= (i+a1)*np.cos(theta)-(j+b1)*np.sin(theta)-a1
      y= (i+a1)*np.sin(theta)+(j+b1)*np.cos(theta)-b1
      if -a<x<a and -b<y<b:
        im_res[i,j]= im1[int(np.floor(x)),int(np.floor(y))]
      if x<=0 or y<=0:
         im_res[i,j] = 0


#======================================Detecção de Borda===============================================================================================================

img=img.astype('int')

a1=len(img)  #largura
a2=len(img[0])  #altura

Dx = np.empty((a1, a2))
Dx = Dx.astype(int)

Dy = np.empty((a1, a2))
Dy = Dy.astype(int)



for i in range(a1-1):
   for p in range(a2-1):
      if p+1<=a2:
         Dx[i, p] = img[i, p] - img[i, p + 1]


for p in range(a2-1):
   for i in range(a1-1):
      if i+1<=a1:
         Dy[i, p] = img[i, p] - img[i+1, p]


M = np.sqrt(Dx ** 2 + Dy ** 2)


M_max = M.max()

M[M<M_max/4]=0


M1 = M * (255 / M_max)

im_res = M1
'''

hist=np.zeros([255])
for i in range(255):
   hist[i]=sum(sum(img==i))

n=a*b

hist=hist/n
a=sum(hist)
print(a)
plt.plot(hist)
plt.show()

#===================================Visualizar Imagens===========================         
#im_aux=im_aux.astype('uint8')
im_res=im_res.astype('uint8')
#im1=im1.astype('uint8')
#cv2.imshow('img1 teste',im1)
#cv2.imshow('img_aux teste',im_aux)
cv2.imshow('img_nova teste',im_res)
cv2.waitKey(0)
cv2.destroyAllWindows()











