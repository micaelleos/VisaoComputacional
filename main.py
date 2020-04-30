"""
Criado por : Micaelle Oliveira de Souza
Disciplina : Visão Computacional
2018.1

"""
import sys
import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

from dialogos import *
from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QFileDialog, QMessageBox, QLineEdit, QDialog, QCheckBox
from PyQt5.QtGui import QPixmap, QImage, qRgb, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSlot      
        
class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        loadUi('Interfaces/Interface.ui',self )
        self.setWindowTitle('Visão Computacional')
        self.setWindowIcon(QIcon('Icone.png'))
        self.menubar.setNativeMenuBar(False)
        self.im1 = None
        self.im2 = None
        self.im_res = None
        self.im_aux = None
        self.op_slider = 0 # Constanete que varia dependendo que quem está usando o valor do vertical slider.
        self.n = 1 # n sei o que é
        self.hist=np.zeros([255]) # histograma
        self.verticalSlider.valueChanged.connect(self.atualizar_lim)
        self.Button_abrirIm1.clicked.connect(self.abrir_imagem_1)
        self.Button_abrirIm2.clicked.connect(self.abrir_imagem_2)
        self.Button_Usar_Resultado.clicked.connect(self.usar_res)
        self.Button_switch.clicked.connect(self.switch)
        


        
        #Funções do menu
        self.actionAbrir_Imagem_1.triggered.connect(self.abrir_imagem_1)
        self.actionAbrir_Imagem_2.triggered.connect(self.abrir_imagem_2)
        self.actionSalvar_Resultado.triggered.connect(self.salvar)
        self.actionSair.triggered.connect(self.fechar)
        #Converter
        self.actionTons_de_Cinza.triggered.connect(self.tons_de_cinza)
        self.actionR.triggered.connect(self.conversaoR)
        self.actionG.triggered.connect(self.conversaoG)
        self.actionB.triggered.connect(self.conversaoB)
        self.actionBin_rio.triggered.connect(self.binario)
        #Operação
        self.actionOpera_o_por_escalar.triggered.connect(self.abrirDialog5)
        self.actionSoma.triggered.connect(self.Op_soma)
        self.actionSubtra_o.triggered.connect(self.Op_subtracao)
        self.actionMult.triggered.connect(self.Op_multiplicacao)
        self.actionDivisao.triggered.connect(self.Op_divisao)
        self.actionAnd.triggered.connect(self.Op_and)
        self.actionOr.triggered.connect(self.Op_or)
        self.actionNot.triggered.connect(self.Op_not)
        self.actionXor.triggered.connect(self.Op_xor)
        #Transformação
        self.actionEscalonamento.triggered.connect(self.abrirDialog1)
        self.actionTransla_o.triggered.connect(self.abrirDialog2)
        self.actionRota_o.triggered.connect(self.abrirDialog3)
        #Detecção de borda
        self.actionPrimeira_Ordem_2.triggered.connect(self.Ordem1)
        self.actionSegunda_Ordem_2.triggered.connect(self.Ordem2)
        self.actionSobel.triggered.connect(self.Sobel)
        self.action3x3.triggered.connect(self.Laplaciano3x3)
        self.action5x5.triggered.connect(self.Laplaciano5x5)
        self.action9x9.triggered.connect(self.Laplaciano9x9)
        self.actionKirsch.triggered.connect(self.Kirsch)
        self.actionCanny.triggered.connect(self.Canny)
        #filtros
        self.actionGaussiano.triggered.connect(self.abrirDialog4)
        self.actionM_dia.triggered.connect(self.media)
        self.actionMediana.triggered.connect(self.mediana)
        self.actionPassa_Alta.triggered.connect(self.passaAlta)
        #Histogramas
        self.actionHistogramas.triggered.connect(self.Histo)
        self.actionCalculo_de_CDF.triggered.connect(self.cdf)
        self.actionAuto_Escala.triggered.connect(self.Auto)
        self.actionEqualiza_o.triggered.connect(self.Equaliza)
        self.actionLimiariza_oGlobal.triggered.connect(self.Global)
        self.actionLimiariza_o_Otsu.triggered.connect(self.Otsu)
        #morfologia
        self.actionPersonalizado.triggered.connect(self.morfoPersonalizado)
        self.actionDilata_o.triggered.connect(self.morfoDilatacao)
        self.actionEros_o.triggered.connect(self.morfoErosao)
        self.actionAbertura.triggered.connect(self.morfoAbertura)
        self.actionFechamento.triggered.connect(self.morfoFechamento)
        


    def Ordem2(self):
        self.n=2
        self.B_derivativo()
    def Ordem1(self):
        self.n=1
        self.B_derivativo()
        
    def abrir_imagem_1(self):
        print('abrir imagem')

        filename = QFileDialog.getOpenFileName(self)
        if filename[0] is not '':
            self.im1 = cv2.imread(filename[0]) #abre e salva a imagem em self.orig
            self.atualizarIm('im1') 
            
    def abrir_imagem_2(self):
        filename = QFileDialog.getOpenFileName(self)
        if filename[0] is not '': 
            self.im2 = cv2.imread(filename[0]) #abre e salva a imagem em self.orig
            self.atualizarIm('im2')
        
    def usar_res(self): #Atualiza a imagem im1 com a imagem resultado.
        if self.im_res is None:
            QMessageBox.about(self,"Erro", "Imagem resultado não encontrado.")
        else:
            self.op_slider = 0
            self.im1 = self.im_res.copy()
            self.atualizarIm('im1')

    def switch(self): # Faz o switch entre as imagens im1 e im2 para facilitar operações.
        if self.im2 is None:
            self.im2 = self.im1.copy()
            self.atualizarIm('im2')
        if self.im1 is None:
            self.im1 = self.im2.copy()
            self.atualizarIm('im1')
        if self.im1 is not None and self.im2 is not None:
            im = self.im1.copy()
            self.im1 = self.im2.copy()
            self.im2 = im
            self.atualizarIm('im1')
            self.atualizarIm('im2')

    def fechar(self): # fecha programa
        sys.exit()

    def salvar(self): # salva a imagem im1.
        filename = QFileDialog.getSaveFileName(self)
        cv2.imwrite(filename[0],self.im_res)

    def atualizarIm(self,tipo):
        #tipo 1: imagem original, senão é a processada
        if tipo == 'im1':
            im = self.im1
            label = self.label_1
        elif tipo == 'im_res':
            im = self.im_res
            label = self.label_3
        elif tipo == 'im2':
            im = self.im2
            label = self.label_2
        else: 
            im = self.im_aux
            label = self.label_4
        #pega os canais e dimensões
        
        if len(im.shape) == 3:
            b,g,r = cv2.split(im) #BGR no openCV
            #cria uma QImage com os canais RGB
            qim = QImage(cv2.merge((r,g,b)), im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
        else:
            qim = QImage(im, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
            qim.setColorTable([qRgb(i,i,i) for i in range(256)])
        #cria um Pixmap a partir do QImage
        pixmap = QPixmap.fromImage(qim)
        #redimensiona o pixmap pra o tamanho do label
        pixmap = pixmap.scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        #atualiza o label
        label.setPixmap(pixmap)

    def tons_de_cinza(self): # função de conversão para tons de cinza.
        print("Tons de cinza")
        if self.im1 is None:
             self.abrir_imagem_1(self)
        else:
            self.im_res = self.im1.copy()
            if len(self.im_res.shape) == 3:
                imagem = cv2.cvtColor(self.im_res, cv2.COLOR_BGR2GRAY)
                #Comentário: O usa da equação abaixo causa uma grande variância no histograma, causando erro nas limiarizações.
                #imagem =  self.im_res[:,:,0]*0.114 + self.im_res[:,:,1]*0.587 + self.im_res[:,:,2]*0.299
                self.im_res = imagem.astype('uint8')
                self.atualizarIm('im_res')
            else:
                QMessageBox.about(self,"Aviso", "A imagem já está em tons de cinza.")

    def conversaoR(self):
        print("conversão R")
        if self.im1 is None:
             self.abrir_imagem_1(self)
        else:
            self.im_res = self.im1.copy()
            if len(self.im_res.shape) == 3:
                imagem = self.im_res[:,:,0]
                self.im_res = imagem.astype('uint8')
                self.atualizarIm('im_res')
            else:
                QMessageBox.about(self,"Aviso", "A imagem já está em tons de cinza.")

    def conversaoG(self):
        print('Connversão G')
        if self.im1 is None:
             self.abrir_imagem_1(self)
        else:
            self.im_res = self.im1.copy()
            if len(self.im_res.shape) == 3:
                imagem = self.im_res[:,:,1]
                self.im_res = imagem.astype('uint8')
                self.atualizarIm('im_res')
            else:
                QMessageBox.about(self,"Aviso", "A imagem já está em tons de cinza.")

    def conversaoB(self):
        print('conversãoB')

        if self.im1 is None:
             self.abrir_imagem_1(self)
        else:
            self.im_res = self.im1.copy()
            if len(self.im_res.shape) == 3:
                imagem = self.im_res[:,:,2]
                self.im_res = imagem.astype('uint8')
                self.atualizarIm('im_res')
            else:
                QMessageBox.about(self,"Aviso", "A imagem já está em tons de cinza.")


    def binario(self):

        if self.im1 is None: # se não tem imagem im1, abre e converte para tons de cinza.
            self.abrir_imagem_1()
            self.tons_de_cinza()
        if len(self.im1.shape) == 3: # se tiver 3 canais converte para tons de cinza e um canal.
            self.tons_de_cinza()
            self.usar_res()
        self.op_slider = 3 # atulaiza os valores di verticla slider para esta operação.
        limiar = self.verticalSlider.value()

        self.im_res[self.im1 > limiar] = 255
        self.im_res[self.im1 <= limiar] = 0

        self.im_res = self.im_res.astype('uint8')
        self.atualizarIm('im_res')

    def Opera_o_por_escalar(self,tipo,escalar):
        
        self.im_res=None
        
        if tipo == "soma":
            self.im_res = self.im1.astype('int') + escalar
            

        if tipo == "subtração":
            self.im_res = self.im1.astype('int') - escalar

        
        self.im_res[self.im_res > 255] = 255
        self.im_res[self.im_res < 0] = 0


        self.im_res = self.im_res.astype('uint8')
        self.atualizarIm('im_res')


    def abrirDialog5(self):
        if self.im1 is None:
            self.abrir_imagem_1()
        if len(self.im1.shape) == 3: #se tem 3 canais converte para 1 canal
            self.tons_de_cinza()
            self.im1 = self.im_res.copy()
            self.atualizarIm('im1')
            
            
        dialogo = Dialogo5()
        dialogo.setWindowTitle('Operação por Escalar')
        dialogo.exec_()

        escalar = int(dialogo.lineEdit.text())

        if dialogo.cancelou == 0:
            if dialogo.radioButton.isChecked() == True:
                self.Opera_o_por_escalar("soma",escalar)
                
            if dialogo.radioButton_2.isChecked() == True:
                self.Opera_o_por_escalar("subtração",escalar)
            
           
        
        
    def Op_soma(self):
        print('op soma')
        if self.im1 is None: # se não tem imagem, abre.
            self.abrir_imagem_1()
        if self.im2 is None:
            self.abrir_imagem_2()
        if len(self.im1.shape) == 3: #se tem 3 canais converte para 1 canal
            self.tons_de_cinza()
        if len(self.im2.shape) == 3:
              QMessageBox.about(self,"Erro", "Converta imagem 2 em tons de cinza.") # caso a imagem im2 não estiver em tons de cinza, o usuário é avisado.
        if self.im1.shape == self.im2.shape :
            self.im_res = self.im1 + self.im2

            a=self.im_res.max()
            self.im_res = 255*(self.im_res/a)
        
            self.im_res = self.im_res.astype('uint8')
            self.atualizarIm('im_res')
        else:
            QMessageBox.about(self,"Erro","As duas imagens devem ser do mesmo tamanho para esta operação.")
        
    def Op_subtracao(self):
        print('op sub')

        if self.im1 is None:
            self.abrir_imagem_1()
        if self.im2 is None:
            self.abrir_imagem_2()
        if len(self.im1.shape) == 3:
            self.tons_de_cinza()
        if len(self.im2.shape) == 3:
              QMessageBox.about(self,"Erro", "Converta imagem 2 em tons de cinza.")
        else:
            im1=self.im1.astype('int')
            im2= self.im2.astype('int')
            self.im_res = im1 - im2
            
            a=self.im_res.max()
            #self.im_res = 255*(self.im_res/a)
            b=self.im_res.min()
            self.im_res = 255*(self.im_res/a - self.im_res/b)
            
            self.im_res = self.im_res.astype('uint8')
            self.atualizarIm('im_res')

    def atualizar_lim(self):
        #Cada valor guardado na variável op_slider direciona-se para uma função : multiplicação, divisão ou binário.
        if self.im1 is not None:
            if self.op_slider == 1:# -> Multiplicação
                self.label_limiar.setText(str(float(self.verticalSlider.value()/255)))
                self.Op_multiplicacao()
            elif self.op_slider == 2:# -> Divisão
                self.label_limiar.setText(str(float(self.verticalSlider.value()/255)))
                self.Op_divisao()
            elif self.op_slider == 3:# -> Binário
                if len(self.im1.shape) != 3:
                    self.label_limiar.setText(str(self.verticalSlider.value()))
                    self.binario()
                else:
                    self.tons_de_cinza()
                    self.atualizar_lim()
            elif self.op_slider == 4:  # -> euqalização, define quantidade de níveis de cinza
                self.label_limiar.setText(str(self.verticalSlider.value()))
                self.Equaliza()
        
    def Op_multiplicacao(self):
        if self.im1 is None: # Se não tem imagem im1, abre.
            self.abrir_imagem_1()

        #Slider está executando a função multiplicação
        self.op_slider=1

        #Pega o valor do vertical slider.
        limiar2 = self.verticalSlider.value()

        #normaliza o valor do limiar para 0 a 2
        limiar2 = limiar2*2/255

        #if limiar2 >= 1:
        
        im=np.array(self.im1)
        self.im_res = im*limiar2+self.im1
        
        '''if limiar2 < 1:
            im=self.im1
            self.im_res = im*limiar2'''

        #Truncamento
        self.im_res[self.im_res > 255] = 255
        
        self.im_res = self.im_res.astype('uint8')
        self.atualizarIm('im_res')
          
    def Op_divisao(self):
        if self.im1 is None:
            self.abrir_imagem_1()
            
        #Slider está executando a função divisão
        self.op_slider = 2

        limiar2 = self.verticalSlider.value()

        #normaliza o valor do limiar para 0 a 2
        limiar2 = limiar2/255

        im=self.im1
        self.im_res = im*limiar2

        #Truncamento
        self.im_res[self.im_res > 255] = 255
        
        self.im_res = self.im_res.astype('uint8')
        self.atualizarIm('im_res')
          
    def Op_and(self):
        print('op and')

        #Se não tem imagem im1, abre.
        if self.im1 is None:
            self.abrir_imagem_1()
        #Se não tem imagem im2, abre.
        if self.im2 is None:
            self.abrir_imagem_2()
        #Se im1 tem 3 canais, converte pra tons de cinza.
        if len(self.im1.shape) == 3:
            self.tons_de_cinza()
        #Se im2 tem 3 canais, avisa para o usuário.
        if len(self.im2.shape) == 3:
              QMessageBox.about(self,"Erro", "Converta imagem 2 em tons de cinza.")
        else:
            self.im_res = self.im1 & self.im2    
            self.im_res = self.im_res.astype('uint8')
            self.atualizarIm('im_res')

    def Op_or(self):
        print('op or')

        #Se não tem imagem im1, abre.
        if self.im1 is None:
            self.abrir_imagem_1()
        #Se não tem imagem im2, abre.
        if self.im2 is None:
            self.abrir_imagem_2()
        #Se im1 tem 3 canais, converte pra tons de cinza.
        if len(self.im1.shape) == 3:
            self.tons_de_cinza()
        #Se im2 tem 3 canais, avisa para o usuário.
        if len(self.im2.shape) == 3:
              QMessageBox.about(self,"Erro", "Converta imagem 2 em tons de cinza.")
        else:
            self.im_res = self.im1 | self.im2
        
            self.im_res = self.im_res.astype('uint8')
            self.atualizarIm('im_res')

    def Op_not(self):
        print('op not')

        #Se não tem imagem im1, abre.
        if self.im1 is None:
            self.abrir_imagem_1()
        #Se não tem imagem im2, abre.
        if len(self.im1.shape) == 3:
            self.tons_de_cinza()
            self.binario()
            self.Op_not()
        else:
            self.im_res = cv2.bitwise_not(self.im1) 
        
            self.im_res = self.im_res.astype('uint8')
            self.atualizarIm('im_res')

    def Op_xor(self):
        print('op xor')

        #Se não tem imagem im1, abre.
        if self.im1 is None:
            self.abrir_imagem_1()
        #Se não tem imagem im2, abre.
        if len(self.im1.shape) == 3:
            self.tons_de_cinza()
            self.binario()
            self.Op_xor()
        else:
            self.im_res = self.im1 | self.im2
            self.im_res = cv2.bitwise_not(self.im_res) 
            self.im_res = self.im_res.astype('uint8')
            self.atualizarIm('im_res')

    def escalonamento(self,px,py,escalar,tipo):
        print('escalonamento')

        sx=escalar
        sy=escalar
        
        im1 = self.im1 

        im_res = np.zeros(np.shape(im1))
        
        a = len(im1)
        b = len(im1[0])

        if tipo == "centro":
            px=a/2
            py=b/2
        
        a1 = int(-px+px/sx)
        b1 = int(-py+py/sy)

        for i in range(a-1):
           for j in range(b-1):
              x=(i+a1)*sx
              y=(j+b1)*sy
              if -a<x<a and -b<y<b:
                 im_res[i,j] = im1[int(x),int(y)]
              if x<=0 or y<=0:
                 im_res[i,j] = 0

        
        self.im_res = im_res.astype('uint8')
        self.atualizarIm('im_res')
    
    def abrirDialog1(self):
        if self.im1 is None:
            self.abrir_imagem_1()
            
        dialogo = Dialogo()
        dialogo.setWindowTitle('Escalonamento')
        dialogo.exec_()

        if dialogo.cancelou == 1 :
            pass
        if dialogo.cancelou == 0 :
            escalar = float(dialogo.lineEdit_3.text())
            if dialogo.checkBox_3.isChecked() is True:
                px=int(dialogo.lineEdit.text())
                py=int(dialogo.lineEdit_2.text())
                self.escalonamento(px,py,escalar,"")
            if dialogo.checkBox.isChecked() is True:
                self.escalonamento(0,0,escalar,"")
            if dialogo.checkBox_2.isChecked() is True:
                self.escalonamento(0,0,escalar,"centro")

    def translacao(self,x,y):
        im1 = self.im1 

        im_res = np.zeros(np.shape(im1))
            
        a = len(im1)
        b = len(im1[0])

        a1 =x
        b1 =y

        for i in range(a):
           for j in range(b):
              x=i+a1
              y=j+b1
              if x<a and y<b:
                im_res[x,y] = im1[i,j]
              if x<=0 or y<=0:
                 im_res[i,j] = 0

        self.im_res = im_res.astype('uint8')
        self.atualizarIm('im_res')

    def abrirDialog2(self):
        if self.im1 is None:
            self.abrir_imagem_1()
            
        dialogo = Dialogo2()
        dialogo.exec_()

        if dialogo.cancelou == 1 :
            pass
        
        if dialogo.cancelou == 0 :
            x=int(dialogo.lineEdit.text())
            y=int(dialogo.lineEdit_2.text())
            self.translacao(x,y)

    def rotacao(self,px,py,angulo,tipo):
        if self.im1 is None:
            self.abrir_imagem_1()

        im1 = self.im1 

        im_res = np.zeros(np.shape(im1))
        
        a = len(im1)
        b = len(im1[0])

        px=a #coordenada de rotação para o eixo x
        py=b #coordenada de rotação para o eixo y

        
        if tipo == "centro":
            px=a/2
            py=b/2
            print("centro acionado")

        a1 = int(-px)
        b1 = int(-py)


        x=0
        y=0
        graus=-angulo
        theta=(3.14/180)*graus #rad

        for j in range(b):
           for i in range(a):
              x= (i+a1)*np.cos(theta)-(j+b1)*np.sin(theta)-a1
              y= (i+a1)*np.sin(theta)+(j+b1)*np.cos(theta)-b1
              if -a<x<a and -b<y<b:
                im_res[i,j]= im1[int(np.floor(x)),int(np.floor(y))]
              if x<=0 or y<=0:
                 im_res[i,j] = 0

        
        self.im_res = im_res.astype('uint8')
        self.atualizarIm('im_res')

    def abrirDialog3(self):
        if self.im1 is None:
            self.abrir_imagem_1()
            
        dialogo = Dialogo()
        dialogo.setWindowTitle('Rotação')
        #dialogo.label_1.setText('Ângulo de rotação:')
        dialogo.exec_()

        if dialogo.cancelou == 1 :
            pass
        if dialogo.cancelou == 0 :
            angulo = float(dialogo.lineEdit_3.text())
            if dialogo.checkBox_3.isChecked() is True:
                px=int(dialogo.lineEdit.text())
                py=int(dialogo.lineEdit_2.text())
                self.rotacao(px,py,angulo,"")
            if dialogo.checkBox.isChecked() is True:
                self.rotacao(0,0,angulo,"")
            if dialogo.checkBox_2.isChecked() is True:
                self.rotacao(0,0,angulo,"centro")

    def B_derivativo(self):
        if self.im1 is None:
            self.abrir_imagem_1()
        if len(self.im1.shape) == 3:
            self.tons_de_cinza()

        
        n=self.n
        
        img=self.im1.astype('int')

        a1=len(img)  #largura
        a2=len(img[0])  #altura

        Dx = np.empty((a1, a2))
        Dx = Dx.astype(int)

        Dy = np.empty((a1, a2))
        Dy = Dy.astype(int)



        for i in range(a1-1):
           for p in range(a2-1):
              if p+n<a2:
                 Dx[i, p] = img[i, p] - img[i, p + n]


        for p in range(a2-1):
           for i in range(a1-1):
              if i+n<a1:
                 Dy[i, p] = img[i, p] - img[i+n, p]


        M = np.sqrt(Dx ** 2 + Dy ** 2)
        

        #Normalização para escala tons de cinza
        M_max=M.max()
        M = M * (255 / M_max)

        im_res = M

        self.im_res = im_res.astype('uint8')
        self.atualizarIm('im_res')
        
    def Sobel(self,img):
        #Detecção de borda Sobel
        Sx=(1/4)*np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        Sy=(1/4)*np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])

        if img=='im2':
            resx = self.convolucao(Sx,'im2')
            resy = self.convolucao(Sy,'im2')

        else:
            resx = self.convolucao(Sx,'im1')
            resy = self.convolucao(Sy,'im1')

        theta=abs(np.arctan2(resy,resx)*180/np.pi)
        
        im_res = abs(resx)+abs(resy)

        res_max=im_res.max()
        limiar=30
        #im_res[im_res<limiar]=0
        im_res=im_res*(255/res_max)
        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

        return im_res, theta

    def Kirsch(self):
        m0=np.array([[-3,-3,5],[-3,0,5],[-3,-3,5]])
        m1=np.array([[-3,5,5],[-3,0,5],[-3,-3,-3]])
        m2=np.array([[5,5,5],[-3,0,-3],[-3,-3,-3]])
        m3=np.array([[5,5,-3],[5,0,-3],[-3,-3,-3]])
        m4=np.array([[5,-3,-3],[5,0,-3],[5,-3,-3]])
        m5=np.array([[-3,-3,-3],[5,0,-3],[5,5,-3]])
        m6=np.array([[-3,-3,-3],[-3,0,-3],[5,5,5]])
        m7=np.array([[-3,-3,-3],[-3,0,5],[-3,5,5]])
        
        resm0=self.convolucao(m0,'im1')
        resm1=self.convolucao(m1,'im1')
        resm2=self.convolucao(m2,'im1')
        resm3=self.convolucao(m3,'im1')
        resm4=self.convolucao(m4,'im1')
        resm5=self.convolucao(m5,'im1')
        resm6=self.convolucao(m6,'im1')
        resm7=self.convolucao(m7,'im1')

        im_res=np.maximum(resm0[:],resm1[:],resm2[:])
        im_res=np.maximum(im_res[:],resm3[:],resm4[:])
        im_res=np.maximum(im_res[:],resm5[:],resm6[:])
        im_res=np.maximum(im_res[:],resm7[:])

        res_max=im_res.max()
        limiar=127
        im_res[im_res<127]=0
        im_res=im_res*(255/res_max)
        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def Laplaciano3x3(self):
        mascara=np.array([[0,-1,0],
                          [-1,4,-1],
                          [0,-1,0]])

        im_res=self.convolucao(mascara,'im1')

        res_max=im_res.max()
        limiar=127
        im_res[im_res<127]=0
        im_res=im_res*(255/res_max)
        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def Laplaciano5x5(self):
        mascara=np.array([[-1,-1,-1,-1,-1],
                          [-1,-1,-1,-1,-1],
                          [-1,-1,24,-1,-1],
                          [-1,-1,-1,-1,-1],
                          [-1,-1,-1,-1,-1]])

        im_res=self.convolucao(mascara,'im1')

        res_max=im_res.max()
        limiar=127
        im_res[im_res<127]=0
        im_res=im_res*(255/res_max)
        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')
        
    def Laplaciano9x9(self):
        mascara=np.array([[-1,-1,-1,-1,-1,-1,-1,-1,-1],
                          [-1,-1,-1,-1,-1,-1,-1,-1,-1],
                          [-1,-1,-1,-1,-1,-1,-1,-1,-1],
                          [-1,-1,-1,8,8,8,-1,-1,-1],
                          [-1,-1,-1,8,8,8,-1,-1,-1],
                          [-1,-1,-1,8,8,8,-1,-1,-1],
                          [-1,-1,-1,-1,-1,-1,-1,-1,-1],
                          [-1,-1,-1,-1,-1,-1,-1,-1,-1],
                          [-1,-1,-1,-1,-1,-1,-1,-1,-1]])

        im_res=self.convolucao(mascara,'im1')

        res_max=im_res.max()
        limiar=127
        im_res[im_res<127]=0
        im_res=im_res*(255/res_max)
        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def abrirDialog4(self):
        if self.im1 is None:
            self.abrir_imagem_1()
            
        dialogo = Dialogo4()
        dialogo.exec_()
        
        if dialogo.cancelou==1:
            pass
        else:
            if dialogo.horizontalSlider.value()%2 == 0:
                tam=dialogo.horizontalSlider.value()+1
            else:
                tam=dialogo.horizontalSlider.value()
            self.Gaussiano(tam,1.4)

    def Gaussiano(self,tam,sig):

        intervalo = (2*sig+1.)/(tam)
        x = np.linspace(-sig-intervalo/2., sig+intervalo/2., tam+1)
        kern1d = np.diff(st.norm.cdf(x))
        kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
        mascara = kernel_raw/kernel_raw.sum()
        
        im_res=self.convolucao(mascara,'im1')

        for i in range(tam):
            im_res[:,-i]=im_res[:,-tam-1]
            im_res[-i,:]=im_res[-tam-1,:]
        
        res_max=im_res.max()
        im_res=im_res*(255/res_max)

        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

        return im_res

    def Canny(self):

        a1,a2 = np.shape(self.im_res)
        
        self.Gaussiano(5,1.4)
        im_res,theta = self.Sobel('im2')

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
        a=0
        pixel=0
        
        for i in range(a1):
            for p in range(a2):
                if (i+1<a1 & i-1 > 0) and (p+1<a2 & p-1>0) is True:
                    a=im_res[i-1:i+1,p-1:p+1]
                    print(a)
                    pixel = a.flat[np.abs(a-pix_forte).argmin()]
                    if pixel == pix_forte is True:
                        im_final[i,p] = 255

        print(im_final)
        

        final_max=im_final.max()
        im_final=im_final*(255/final_max)

        self.im_res=im_final.astype('uint8')
        self.atualizarIm('im_res')
        
    
    def convolucao(self,mascara,img):


        if img == 'im1':
            imagem=self.im1.astype('int')

        if img == 'im2':
            imagem=self.im_res.astype('int')
            
        a1,a2 = np.shape(imagem) # dimensões da imagem
        b1,b2 = np.shape(mascara) #dimensões da máscara

        im_res_masc = np.zeros([a1,a2])

        #Convolução tipo varredura:

        for i in range(a1):
            for p in range(a2):
                if i <= a1-b1 and p <= a2-b2 :
                    im_res_masc[i,p]= np.sum([mascara[:,:]*imagem[i:i+b1,p:p+b2]])

        return im_res_masc

    def Histo(self):
        imagem=self.im1.astype('int')
        a= len(imagem)
        b= len(imagem[0])
        hist=np.zeros([255])
        for i in range(255):
            hist[i]=sum(sum(imagem==i))

        hist=hist/(a*b)

        self.hist=hist

        fig = plt.figure()
        fig.canvas.set_window_title('Visão Computacional - Histograma')
        plt.title('Histograma')
        plt.xlabel('Pixels')
        plt.ylabel('Probabilidade')
        plt.plot(hist)
        plt.show()

    def Equaliza(self):
        imagem=self.im1.astype('int')
        if sum(self.hist)==0:
            QMessageBox.about(self,"Erro", "Calcule primeiramente o histograma.")
        else:
            hist=self.hist

            #CALCULO DA CDF 

            k=255
            prob=np.zeros([k])

            nivel=int(255/(k-1))
            nivel_map=np.arange(0,k)/k
            p=0

            im_res=np.zeros(imagem.shape)

            for l in range(0,k,1):
                prob[l]=np.sum(hist[l*nivel:nivel+l*nivel])+prob[l-1]

            for i in range(imagem.shape[0]):
                for j in range(imagem.shape[1]):
                    p=int(imagem[i,j]*k/255)-1
                    idx = (np.abs(nivel_map-prob[p])).argmin()
                    im_res[i,j]=idx


            self.im_res=im_res.astype('uint8')
            self.atualizarIm('im_res')
            
    def Auto(self):
        imagem=self.im1.astype('int')

        im_res=np.zeros(imagem.shape)

        a=imagem.max()
        b=imagem.min()
        im_res = (imagem - b)*(255/(a-b))

        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def Global(self):
        img=self.im1.astype('int')
        a = len(img)
        b = len(img[0])
        T=sum(sum(img))/(a*b)
        dt=100
        while dt > 0.5:
            m1=sum(sum((img<T)==True))
            m2=sum(sum((img>T)==True))
            M1=sum(img[img<T])/m1
            M2=sum(img[img>T])/m2
            T1=(M1+M2)/2
            dt=abs(T-T1)
            T=T1

        mascara=img
        mascara[mascara<T]=0
        mascara[mascara>T]=255
        

        self.im_res=mascara.astype('uint8')
        self.atualizarIm('im_res')

    def cdf(self):
        if sum(self.hist)==0:
            QMessageBox.about(self,"Erro", "Calcule primeiramente o histograma.")
        else:
            cdf=np.zeros([255])
            hist=self.hist

            for i in range(255):
                if i > 2:
                    cdf[i]= cdf[i-1] + hist[i]

                
            fig = plt.figure()
            fig.canvas.set_window_title('Visão Computacional - CDF')
            plt.title('CDF')
            plt.xlabel('Pixels')
            plt.ylabel('Probabilidade Acumulada') 
            plt.plot(cdf)
            plt.show()

    def Otsu(self):
        if sum(self.hist)==0:
            QMessageBox.about(self,"Erro", "Calcule primeiramente o histograma.")
        else:
            hist=self.hist
            img=self.im1.copy()
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
                    if P1[k] != 0 :
                        var[k]=(mg*P1[k]-m[k])**2/(P1[k]*(1-P1[k]))
          
            s,z = np.where([var==var.max()])
            T=z[0]
            mascara=img
            mascara[mascara<T]=0
            mascara[mascara>T]=255

            self.im_res=mascara.astype('uint8')
            self.atualizarIm('im_res')

    
    def media(self):
        tam=5
        mascara=(1/tam**2)*np.ones([tam,tam])
        #mascara=mascara.astype('int')

        im_res=self.convolucao(mascara,'im1')

        
        res_max=im_res.max()
        im_res=im_res*(255/res_max)

        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def passaAlta(self):
        mascara=(1/9)*np.array([[-1,-1,-1],
                          [-1,8,-1],
                          [-1,-1,-1]])

        im_res=self.convolucao(mascara,'im1')

        
        res_max=im_res.max()
        im_res=im_res*(255/res_max)

        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def mediana(self):
        tam=5
        im_res=cv2.medianBlur(self.im1,tam)
        
        res_max=im_res.max()
        im_res=im_res*(255/res_max)

        self.im_res=im_res.astype('uint8')
        self.atualizarIm('im_res')

    def morfoPersonalizado(self):
        img=self.im1.copy()
        if np.any((img[:, :] != 0)&(img[:, :] != 255 )):
            QMessageBox.about(self,"Erro", "Converta imagem para binário.")
        else:
            
            dialogo = Dialogo7()
            dialogo.setWindowTitle('Morfologia Personalizada')
            dialogo.exec_()

            if dialogo.cancelou != 1:
                elemento=dialogo.elemento
                referencia=np.asarray(dialogo.referencia).astype('int')
                ref=np.where(referencia==1)
                ref2=np.asarray(ref)

                

                if dialogo.radioButton.isChecked() == True:
                    img_res=self.morfoOp1(img,0,elemento,ref2)
                    
                if dialogo.radioButton_2.isChecked() == True:
                    img_res=self.morfoOp2(img,0,elemento,ref2)
                    
                if dialogo.radioButton_3.isChecked() == True:
                    img_res=self.morfoOp1(img,0,elemento,ref2)
                    img_res=self.morfoOp2(img_res,0,elemento,ref2)
                    img_res=self.morfoOp2(img_res,0,elemento,ref2)
                    
                if dialogo.radioButton_4.isChecked() == True:
                    img_res=self.morfoOp2(img,0,elemento,ref2)
                    img_res=self.morfoOp1(img_res,0,elemento,ref2)
                    img_res=self.morfoOp1(img_res,0,elemento,ref2)

                self.im_res=img_res.astype('uint8')
                self.atualizarIm('im_res')
            

    def morfoOp1(self,img,tamanho,elemento,referencia):
        if tamanho != 0 :
            elm=np.ones([tamanho,tamanho])
            ref=np.array([np.floor(tamanho/2),np.floor(tamanho/2)]).astype('int')

        else:
            elm=elemento
            ref=referencia.astype('int')
            ref=np.array([int(ref[0]),int(ref[1])])

            
        img_res=np.zeros(img.shape)
        
        for i in range(img.shape[0]): 
            for j in range(img.shape[1]):

                if img[i,j]==255:
                    for x in range(ref[0]-elm.shape[0],elm.shape[0]-ref[0],1):
                        for y in range(ref[1]-elm.shape[1],elm.shape[1]-ref[1],1):

                            if elm[x+ref[0],y+ref[1]]==1:
                                if i-x >= 0 and j-y >= 0 and i-x <= img.shape[0] and j-y <= img.shape[1]:
                                    img_res[i-x-1,j-y-1]=255
        return img_res

    def morfoOp2(self,img,tamanho,elemento,referencia):
        if tamanho != 0 :
            elm=np.ones([tamanho,tamanho])
            ref=np.array([np.ceil(tamanho/2),np.ceil(tamanho/2)]).astype('int')
        else:
            elm=elemento
            ref=referencia.astype('int')
            ref=np.array([int(ref[0]),int(ref[1])])

        img_res=255*np.ones(img.shape)
        

        for i in range(img.shape[0]): 
            for j in range(img.shape[1]):

                if img[i,j]==0:
                    for x in range(ref[0]-elm.shape[0],elm.shape[0]-ref[0],1):
                        for y in range(ref[1]-elm.shape[1],elm.shape[1]-ref[1],1):

                            if elm[x+ref[0],y+ref[1]]==1:
                                if i-x >= 0 and j-y >= 0 and i-x <= img.shape[0] and j-y <= img.shape[1]:
                                    img_res[i-x-1,j-y-1]=0
        return img_res


    def morfoDilatacao(self):
        img=self.im1.copy()
        print(np.any((img[:, :] != 0)&(img[:, :] != 255 )))
        if np.any((img[:, :] != 0)&(img[:, :] != 255 )):
            QMessageBox.about(self,"Erro", "Converta imagem para binário.")
        else: 
            dialogo = Dialogo4()
            dialogo.setWindowTitle('Dilatação')
            dialogo.label.setText('Defina o tamanho do elemento estruturante:')
            dialogo.exec_()

            if dialogo.cancelou == 0:
                tamanho=int(dialogo.horizontalSlider.value())
            
                img_res=self.morfoOp1(img,tamanho,0,0)

                self.im_res=img_res.astype('uint8')
                self.atualizarIm('im_res')
            

    def morfoErosao(self):
        img=self.im1.copy()
        #ver se a imagem 1 está em binário
        if np.any((img[:, :] != 0)&(img[:, :] != 255 )):
            QMessageBox.about(self,"Erro", "Converta imagem para binário.")
        else:
            dialogo = Dialogo4()
            dialogo.setWindowTitle('Erosão')
            dialogo.label.setText('Defina o tamanho do elemento estruturante:')
            dialogo.exec_()

            if dialogo.cancelou == 0:
                tamanho=int(dialogo.horizontalSlider.value())
                img_res=self.morfoOp2(img,tamanho,0,0)
                
                self.im_res=img_res.astype('uint8')
                self.atualizarIm('im_res')

    def morfoAbertura(self):
        img=self.im1.copy()
        if np.any((img[:, :] != 0)&(img[:, :] != 255 )):
            QMessageBox.about(self,"Erro", "Converta imagem para binário.")

        else:
            dialogo = Dialogo4()
            dialogo.setWindowTitle('Abertura')
            dialogo.label.setText('Defina o tamanho do elemento estruturante:')
            dialogo.exec_()

            if dialogo.cancelou == 0:
                tamanho=int(dialogo.horizontalSlider.value())
                img_res=self.morfoOp1(img,tamanho,0,0)
                img_res=self.morfoOp2(img_res,tamanho,0,0)
                img_res=self.morfoOp2(img_res,tamanho,0,0)
                
                self.im_res=img_res.astype('uint8')
                self.atualizarIm('im_res')
            

    def morfoFechamento(self):
        img=self.im1.copy()
        if np.any((img[:, :] != 0)&(img[:, :] != 255 )):
            QMessageBox.about(self,"Erro", "Converta imagem para binário.")
        
        else:
            dialogo = Dialogo4()
            dialogo.setWindowTitle('Fechamento')
            dialogo.label.setText('Defina o tamanho do elemento estruturante:')
            dialogo.exec_()

            if dialogo.cancelou == 0:
                tamanho=int(dialogo.horizontalSlider.value())
                img_res=self.morfoOp2(img,tamanho,0,0)
                img_res=self.morfoOp1(img_res,tamanho,0,0)
                img_res=self.morfoOp1(img_res,tamanho,0,0)
                
                self.im_res=img_res.astype('uint8')
                self.atualizarIm('im_res')
            
        
app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())
    
