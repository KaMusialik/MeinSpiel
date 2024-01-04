# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd

from pathlib import Path

import hilfe_system as hs

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class CashflowWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_cashflowWindow'))      

        self.file_bilanz = f_dict.get('file_bilanz')
        datei = Path(self.file_bilanz)
        if datei.is_file():
            text = 'CashflowWindow/init: Die Datei ' + self.file_bilanz + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'CashflowWindow/init: Die Datei ' + self.file_bilanz + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
        
        
        self.file_kapitalanlage = f_dict.get('file_kapitalanlagen_csv')
        datei = Path(self.file_kapitalanlage)
        if datei.is_file():
            text = 'CashflowWindow/init: Die Datei ' + self.file_kapitalanlage + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'CashflowWindow/init: Die Datei ' + self.file_kapitalanlage + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.file_kapitalanlage_struktur = f_dict.get('file_kapitalanlagen_csv_struktur')

        self.file_ui = f_dict.get('cashflowWindow_file')
        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'CashflowWindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'CashflowWindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.listeDerPositionen = { 'Beiträge': ('beitraege', 1),
                                    '- Provisionen':('provisionen_ap', 101),
                                    '- Kosten':('kosten', 110),
                                    '= cash flow':('cashflow', 1001)
                                  }
        
        self.w.setWindowTitle('Cash Flow ...')

    
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
        
        #dimensioniere die Tabelle:
        anzahlDerJahre = len(jahre_dict)
        self.w.tableWidget_cashflow.setColumnCount(anzahlDerJahre+1)
        
        anzahlDerPositionen = len(self.listeDerPositionen)
        self.w.tableWidget_cashflow.setRowCount(anzahlDerPositionen+1)
        
        key_dict = {}
        key_dict['topf'] = '999'
        
        #Überschriften für die Jahre:
        irow = 0
        icol = 0
        
        self.w.tableWidget_cashflow.setItem(irow, icol, QTableWidgetItem(''))
        self.w.tableWidget_cashflow.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))
        for keyJahr, jahr in jahre_dict.items():
            icol += 1
            self.w.tableWidget_cashflow.setItem(irow, icol, QTableWidgetItem(jahr))
            self.w.tableWidget_cashflow.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))

        #Überschriften für die Positione:
        irow = 0
        icol = 0      
        for keyPosition, wertPosition in self.listeDerPositionen.items():    
            irow += 1
            wert = keyPosition
            self.w.tableWidget_cashflow.setItem(irow, icol, QTableWidgetItem(str(wert)))
            self.w.tableWidget_cashflow.item(irow, icol).setBackground(QtGui.QColor(193, 255, 193))        
        
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
                self.w.tableWidget_cashflow.setItem(irow, icol, QTableWidgetItem(wert_s))
            

    def LeseKapitalanlageCSV(self, key_dict):
        datei = self.file_kapitalanlage
        df = pd.read_csv(datei, sep=";", dtype=self.file_kapitalanlage_struktur)
       
        jahr=key_dict.get('jahr')
        topf=key_dict.get('topf')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == int(jahr)) & (df.topf==str(topf)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
            text='CashflowWindow/LeseKapitalanlagenCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
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