# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd

from pathlib import Path

import hilfe_system as hs

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class KapitalanlagenWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_kapitalanlagenWindow'))      

        self.file_bilanz = f_dict.get('file_bilanz')
        datei = Path(self.file_bilanz)
        if datei.is_file():
            text = 'KapitalanlagenWindow/init: Die Datei ' + self.file_bilanz + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'KapitalanlagenWindow/init: Die Datei ' + self.file_bilanz + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
        
        
        self.file_kapitalanlage = f_dict.get('file_kapitalanlagen_csv')
        datei = Path(self.file_kapitalanlage)
        if datei.is_file():
            text = 'KapitalanlagenWindow/init: Die Datei ' + self.file_kapitalanlage + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'KapitalanlagenWindow/init: Die Datei ' + self.file_kapitalanlage + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.file_kapitalanlage_struktur = f_dict.get('file_kapitalanlagen_csv_struktur')

        self.file_ui = f_dict.get('kapitalanlagenWindow_file')
        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'KapitalanlagenWindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'KapitalanlagenWindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.listeDerPositionen = { 'Kapitalanlagen Anfang': ('kapitalanlagen_anfang', 1),
                                    '+ Zufhrung aus Kasse':('umbuchung_kasse', 101),
                                    '+ Veränderung/Zinsen':('zinsen', 201),
                                    '- Abgang':('abgang', 301),
                                    '= Kapitalanlage Ende':('kapitalanlage_ende', 1001)
                                  }
        
        self.w.setWindowTitle('Kapitalanlage ...')

    
    def ErmittleJahreFuerTableVor(self, jahre_dict):
 
        datei = self.file_kapitalanlage
        
        df = pd.read_csv(datei, sep=";", dtype=self.file_kapitalanlage_struktur)
        df1 = df[( (df.topf == '999') )]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2=df1.groupby(['jahr']).count().reset_index()
        df3=df2[['jahr']]
    
        for index, row in df3.iterrows():
            jahr=str(row['jahr'])
            jahre_dict[jahr] = jahr

    
    def LeseKapitalanlagen(self):
        
        ohs = hs.ZahlenFormatieren() #Klasse für die Zahlendarstellung
        
        #Ermittle die bereits gerechneten Jahre:
        jahre_dict = {}
        self.ErmittleJahreFuerTableVor(jahre_dict)
        
        objekt = self.w.tableWidget_kapitalanlagenWindow
        
        #dimensioniere die Tabelle:
        anzahlDerJahre = len(jahre_dict)
        objekt.setColumnCount(anzahlDerJahre+1)
        
        anzahlDerPositionen = len(self.listeDerPositionen)
        objekt.setRowCount(anzahlDerPositionen+1)
        
        key_dict = {}
        key_dict['topf'] = '999'
        
        #Überschriften für die Jahre:
        irow = 0
        icol = 0
        
        objekt.setItem(irow, icol, QTableWidgetItem(''))
        objekt.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))
        for keyJahr, jahr in jahre_dict.items():
            icol += 1
            objekt.setItem(irow, icol, QTableWidgetItem(jahr))
            objekt.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))

        #Überschriften für die Positione:
        irow = 0
        icol = 0      
        for keyPosition, wertPosition in self.listeDerPositionen.items():    
            irow += 1
            wert = keyPosition
            objekt.setItem(irow, icol, QTableWidgetItem(str(wert)))
            objekt.item(irow, icol).setBackground(QtGui.QColor(193, 255, 193))        
        
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
                wert_f = float(self.LeseKapitalanlageCSV(key_dict))
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                objekt.setItem(irow, icol, QTableWidgetItem(wert_s))
            

    def LeseKapitalanlageCSV(self, key_dict):
        datei = self.file_kapitalanlage
        df = pd.read_csv(datei, sep=";", dtype=self.file_kapitalanlage_struktur)
       
        jahr=key_dict.get('jahr')
        topf=key_dict.get('topf')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == int(jahr)) & (df.topf==str(topf)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
            text='KapitalanlagenWindow/LeseKapitalanlagenCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
       
        return float(wert)   
    
    
    def SchliesseFenster(self):
        self.w.close()
        
    
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
                        
        self.LeseKapitalanlagen()
        
        self.w.exec_()