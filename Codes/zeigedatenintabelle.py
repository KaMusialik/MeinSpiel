# -*- coding: utf-8 -*-

import pandas as pd

from PyQt5.QtWidgets import QTableWidgetItem

class ZeigeDatnInTabelle():

    def __init__(self, tabelle):
        self.tabelle = tabelle
    
    def SchreibeDatenIntabelle(self, filedaten):
        self.daten = filedaten
    
        infoCSV_dict = {}
        self.LeseInfosDerDaten(infoCSV_dict)
        
        anzahlDerSpalten = int(infoCSV_dict.get('anzahlDerSpalten'))
        
        anzahDerZeilen = int(infoCSV_dict.get('anzahDerZeilen'))
        
        #dimensioniere die Tabelle:
        self.tabelle.setRowCount(anzahDerZeilen)
        self.tabelle.setColumnCount(anzahlDerSpalten)

        datei = self.daten
        df = pd.read_csv(datei, sep=";")
        
        irow = -1
        icol = 0
        for index, row in df.iterrows():
            irow += 1
            icol = -1
            for x in row:
                icol += 1
                x_s = str(x)
                self.tabelle.setItem(irow, icol, QTableWidgetItem(x_s))
        
    def LeseInfosDerDaten(self, infoCSV_dict):
        datei = self.daten
        
        df = pd.read_csv(datei, sep=";")
        infoCSV_dict['anzahlDerSpalten'] = len(df.columns)
        
        infoCSV_dict['anzahDerZeilen'] = len(df)
        
        