import sys
import cv2 as cv2
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st

from PyQt5.QtWidgets import QMainWindow, QApplication, qApp, QFileDialog, QMessageBox, QLineEdit, QDialog, QCheckBox
from PyQt5.QtGui import QPixmap, QImage, qRgb, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, pyqtSlot      

class Dialogo(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        loadUi('Interfaces/Dialog1.ui',self)
        self.setWindowIcon(QIcon('Icone.png'))
        self.pushButton.clicked.connect(self.BotaoOk)
        self.pushButton_2.clicked.connect(self.Cancelar)
        self.checkBox.toggled.connect(self.BoxChecked)
        self.checkBox_2.toggled.connect(self.BoxChecked)
        self.checkBox_3.toggled.connect(self.BoxChecked)
        self.cancelou = 0

    def BoxChecked(self):
        if self.checkBox.isChecked() is True:
            self.checkBox_2.setEnabled(False)
            self.checkBox_3.setEnabled(False)
            
        elif self.checkBox_2.isChecked() is True :
            self.checkBox.setEnabled(False)
            self.checkBox_3.setEnabled(False)

        elif self.checkBox_3.isChecked() is True :
            self.checkBox_2.setEnabled(False)
            self.checkBox.setEnabled(False)

        else:
            self.checkBox_2.setEnabled(True)
            self.checkBox_3.setEnabled(True)
            self.checkBox.setEnabled(True)
            
        
    def BotaoOk(self):
      
        if self.lineEdit_3.text() != "" and (self.checkBox.isChecked() or self.checkBox_2.isChecked()) is True :
            self.close()
        if self.lineEdit_3.text() == "" :
            QMessageBox.about(self,"Erro", "Adicione dados.")
        if (self.checkBox.isChecked() or self.checkBox_2.isChecked() or self.checkBox_3.isChecked()) is not True:
            QMessageBox.about(self,"Erro", "Adicione uma opção.")
        if self.checkBox_3.isChecked() and (self.lineEdit.text() and self.lineEdit_2.text() == "" ) is True:
            QMessageBox.about(self,"Erro", "Adicione coordenadas do ponto P.")
        if (self.checkBox_3.isChecked() and (self.lineEdit_3.text() != "") is True) and (self.lineEdit.text() and self.lineEdit_2.text() != "" ) is True:
            self.close()
        
    def Cancelar(self):
        self.cancelou = 1
        self.close()
        
class Dialogo2(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        loadUi('Interfaces/Dialog2.ui',self)
        self.setWindowTitle('Translação')
        self.setWindowIcon(QIcon('Icone.png'))
        self.pushButton.clicked.connect(self.BotaoOk)
        self.pushButton_2.clicked.connect(self.Cancelar)
        self.cancelou = 0
            
        
    def BotaoOk(self):
        if (self.lineEdit.text() != "") and (self.lineEdit_2.text() != "") is True:
            self.close()
        else:
            QMessageBox.about(self,"Erro", "Adicione coordenadas X e Y de trnaslação.")
            
    def Cancelar(self):
        self.cancelou = 1
        self.close()
        
class Dialogo4(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        loadUi('Interfaces/Dialog4.ui',self)
        self.setWindowTitle('Filtro Gaussiano')
        self.setWindowIcon(QIcon('Icone.png'))
        self.pushButton.clicked.connect(self.BotaoOk)
        self.pushButton_2.clicked.connect(self.Cancelar)
        self.cancelou = 0
        self.horizontalSlider.valueChanged.connect(self.atualizar_lim)



    def atualizar_lim(self):
        self.label_2.setText(str(self.horizontalSlider.value())+' X '+str(self.horizontalSlider.value()))

    def BotaoOk(self):
        self.close()
    def Cancelar(self):
        self.cancelou=1
        self.close()

class Dialogo5(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        loadUi('Interfaces/Dialog5.ui',self)
        self.setWindowTitle('Operação por Escalar')
        self.setWindowIcon(QIcon('Icone.png'))
        self.cancelou = 0
        self.pushButton.clicked.connect(self.BotaoOk)
        self.pushButton_2.clicked.connect(self.BotaoCancelar)

    def BotaoOk(self):
        if (self.radioButton.isChecked() | self.radioButton_2.isChecked()) != True:
            QMessageBox.about(self,"Erro", "Selecione uma opção de operação.")
        else:
            self.close()

    def BotaoCancelar(self):
            self.cancelou = 1
            self.close()

class Morfologia(QDialog):
    def __init__(self, x, y ,parent = None):
        QDialog.__init__(self, parent)
        loadUi('Interfaces/Dialog6.ui',self)
        self.setWindowTitle('Operação por Escalar')
        self.setWindowIcon(QIcon('Icone.png'))
        self.setMouseTracking(True)
        self.img = None
        self.x = x
        self.y = y
        self.cancelou=0
        self.elemento = np.zeros([x,y])
        self.referencia = np.zeros([x,y])
        self.imgInicial()
        self.op=0
        self.pushButton.clicked.connect(self.origem)
        self.pushButton_2.clicked.connect(self.OK)
        self.pushButton_3.clicked.connect(self.cancelar)

    def OK(self):
        if self.referencia.any():
            self.close()
        else:
            QMessageBox.about(self, "Erro", "Defina a origem do elemento estruturante.")
    def cancelar(self):
        self.cancelou = 1
        self.close()

    def origem(self):
        if self.op==1:
            slef.op=0
        else:
            self.op=1

    def imgInicial(self):
        imagem=255*np.ones([10*self.x, 10*self.y])

        for i in range(0,self.x,1):
            imagem[0:self.y*10,i*10]=0
            imagem[i*10, 0:self.y*10]=0
        
        imagem[0:self.y*10,-1]=0
        imagem[-1, 0:self.y*10]=0
        
        self.img=imagem.copy()
        self.img=self.img.astype('uint8')
        self.atualizarIm()
        

    def mousePressEvent(self, event):
        pixel_x=480/self.x*2
        pixel_y=480/self.y*2
        cor_x=int(np.floor(event.x()/pixel_x*2))
        cor_y=int(np.floor(event.y()/pixel_y*2))

        if cor_x <=self.x and cor_y <=self.y:
            self.novaImagem(cor_x,cor_y)

    def novaImagem(self, my, mx):
        
        imagem=255*np.ones([10*self.x,10*self.y])

        if self.op==1:
            self.referencia = np.zeros([self.x,self.y])
            self.referencia[mx,my]=1
            self.op=0
            
        else:
            
            if self.elemento[mx,my]== 1:
                self.elemento[mx,my]=0
            
            else:
                self.elemento[mx,my]=1

        for m in range(self.x):
            for n in range(self.y):
                
                if self.elemento[m,n] == 1:
                    imagem[m*10:m*10+10,n*10:n*10+10]=0

                    if self.referencia[m,n] == 1:
                        for i in range(1,11,1):
                            imagem[m*10+i,n*10+i]=255
                            imagem[m*10+10-i,n*10+i]=255    
                
                else:
                    imagem[m*10:m*10+10,n*10:n*10+10]=255
                    if self.referencia[m, n] == 1:
                        for i in range(1, 11, 1):
                            imagem[m*10+i, n*10+i] = 0
                            imagem[m*10+10-i, n*10+i] = 0

        for i in range(0,self.x,1):
            imagem[0:self.y*10,i*10]=0
            imagem[i*10,0:self.y*10]=0
        
        imagem[0:self.y*10,-1]=0
        imagem[-1,0:self.y*10]=0
                      
        self.img=imagem.copy()
        self.img=self.img.astype('uint8')
        self.atualizarIm()

    def atualizarIm(self):
        imagem = QImage(self.img, self.img.shape[1], self.img.shape[0], self.img.strides[0], QImage.Format_Indexed8)
        imagem.setColorTable([qRgb(i,i,i) for i in range(256)])
        pixmap = QPixmap.fromImage(imagem)
        pixmap = pixmap.scaled(self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation) 
        self.label.setPixmap(pixmap)

class Dialogo7(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        loadUi('Interfaces/Dialog7.ui',self)
        self.setWindowTitle('Operação por Escalar')
        self.setWindowIcon(QIcon('Icone.png'))
        self.cancelou = 0
        self.pushButton.clicked.connect(self.BotaoOk)
        self.pushButton_2.clicked.connect(self.BotaoCancelar)
        self.x=0
        self.y=0
        self.referencia = None
        self.elemento = None
        
    def BotaoOk(self):
        if self.lineEdit.text() == "":
            QMessageBox.about(self,"Erro", "Defina o tamanho do elemento estruturante.")
        else:
            self.x=int(self.lineEdit.text())
            self.y=int(self.lineEdit.text())
            morfologia = Morfologia(self.x,self.y)
            morfologia.exec_()

            if morfologia.cancelou == 0:
                self.elemento = morfologia.elemento
                self. referencia = morfologia.referencia
            else:
                self.cancelou = 1
        
            self.close()

    def BotaoCancelar(self):
        self.cancelou = 1
        self.close()
  