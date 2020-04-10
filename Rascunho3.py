'''Rasunho3'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('Img7.jpg',0)


img[img > 127] = 255
img[img <= 127] = 0

#print(len(img))

elm=np.ones([11,11])
ref=np.array([6,6])

img_res=np.zeros(img.shape)
#img_res[:,:]=255

img_res2=np.zeros(img.shape)

pixel=1


#dilatação e erosão

for i in range(img.shape[0]): #
    for j in range(img.shape[1]):#

        #if img[i,j]==0:
            for x in range(ref[0]-elm.shape[0],elm.shape[0]-ref[0],1):
                for y in range(ref[1]-elm.shape[1],elm.shape[1]-ref[1],1):

                    if img[i,j]==255:
                        if elm[x+ref[0],y+ref[1]]==1:
                            if i-x >= 0 and j-y >= 0 and i-x <= img.shape[0] and j-y <= img.shape[1]:
                                img_res[i-x-1,j-y-1]=255

'''bloco=np.array([])

for i in range(1,img.shape[0],2*pixel):
    for j in range(1,img.shape[1],2*pixel):
        bloco=img[i-pixel:i+pixel,j-pixel:j+pixel]

        if bloco.all():
            
            for x in range(ref[0]-elm.shape[0],elm.shape[0]-ref[0],1):
                for y in range(ref[1]-elm.shape[1],elm.shape[1]-ref[1],1):

                    if elm[x+ref[0],y+ref[1]]==1:
                        if i-x >= 0 and j-y >= 0 and i-x <= img.shape[0] and j-y <= img.shape[1]:
                            img_res[i-x-1,j-y-1]=255'''
                    


#----------EXIBIÇÃO--------------
img=img.astype('uint8')
cv2.imshow('Original',img)

img_res=img_res.astype('uint8')
cv2.imshow('Dilatada',img_res)


cv2.waitKey(0)
cv2.destroyAllWindows()
