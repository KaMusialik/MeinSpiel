# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd

from pathlib import Path

import hilfe_system as hs

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class GuVWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_guvwindow'))
              
        self.file_bilanz = f_dict.get('file_bilanz')
        datei = Path(self.file_bilanz)
        if datei.is_file():
            text = 'GuVWindow/init: Die Datei ' + self.file_bilanz + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'GuVWindow/init: Die Datei ' + self.file_bilanz + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
      
                   
        self.file_ui = f_dict.get('guvwindow_file')
        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'GuVWindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'GuVWindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.listeDerPositionen = {'Gebuchter Beitrag': ('bil_gebuchter_beitrag', 1),
                                   'Abschlussprovision':('ap', 50),
                                   'Veränderung der Deckungsrückstellung': ('bil_derue7_veraenderung', 100),
                                   'Jahresüberschuss':('jahresueberschuss', 999)
                                   }

    def ErmittleListeDerAbrechnungsverbaende(self):
        datei=self.file_bilanz
        
        df=pd.read_csv(datei, sep=";")
        df1 = df[( (df.rl == 'guv') )]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2=df1.groupby(['avbg']).count().reset_index()
        df3=df2[['avbg']]
    
        liste = []
        for index, row in df3.iterrows():
            wert = str(row['avbg'])
            liste.append(wert)
        
            
        return liste

    
    
    def ErmittleJahreFuerTableVor(self, jahre_dict):
 
        datei=self.file_bilanz
        
        df=pd.read_csv(datei, sep=";")
        df1 = df[( (df.rl == 'guv') )]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2=df1.groupby(['jahr']).count().reset_index()
        df3=df2[['jahr']]
    
        for index, row in df3.iterrows():
            jahr=str(row['jahr'])
            jahre_dict[jahr] = jahr

    def LeseGuV(self):
        
        ohs = hs.ZahlenFormatieren() #Klasse für die Zahlendarstellung
        
        #Ermittle die bereits gerechneten Jahre:
        jahre_dict = {}
        self.ErmittleJahreFuerTableVor(jahre_dict)
        
        #dimensioniere die Tabelle:
        anzahlDerJahre = len(jahre_dict)
        self.w.tableWidget_GuV.setColumnCount(anzahlDerJahre+1)
        
        anzahlDerPositionen = len(self.listeDerPositionen)
        self.w.tableWidget_GuV.setRowCount(anzahlDerPositionen+1)
        
        key_dict = {}
        
        key_dict['rl'] = 'guv'
        
        avbg = self.w.comboBox_avbg.currentText()
        key_dict['avbg'] = avbg
        
        #Überschriften für die Jahre:
        irow = 0
        icol = 0
        
        self.w.tableWidget_GuV.setItem(irow, icol, QTableWidgetItem(''))
        self.w.tableWidget_GuV.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))
        for keyJahr, jahr in jahre_dict.items():
            icol += 1
            self.w.tableWidget_GuV.setItem(irow, icol, QTableWidgetItem(jahr))
            self.w.tableWidget_GuV.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))

        #Überschriften für die Positione:
        irow = 0
        icol = 0      
        for keyPosition, wertPosition in self.listeDerPositionen.items():    
            irow += 1
            wert = keyPosition
            self.w.tableWidget_GuV.setItem(irow, icol, QTableWidgetItem(str(wert)))
            self.w.tableWidget_GuV.item(irow, icol).setBackground(QtGui.QColor(193, 255, 193))

        #Werte in die Tabelle schreiben:       
        irow = 0
        icol = 0      

        for keyJahr, jahr in jahre_dict.items():
            key_dict['jahr'] = jahr
            icol += 1
            irow = 0
        
            for keyPosition, wertPosition in self.listeDerPositionen.items():
                irow += 1
                key_dict['name'] = wertPosition[0]
                wert_f = float(self.LeseBilanzCSV(key_dict))
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                self.w.tableWidget_GuV.setItem(irow, icol, QTableWidgetItem(wert_s))
            
    def LeseBilanzCSV(self, key_dict):
        datei=self.file_bilanz
        df=pd.read_csv(datei, sep=";")
       
        jahr=int(key_dict.get('jahr'))
        rl=str(key_dict.get('rl'))
        avbg=str(key_dict.get('avbg'))
        name=str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.rl==rl) & (df.avbg==avbg) & (df.name==name)]

        if df1.empty:
            wert=0
            text='guvwindow/LeseBilanzCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: '+str(key_dict)
            self.oprot.SchreibeInProtokoll(text)
        else:
            if df1.__len__() != 1:
                wert=999999999
                text='guvWindow/LeseBilanzCSV: mehrere Eintraeg in der Tabelle gefunden. Es wurde ein Wert von '+str(wert)+ ' verwendet: '+str(key_dict)
                self.oprot.SchreibeInProtokoll(text)
            else:
                index=df1.index[0]
                wert=df1.at[index, 'wert']

        return float(wert)   
    
    
    def SchliesseFenster(self):
        self.w.close()
        
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        self.w.comboBox_avbg.activated.connect(self.LeseGuV)
                
        avbg_liste = []
        avbg_liste = self.ErmittleListeDerAbrechnungsverbaende()
        
        self.w.comboBox_avbg.addItems(avbg_liste)
        self.w.comboBox_avbg.setCurrentText('999')

        self.LeseGuV()
        self.w.exec_()