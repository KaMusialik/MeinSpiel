# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
from copy import deepcopy

import hilfe_system as hs

from pathlib import Path

import PyQt5.uic as uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui, QtCore

class StatistikWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_statistikwindow'))
        
        self.file_statistik = f_dict.get('file_system_statistik')
        self.dtype_statistik_dict= { 'von':int, 'bis':int, 'produkt':int, 'position':str, 'vsnr':int, 'histnr':int, 'name':str, 'wert':float}
        
        self.file_ui = f_dict.get('statistikwindow_file')

        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'Statistikwindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'Statistikwindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
            
        self.listeStatistikPositionen_dict = {}
    
    def LesePositionenAusStatistikCSV(self):
        datei=self.file_statistik
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_statistik_dict)
                
        df1 = df.groupby(['name'], as_index=False)['wert'].sum()
        
        pos_liste = []
        
        if df1.empty:
            text = 'Statistik/LeseWertAusStatistikCSVPositionen: in der Statistiktabelle: ' +datei+ ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            for index, row in df1.iterrows():
                
                name = row['name']
                pos_liste.append(name)
        
        return pos_liste
              
    def BereiteWerteFuerTableVor(self, name):
        #hier wird die Statistik in die Tabelle reigeschrieben:
        datei=self.file_statistik
        
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_statistik_dict)

        col_labels = []
        row_labels = ['Anfang', 'Zugang', 'Abgang', 'Ende']

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df1=df[(df.name == name)].groupby('bis', as_index=False).count()
        df2=df1[['bis']]
    
        for index, row in df2.iterrows():
            bis=str(row['bis'])
            jahr=bis[0:4]
            col_labels.append(jahr)
          
    
        wert={}
        wert_dict={}
        
        for jahr in col_labels:
            wert_dict.clear()
            wert_dict['jahr']=jahr
            wert_dict['von']=jahr+'0101'
            wert_dict['bis']=jahr+'1231'
            
            for position in row_labels:
                wert_dict['position'] = position.lower()
    
                von=int(wert_dict.get('von'))
                bis=int(wert_dict.get('bis'))
                pos=wert_dict.get('position')
                
                df1=df[((df.name==name) & (df.von==von) & (df.bis==bis) & (df.position==pos))]
                df2=df1[['von', 'bis', 'position', 'name', 'wert']].groupby(['von', 'bis', 'position', 'name'], as_index=False).sum()
                
                if df2.__len__() == 0:
                    #keine Werte gefunden. Es ist nicht schlim. Es kann schon sein:
                    ergebnis = 0
                else:
                    if df2.__len__() > 1:
                        #es dürfen nicht mehr als ein wert sein. Also fehler:
                        text = 'Statistikwindow/WerteInTabelle: es wurde mehr als nur ein Wert gefunden. das kein nicht sein!: ' + str(wert_dict)
                        self.oprot.SchreibeInProtokoll(text)
                    else:
                        index=df2['wert'].index[0]
                        ergebnis = df2.at[index, 'wert']

                wert_dict[position] = ergebnis
            
            wert[jahr]=deepcopy(wert_dict)
            
        return wert

   
    def WerteInTabelle(self, werte_dict):
       
        row_labels_dict = {'Anfang': 1, 'Zugang': 2, 'Abgang': 3, 'Ende': 4}
        ohs = hs.ZahlenFormatieren()
        
        #dimensioniere die Tabelle:
        self.w.tableWidget_Statistik.setRowCount(5)
        self.w.tableWidget_Statistik.setColumnCount(len(werte_dict)+1)
        
        irow = 0
        icol = 0
        #setzt die Farbe in die Beschriftungszelle:
        self.w.tableWidget_Statistik.setItem(0, 0, QTableWidgetItem(""))
        self.w.tableWidget_Statistik.item(0, 0).setBackground(QtGui.QColor(151, 255, 255))
        
        
        #Beschriftungen der Zeilen:
        for key, wert in row_labels_dict.items():
            irow = irow + 1
            self.w.tableWidget_Statistik.setItem(irow, 0, QTableWidgetItem(key))
            self.w.tableWidget_Statistik.item(irow, 0).setBackground(QtGui.QColor(193, 255, 193))
       
        #Beschriftungen der Spalten also Jahre 
        for key, wert in werte_dict.items():
            icol = icol + 1
            self.w.tableWidget_Statistik.setItem(0, icol, QTableWidgetItem(key))
            self.w.tableWidget_Statistik.item(0, icol).setBackground(QtGui.QColor(193, 255, 193))

        icol = 0
        #Werte in die Tabelle schreiben: 
        for werte_key, werte_value in werte_dict.items():
            icol = icol + 1
            irow = 0

            for row_key, row_value in row_labels_dict.items():
                irow = irow + 1
                wert_f = float(werte_value.get(row_key))
                wert_s = ohs.TasenderPunktInFloat(wert_f, 1)
                self.w.tableWidget_Statistik.setItem(irow, icol, QTableWidgetItem(wert_s))
        
        
        
        
    def LeseStatistik(self):
        position = self.w.comboBox_auswahl.currentText()
        werte = {}
        werte= self.BereiteWerteFuerTableVor(position)
        self.WerteInTabelle(werte)
    
    def BestimmeListeStatistikPosiotionen(self):
        
        pos_liste = []
        pos_liste = self.LesePositionenAusStatistikCSV()
        self.w.comboBox_auswahl.addItems(pos_liste)
    
    def SchliesseFenster(self):
        self.w.close()
        
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        self.w.comboBox_auswahl.activated.connect(self.LeseStatistik)
        self.BestimmeListeStatistikPosiotionen()
        self.LeseStatistik()
        self.w.exec_()
