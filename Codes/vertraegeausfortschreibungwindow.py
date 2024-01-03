# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd


from pathlib import Path

import PyQt5.uic as uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import QtGui

class VertraegeAusFortschreibungWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_vertraegeausderfortschreibungwindow'))
        
        self.file_fortschreibung = f_dict.get('file_system_fortschreibung')
        self.file_fortschreibung_struktur = f_dict.get('file_system_fortschreibung_struktur')
        
        datei = Path(self.file_fortschreibung)
        if datei.is_file():
            text = 'VertraegeAusFortschreibungWindow/init: Die Datei ' + self.file_fortschreibung + ' existiert'
            self.oprot.SchreibeInProtokoll(text)
        else:
            text = 'VertraegeAusFortschreibungWindow/init: Die Datei ' + self.file_fortschreibung + ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)
      
        self.file_ui = f_dict.get('fortschreibungwindow_file')

        datei= Path(self.file_ui)
        if datei.is_file():
            text = 'VertraegeAusFortschreibungWindow/init: Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            self.w = None
            text = 'VertraegeAusFortschreibungWindow/init: Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

        self.w.setWindowTitle('Verträge aus der Fortschreibung')

    
    def VsnrDictZuTree(self, vsnrDict):
        anzahlDerEintraege = len(vsnrDict)
        if anzahlDerEintraege == 0:
            print(f"VsnrDictZuTree: keine Einträge vorhanden: {vsnrDict}")
            return

        self.w.treeWidget_vsnrDict.clear()
        self.w.treeWidget_vsnrDict.setHeaderLabels(["Name", "Wert"])

        items = []
        for key, value in vsnrDict.items():
            item = self.GetChildTreeAusDict(key, value)
            items.append(item)

        self.w.treeWidget_vsnrDict.insertTopLevelItems(0, items)

    def GetChildTreeAusDict(self, key, myDict):
        if isinstance(myDict, dict):
            
            item = QtWidgets.QTreeWidgetItem([key])

            for keyDict, valueDict in myDict.items():
                child = self.GetChildTreeAusDict(keyDict, valueDict)
                item.addChild(child)

            return item

        else:
            #print(f'GetChildTreeAusDict: es wird ein Dictonary erwartet. Es wurde aber übertragen: {myDict}')
            item = QtWidgets.QTreeWidgetItem([key, str(myDict)])
            return item
        
        
    def LeseVertrag(self):
        #hier werden alle gefilterte Informationen zum Vertrag ausgegeben:
    
        #lese Filter:    
        vsnr = str(self.w.comboBox_vertrag.currentText())
        
        datei = self.file_fortschreibung
        struktur = self.file_fortschreibung_struktur
        
        df = pd.read_csv(datei, sep=";", dtype = struktur)
        df1 = df[( (df.vsnr == vsnr) )]
        
        # die Daten aud demDateframe müssen in ein Dict gebracht werden, damit sie später in ein Tree im Dialog angezeigt werden:
        vertragDict = {}
        vertragDict[vsnr] = {}
        listeDict = []
        i = 0
        for index, row in df1.iterrows():
            von = str(row['von'])
            bis = str(row['bis'])
            keyDict = von + '_' + bis
            if keyDict not in vertragDict[vsnr]:
                vertragDict[vsnr][keyDict] =  {}

            name = row['name']
            wert = row['wert']

            vertragDict[vsnr][keyDict][name] = wert

        self.VsnrDictZuTree(vertragDict)
    
    def SchliesseFenster(self):
        self.w.close()
        
    
    def ErmittleListeDerAktivenVertraege(self):
        datei = self.file_fortschreibung
        struktur = self.file_fortschreibung_struktur
        
        df = pd.read_csv(datei, sep=";", dtype = struktur)
                
        df2=df.groupby(['vsnr']).count().reset_index()
        df3=df2[['vsnr']]
    
        liste = []
        for index, row in df3.iterrows():
            wert = str(row['vsnr'])
            liste.append(wert)
                    
        return liste    
    
    
    def RufeFensterAuf(self, jahr):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        self.w.comboBox_vertrag.activated.connect(self.LeseVertrag)
        
        vsnr_liste = []
        vsnr_liste = self.ErmittleListeDerAktivenVertraege()
        self.w.comboBox_vertrag.addItems(vsnr_liste)
       
        self.LeseVertrag()
        self.w.exec_()