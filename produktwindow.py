# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd


from pathlib import Path

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class ProduktWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_produktwindow'))
        
        self.file_produkt = f_dict.get('file_produkt')
        datei = Path(self.file_produkt)
        if datei.is_file():
            text = 'Produktwindow/init: Die Datei ' +self.file_produkt+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'Produktwindow/init: Die Datei ' +self.file_produkt+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
      
        self.file_ui = f_dict.get('produktwindow_file')

        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'Produktwindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'Produktwindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
            
    def LeseProdukt(self):
        #hier werden alle gefiltrte Informationen zum Produkt ausgegeben:
        
        #lese Filter:    
        tkz = int(self.w.comboBox_tkz.currentText())
        sra = self.w.comboBox_sra.currentText()
        
        datei=self.file_produkt
        
        df = pd.read_csv(datei, sep=";")
        df1 = df[( (df.tkz==tkz) & (df.sra==sra) )]

        col_labels = ['name', 'Wert']
        
        #dimensioniere die Tabelle:
        self.w.tableWidget_Produkt.setRowCount(len(df1)+1)
        self.w.tableWidget_Produkt.setColumnCount(2)
        
        irow = 0

        #setzt die Spaltenbeschrieftung und die Farbe in die Beschriftungszelle:
        self.w.tableWidget_Produkt.setItem(0, 0, QTableWidgetItem(col_labels[0]))
        self.w.tableWidget_Produkt.item(0, 0).setBackground(QtGui.QColor(151, 255, 255))
        self.w.tableWidget_Produkt.setItem(0, 1, QTableWidgetItem(col_labels[1]))
        self.w.tableWidget_Produkt.item(0, 1).setBackground(QtGui.QColor(151, 255, 255))
        
        for index, row in df1.iterrows():
            irow = irow + 1
            name = str(row['name'])
            wert = str(row['wert'])
            self.w.tableWidget_Produkt.setItem(irow, 0, QTableWidgetItem(name))
            self.w.tableWidget_Produkt.setItem(irow, 1, QTableWidgetItem(wert))
            
        
        #Anpassung der zwei Spalten an das TableWigets:
        self.w.tableWidget_Produkt.setFixedWidth(self.w.tableWidget_Produkt.columnWidth(0)+self.w.tableWidget_Produkt.columnWidth(1) )

    
    def BestimmeListe(self, nameDerEntitaet):
        #hier wird die Liste der vorkommenden Auspraegungen ermittelt. Die Liste wird dann in der Combobox erscheinen 
        
        datei=self.file_produkt
        df=pd.read_csv(datei, sep=";")
                
        df1 = df.groupby([nameDerEntitaet], as_index=False)['wert'].sum()
        
        liste = []
        
        if df1.empty:
            text = 'Produktwindow/BestimmeListe: in der Statistiktabelle: ' +datei+ ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            for index, row in df1.iterrows():
                
                name = str(row[nameDerEntitaet])
                liste.append(name)
        
        return liste

    
    def SchliesseFenster(self):
        self.w.close()
        
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        self.w.comboBox_tkz.activated.connect(self.LeseProdukt)
        
        tkz_liste = []
        tkz_liste = self.BestimmeListe('tkz')
        self.w.comboBox_tkz.addItems(tkz_liste)

        sra_liste = []
        sra_liste = self.BestimmeListe('sra')
        self.w.comboBox_sra.addItems(sra_liste)
        
        self.LeseProdukt()
        self.w.exec_()
