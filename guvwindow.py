# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd


from pathlib import Path

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

        self.listeDerPositionen = {'Gebuchter Beitrag':1}


    def SchliesseFenster(self):
        self.w.close()
        
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.SchliesseFenster)
        
        self.w.exec_()