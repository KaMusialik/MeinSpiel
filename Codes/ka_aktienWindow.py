# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
import ka_aktienCSV

from pathlib import Path

import hilfe_system as hs

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class KA_AktienWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_ka_aktienWindow'))      

        self.file = f_dict.get('file_kapitalanlagen_aktien_csv')
        datei = Path(self.file)
        if datei.is_file():
            text = 'KA_AktienWindow/init: Die Datei ' + self.file + ' existiert'
            print(text)
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'KA_AktienWindow/init: Die Datei ' + self.file + ' existiert nicht!'
            print(text)
            self.oprot.SchreibeInProtokoll(text)
        
        
        self.file_struktur = f_dict.get('file_aktien_csv_struktur')

        
        self.file_ui = f_dict.get('ui_ka_aktienWindow_file')
        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'KA_AktienWindow/init: Die Datei ' + self.file_ui + ' existiert'
            print(text)
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'KA_AktienWindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
            print(text)
        
        self.listeDerPositionenAktienKurs = { 'Kurs Anfang': ('kurs_anfang', 1),
                                    '+ Kursveränderung':('kurs_veraenderung', 101),
                                    '= Kurs Ende':('kurs_ende', 201)
                                  }
        
        self.listeDerPositionenAktienAnteile = { 'Anteile Anfang': ('anteile_anfang', 501),
                                    '+ neue Anteile':('anteile_neu', 601),
                                    '= Anteile Ende':('anteile_ende', 801)
                                  }
        
        self.w.setWindowTitle('Aktien ...')
        self.ka_aktienCSV = ka_aktienCSV.KA_AktienCSV(f_dict)
    
    def ErmittleJahreFuerTableVor(self, jahre_dict):
 
        datei = self.file
        struktur = self.file_struktur
        
        df = pd.read_csv(datei, sep=";", dtype=struktur)

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df1 = df.groupby(['jahr']).count().reset_index()
        df2 = df1[['jahr']]
    
        for index, row in df2.iterrows():
            jahr=str(row['jahr'])
            jahre_dict[jahr] = jahr

    
    def LeseTabelle(self):
        
        ohs = hs.ZahlenFormatieren() #Klasse für die Zahlendarstellung
        
        #Ermittle die bereits gerechneten Jahre:
        jahre_dict = {}
        self.ErmittleJahreFuerTableVor(jahre_dict)
        
        #dimensioniere die Tabelle:
        anzahlDerJahre = len(jahre_dict)
        objekt = self.w.tableWidget_ka_aktienWindow

        objekt.setColumnCount(anzahlDerJahre + 1)
        
        anzahlDerPositionen = len(self.listeDerPositionenAktienKurs) + 1 + len(self.listeDerPositionenAktienAnteile)
        objekt.setRowCount(anzahlDerPositionen + 1)
        
        key_dict = {}
        
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
        # Kurs:
        irow = 0
        icol = 0      
        for keyPosition, wertPosition in self.listeDerPositionenAktienKurs.items():    
            irow += 1
            wert = keyPosition
            objekt.setItem(irow, icol, QTableWidgetItem(str(wert)))
            objekt.item(irow, icol).setBackground(QtGui.QColor(193, 255, 193))        
        
        # leere Zeile:
        irow += 1
        wert = ''
        objekt.setItem(irow, icol, QTableWidgetItem(str(wert)))
        objekt.item(irow, icol).setBackground(QtGui.QColor('gray'))        
        
        # Anteile:
        for keyPosition, wertPosition in self.listeDerPositionenAktienAnteile.items():    
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
            
            # Kurs:
            for keyPosition, wertPosition in self.listeDerPositionenAktienKurs.items():
                irow += 1
                key_dict['name'] = wertPosition[0]
                wert_f = float(self.ka_aktienCSV.LeseWertAusCSV(key_dict))
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                objekt.setItem(irow, icol, QTableWidgetItem(wert_s))

            # leere Zeile:
            irow += 1
            wert = ''
            objekt.setItem(irow, icol, QTableWidgetItem(str(wert)))
            objekt.item(irow, icol).setBackground(QtGui.QColor('gray'))        
            
            # Anteile:
            for keyPosition, wertPosition in self.listeDerPositionenAktienAnteile.items():    
                irow += 1
                key_dict['name'] = wertPosition[0]
                wert_f = float(self.ka_aktienCSV.LeseWertAusCSV(key_dict))
                wert_s = ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
                objekt.setItem(irow, icol, QTableWidgetItem(wert_s))

    
    def SchliesseFenster(self):
        self.w.close()
        
    
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
                        
        self.LeseTabelle()
        
        self.w.exec_()


