# -*- coding: utf-8 -*-

import protokoll as prot

import pandas as pd

from pathlib import Path

import hilfe_system as hs

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class RentenWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_rentenWindow'))      

        self.file_renten_csv = f_dict.get('file_kapitalanlagen_renten_csv')
        datei = Path(self.file_renten_csv)
        if datei.is_file():
            text = 'RentenWindow/init: Die Datei ' + self.file_renten_csv + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'RentenWindow/init: Die Datei ' + self.file_renten_csv + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
        
        
        self.file_renten_csv_struktur = f_dict.get('file_renten_csv_struktur')

        self.file_ui = f_dict.get('rentenWindow_file')
        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'RentenWindow/init: Die Datei ' + self.file_ui + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'RentenWindow/init: Die Datei ' + self.file_ui + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.listeDerPositionen = { 'Anfang': ('anfang', 1,),
                                    '+ Zuführung aus Kasse':('zugang', 101,),
                                    '+ Zinsen':('zins', 201),
                                    '- Abgang':('ablauf', 301),
                                    '= Ende':('ende', 1001)
                                  }

        
        self.w.setWindowTitle('Renten ...')

    
    
    def ErmittleJahreFuerTableVor(self, jahre_dict):
 
        datei = self.file_renten_csv
        
        df = pd.read_csv(datei, sep=";", dtype=self.file_renten_csv_struktur)
        df1 = df[( (df.nr == 999) )]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2 = df1.groupby(['jahr']).count().reset_index()
        df3 = df2[['jahr']]
    
        for index, row in df3.iterrows():
            jahr = str(row['jahr'])
            jahre_dict[jahr] = jahr

    
    def LeseRenten(self):
        
        ohs = hs.ZahlenFormatieren() #Klasse für die Zahlendarstellung
        
        #Ermittle die bereits gerechneten Jahre:
        jahre_dict = {}
        self.ErmittleJahreFuerTableVor(jahre_dict)
        
        objekt = self.w.tableWidget_rentenWindow
        
        #dimensioniere die Tabelle:
        anzahlDerJahre = len(jahre_dict)
        objekt.setColumnCount(anzahlDerJahre+1)
        
        anzahlDerPositionen = len(self.listeDerPositionen) 
        objekt.setRowCount(anzahlDerPositionen+1)
        
        key_dict = {}
        key_dict['nr'] = '999'
        
        #Überschriften für die Jahre:
        irow = 0
        icol = 0
        
        objekt.setItem(irow, icol, QTableWidgetItem(''))
        objekt.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))
        for keyJahr, jahr in jahre_dict.items():
            icol += 1
            objekt.setItem(irow, icol, QTableWidgetItem(jahr))
            objekt.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))

        #Überschriften für die Positione der Renten:
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
            
            #Kapitalanlagen:
            for keyPosition, wertPosition in self.listeDerPositionen.items():
                irow += 1
                key_dict['name'] = wertPosition[0]
                wert_f = float(self.LeseRentenCSV(key_dict))
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                objekt.setItem(irow, icol, QTableWidgetItem(wert_s))


    
    def LeseRentenCSV(self, key_dict):
        datei = self.file_renten_csv
        df = pd.read_csv(datei, sep=";", dtype=self.file_renten_csv_struktur)
       
        jahr = key_dict.get('jahr')
        nr = key_dict.get('nr')
        name = key_dict.get('name')
 
        df1 = df[(df.jahr == int(jahr)) & (df.nr == int(nr)) & (df.name == str(name))]
        if df1.__len__() == 0:
            wert=0
            text='RentenWindow/LeseRentenCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
       
        return float(wert)   
    
    
    def SchliesseFenster(self):
        self.w.close()
        
    
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
                        
        self.LeseRenten()
        
        self.w.exec_()