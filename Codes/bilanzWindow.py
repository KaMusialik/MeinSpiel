# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd

from pathlib import Path

import hilfe_system as hs

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class BilanzWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_bilanzWindow'))
              
        self.file_bilanz = f_dict.get('file_bilanz')
        datei = Path(self.file_bilanz)
        if datei.is_file():
            text = 'BilanzWindow/init: Die Datei ' + self.file_bilanz + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'BilanzWindow/init: Die Datei ' + self.file_bilanz + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
      
                   
        self.file_ui = f_dict.get('bilanzWindow_file')
        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'BilanzWindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'BilanzWindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.listeDerPositionenPassivSeite = {'Eigenkapital': ('eigenkapital_ende', 1),
                                            'Deckungsrüuekstellung':('bil_derue7_ende', 100),
                                            }
        self.listeDerPositionenAktivSeite = {'Kapitalanlagen': ('kapitalanlagen_ende', 1001),
                                             'Kasse': ('kasse_ende', 1101)
                                            }
        
        self.w.setWindowTitle('Ergebnisse der Bilanz')


    def ErmittleListeDerAbrechnungsverbaende(self):
        datei = self.file_bilanz
        
        df = pd.read_csv(datei, sep=";")
        df1 = df[( (df.rl == 'bilanz') )]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2 = df1.groupby(['avbg']).count().reset_index()
        df3 = df2[['avbg']]
    
        liste = []
        for index, row in df3.iterrows():
            wert = str(row['avbg'])
            liste.append(wert)
        
            
        return liste
    
    
    def ErmittleJahreFuerTableVor(self, jahre_dict):
 
        datei = self.file_bilanz
        
        df = pd.read_csv(datei, sep=";")
        df1 = df[( (df.rl == 'bilanz') )]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2=df1.groupby(['jahr']).count().reset_index()
        df3=df2[['jahr']]
    
        for index, row in df3.iterrows():
            jahr=str(row['jahr'])
            jahre_dict[jahr] = jahr

    
    def LeseBilanz(self):
        
        ohs = hs.ZahlenFormatieren() #Klasse für die Zahlendarstellung
        
        #Ermittle die bereits gerechneten Jahre:
        jahre_dict = {}
        self.ErmittleJahreFuerTableVor(jahre_dict)
        
        #dimensioniere die Tabelle:
        anzahlDerJahre = len(jahre_dict)
        self.w.tableWidget_Bilanz.setColumnCount(anzahlDerJahre+1)
        
        anzahlDerPositionen = len(self.listeDerPositionenPassivSeite) + 2 + len(self.listeDerPositionenAktivSeite)
        self.w.tableWidget_Bilanz.setRowCount(anzahlDerPositionen+1)
        
        key_dict = {}
        
        key_dict['rl'] = 'bilanz'
        
        avbg = self.w.comboBox_avbg.currentText()
        key_dict['avbg'] = avbg
        
        #Überschriften für die Jahre:
        irow = 0
        icol = 0
        
        self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(''))
        self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))
        for keyJahr, jahr in jahre_dict.items():
            icol += 1
            self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(jahr))
            self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor(151, 255, 255))

        #Überschriften für die Positione der Passivseite:
        irow = 0
        icol = 0      
        for keyPosition, wertPosition in self.listeDerPositionenPassivSeite.items():    
            irow += 1
            wert = keyPosition
            self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(str(wert)))
            self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor(193, 255, 193))

        # Summe der Passivseite einfügen:
        irow += 1
        wert = 'Summe Passiva'
        self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(str(wert)))
        self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor('gray'))

        #Überschriften für die Positione der Aktivseite:
        for keyPosition, wertPosition in self.listeDerPositionenAktivSeite.items():    
            irow += 1
            wert = keyPosition
            self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(str(wert)))
            self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor(193, 255, 193))

        # Summe der Aktivseite einfügen:
        irow += 1
        wert = 'Summe aktiva'
        self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(str(wert)))
        self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor('gray'))
        
        
        #Werte in die Tabelle schreiben:       
        irow = 0
        icol = 0      

        for keyJahr, jahr in jahre_dict.items():
            key_dict['jahr'] = jahr
            icol += 1
            irow = 0
        
            # Passiseite:
            summe = 0.0
            for keyPosition, wertPosition in self.listeDerPositionenPassivSeite.items():
                irow += 1
                key_dict['name'] = wertPosition[0]
                wert_f = float(self.LeseBilanzCSV(key_dict))
                summe += wert_f
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(wert_s))
            
            # Summer der Passiva ausgeben:
            irow += 1
            wert = ohs.FloatZuStgMitTausendtrennzeichen(summe, 1)
            self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(str(wert)))
            self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor('gray'))
    
            # Aktivseite:    
            summe = 0.0
            for keyPosition, wertPosition in self.listeDerPositionenAktivSeite.items():
                irow += 1
                key_dict['name'] = wertPosition[0]
                wert_f = float(self.LeseBilanzCSV(key_dict))
                summe += wert_f
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(wert_s))
            
            # Summer der Aktivseite ausgeben:
            irow += 1
            wert = ohs.FloatZuStgMitTausendtrennzeichen(summe, 1)
            self.w.tableWidget_Bilanz.setItem(irow, icol, QTableWidgetItem(str(wert)))
            self.w.tableWidget_Bilanz.item(irow, icol).setBackground(QtGui.QColor('gray'))

    
    def LeseBilanzCSV(self, key_dict):
        datei = self.file_bilanz
        df = pd.read_csv(datei, sep=";")
       
        jahr = int(key_dict.get('jahr'))
        rl = str(key_dict.get('rl'))
        avbg = str(key_dict.get('avbg'))
        name = str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.rl==rl) & (df.avbg==avbg) & (df.name==name)]

        if df1.empty:
            wert=0
            text='bilanzEindow/LeseBilanzCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: '+str(key_dict)
            self.oprot.SchreibeInProtokoll(text)
        else:
            if df1.__len__() != 1:
                wert=999999999
                text='bilanzWindow/LeseBilanzCSV: mehrere Eintraeg in der Tabelle gefunden. Es wurde ein Wert von '+str(wert)+ ' verwendet: '+str(key_dict)
                self.oprot.SchreibeInProtokoll(text)
            else:
                index=df1.index[0]
                wert=df1.at[index, 'wert']

        return float(wert)   
    
    
    def SchliesseFenster(self):
        self.w.close()
        
    
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        self.w.comboBox_avbg.activated.connect(self.LeseBilanz)
                
        avbg_liste = []
        avbg_liste = self.ErmittleListeDerAbrechnungsverbaende()
        
        self.w.comboBox_avbg.addItems(avbg_liste)
        self.w.comboBox_avbg.setCurrentText('999')

        self.LeseBilanz()
        self.w.exec_()