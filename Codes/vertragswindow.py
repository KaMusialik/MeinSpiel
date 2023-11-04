# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd


from pathlib import Path

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class VertragsWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_vertragswindow'))
        
        self.file_bestand = f_dict.get('file_system_bestand')
        datei = Path(self.file_bestand)
        if datei.is_file():
            text = 'vertragswindow/init: Die Datei ' + self.file_bestand + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'vertragswindow/init: Die Datei ' + self.file_bestand + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
      
        self.file_ui = f_dict.get('vertragswindow_file')

        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'vertragswindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'vertragswindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

    def BestimmeListe(self, nameDerEntitaet):
        #hier wird die Liste der vorkommenden Auspraegungen ermittelt. Die Liste wird dann in der Combobox erscheinen 
        
        datei=self.file_bestand
        df=pd.read_csv(datei, sep=";")
                
        df1 = df.groupby([nameDerEntitaet], as_index=False)['wert'].sum()
        
        liste = []
        
        if df1.empty:
            text = 'vertragswindow/BestimmeListe: in der Tabelle Bestand: ' +datei+ ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            for index, row in df1.iterrows():
                
                name = str(row[nameDerEntitaet])
                liste.append(name)
        
        return liste

    def LeseVertrag(self):
        #hier werden alle gefilterte Informationen zum Vertrag ausgegeben:
        
        #lese Filter:    
        vsnr = int(self.w.comboBox_vertrag.currentText())
        
        datei=self.file_bestand
        
        df = pd.read_csv(datei, sep=";")
        df1 = df[( (df.vsnr == vsnr) )]

        col_labels = ['name', 'Wert']
        
        #dimensioniere die Tabelle:
        self.w.tableWidget_Vertrag.setRowCount(len(df1)+1)
        self.w.tableWidget_Vertrag.setColumnCount(2)
        
        irow = 0

        #setzt die Spaltenbeschrieftung und die Farbe in die Beschriftungszelle:
        self.w.tableWidget_Vertrag.setItem(0, 0, QTableWidgetItem(col_labels[0]))
        self.w.tableWidget_Vertrag.item(0, 0).setBackground(QtGui.QColor(151, 255, 255))
        self.w.tableWidget_Vertrag.setItem(0, 1, QTableWidgetItem(col_labels[1]))
        self.w.tableWidget_Vertrag.item(0, 1).setBackground(QtGui.QColor(151, 255, 255))
                
        for index, row in df1.iterrows():
            irow = irow + 1
            name = str(row['name'])
            wert = str(row['wert'])
            self.w.tableWidget_Vertrag.setItem(irow, 0, QTableWidgetItem(name))
            self.w.tableWidget_Vertrag.setItem(irow, 1, QTableWidgetItem(wert))
        
        
        #Anpassung der zwei Spalten an das TableWigets:
        #self.w.tableWidget_Vertrag.setFixedWidth(self.w.tableWidget_Vertrag.columnWidth(0)+self.w.tableWidget_Vertrag.columnWidth(1) )
        #self.w.tableWidget_Vertrag.resize(self.w.tableWidget_Vertrag.sizeHint())
    
    def SchliesseFenster(self):
        self.w.close()
        
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        self.w.comboBox_vertrag.activated.connect(self.LeseVertrag)
        
        vsnr_liste = []
        vsnr_liste = self.BestimmeListe('vsnr')
        self.w.comboBox_vertrag.addItems(vsnr_liste)
       
        self.LeseVertrag()
        self.w.exec_()
