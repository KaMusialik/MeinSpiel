# -*- coding: utf-8 -*-
import optionen as opt
import protokoll as prot
import pandas as pd

from pathlib import Path

import PyQt5.uic as uic

class GrundEinstelleungWindow():
    
    def __init__(self, f_dict):
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_grundeinstellungwindow'))

        self.start_dict = {} #hier werden die Startdaten abgelegt
        
        f_opt = f_dict.get('optionen_file_grundeinstellungwindow') #Optionendatei  
        #falls die Datei existiert, dann werden die Daten als Startdaten ausgelesen
        datei= Path(f_opt)
        if datei.is_file():
            text = 'Die Datei ' + f_opt+ ' existiert und die vorhandenen Daten werden als Startdaten ausgelesen.'
            self.oprot.SchreibeInProtokoll(text)
            self.start_dict['file'] = f_opt
            self.LeseStartDatenAusOptionen()
            
        self.oopt = opt.Optionen(f_dict.get('optionen_file_grundeinstellungwindow'))  
        
        self.file_ui = f_dict.get('grundeinstellungwindow_file')
        
        datei= Path(self.file_ui)
        if datei.is_file():
            print("Datei " + self.file_ui+ " existiert.")
            #self.SchreibeInOptionen('file_optionen', self.file_optionen)
            text = 'Die Datei ' +self.file_ui+ ' existiert'
            self.oprot.SchreibeInProtokoll(text)
    
            self.w = uic.loadUi(self.file_ui)
            
        else:
            print("Datei " + self.file_ui + " existiert nicht!!!")   
            self.w = None
            text = 'Die Datei ' +self.file_ui+ ' existiert nicht!'
            self.oprot.SchreibeInProtokoll(text)

    def ZeigeStartWerte(self):
        
        ka_renten_sa = self.start_dict.get('ka_renten_sa')
        if ka_renten_sa == 'normal':
            self.w.radioButton_KA_Risiko_normal.setChecked(True)
        else:
            self.w.radioButton_KA_Risiko_normal.setChecked(False)

        if ka_renten_sa == 'risky':
            self.w.radioButton_KA_Risiko_riskant.setChecked(True)
        else:
            self.w.radioButton_KA_Risiko_riskant.setChecked(False)

        if ka_renten_sa == 'high_risky':
            self.w.radioButton_KA_Risiko_sehr_riskant.setChecked(True)
        else:
            self.w.radioButton_KA_Risiko_sehr_riskant.setChecked(False)

        #Einstellungen zur Streueung im Neugeschäft:
        streuungImNG = self.start_dict.get('streuungImNG')
        if streuungImNG == 'normal':
            self.w.radioButton_StreuungImNG_normal.setChecked(True)
        else:
            self.w.radioButton_StreuungImNG_normal.setChecked(False)

        if streuungImNG == 'gross':
            self.w.radioButton_StreuungImNG_gross.setChecked(True)
        else:
            self.w.radioButton_StreuungImNG_gross.setChecked(False)

        if streuungImNG == 'sehrgross':
            self.w.radioButton_StreuungImNG_sehrgross.setChecked(True)
        else:
            self.w.radioButton_StreuungImNG_sehrgross.setChecked(False)
        
        
        wert = self.start_dict.get('beitragMarktRente')
        self.w.lineEdit_BeitragRente.setText(wert)

        wert = self.start_dict.get('provisionMarktRente')
        self.w.lineEdit_ProvisionRente.setText(wert)        

        wert = self.start_dict.get('anzahlRente')
        self.w.lineEdit_AnzahlRente.setText(wert)        
        
        wert = self.start_dict.get('beitragMarktBu')
        self.w.lineEdit_BeitragBu.setText(wert)

        wert = self.start_dict.get('provisionMarktBu')
        self.w.lineEdit_ProvisionBu.setText(wert)

        wert = self.start_dict.get('anzahlBu')
        self.w.lineEdit_AnzahlBu.setText(wert)
    
    def LeseStartDatenAusOptionen(self):
        file = self.start_dict.get('file')
        
        #Wert für Kapitalanlagen Renten:
        key = 'ka_renten_sa'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert

        #Streuung im Neugeschäft:
        key = 'streuungImNG'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert
        
        #Wert für Beitrag Renten:
        key = 'beitragMarktRente'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert

        #Wert für Beitrag Bu:
        key = 'beitragMarktBu'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert

        #Wert für Provison Renten:
        key = 'provisionMarktBu'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert

        #Wert für Provison Renten:
        key = 'provisionMarktRente'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert

        #Wert für Anzahl Renten:
        key = 'anzahlRente'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert

        #Wert für Anzahl BU:
        key = 'anzahlBu'
        wert = self.LeseCsvOptinen(file, key)
        self.start_dict[key] = wert
    
    def LeseCsvOptinen(self, file, key):
        wert = ""
        df=pd.read_csv(file, sep=";")
        df1 = df[df.key == key]
        
        if df1.empty:
            wert=""
            text='Grundeinstellungwindow/LeseCsvOptinen: Kein Eintrag gefunden. Es wurde null verwendet: key='+str(print(key))
            print(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert       
    
    def LeseDatenAusFenster(self):
        
        #hier werden die Informationen aus dem Dialog ausgelesen und in die Datei Optionen reingeschrieben:
        if self.w.radioButton_KA_Risiko_normal.isChecked():
            ka_renten_sa = 'normal'
        elif self.w.radioButton_KA_Risiko_riskant.isChecked():
            ka_renten_sa = 'risky'
        elif self.w.radioButton_KA_Risiko_sehr_riskant.isChecked():
            ka_renten_sa = 'high_risky'
        else:
            ka_renten_sa = 'normal'
            text = 'Grundeinstellungwindow/LeseDatenAusFenster: Das Risiko in der Kapitalanlage in den Renten konnte nicht zugerdnet werden. Es wurde daher festgelegt: ' + str(ka_renten_sa)
            self.oprot.SchreibeInProtokoll(text)

        text = 'Grundeinstellungwindow/LeseDatenAusFenster: Das Risiko in der Kapitalanlage in den Renten wurde festgelegt: ' + str(ka_renten_sa)   
        self.oprot.SchreibeInProtokoll(text)
        
        key = 'ka_renten_sa'
        text = str(ka_renten_sa)   
        self.oopt.SchreibeInOptionen(key, text)
        
        beitragMarktRente = self.w.lineEdit_BeitragRente.text()
        key = 'beitragMarktRente'
        text = beitragMarktRente
        self.oopt.SchreibeInOptionen(key, text)

        provisionMarktRente = self.w.lineEdit_ProvisionRente.text()
        key = 'provisionMarktRente'
        text = provisionMarktRente
        self.oopt.SchreibeInOptionen(key, text)

        anzahlRente = self.w.lineEdit_AnzahlRente.text()
        key = 'anzahlRente'
        text = anzahlRente
        self.oopt.SchreibeInOptionen(key, text)

        beitragMarktBu = self.w.lineEdit_BeitragBu.text()
        key = 'beitragMarktBu'
        text = beitragMarktBu
        self.oopt.SchreibeInOptionen(key, text)
        
        provisionMarktBu = self.w.lineEdit_ProvisionBu.text()
        key = 'provisionMarktBu'
        text = provisionMarktBu
        self.oopt.SchreibeInOptionen(key, text)

        anzahlBu= self.w.lineEdit_AnzahlBu.text()
        key = 'anzahlBu'
        text = anzahlBu
        self.oopt.SchreibeInOptionen(key, text)
        
        if self.w.radioButton_StreuungImNG_normal.isChecked():
            streuungImNG = 'normal'
        elif self.w.radioButton_StreuungImNG_gross.isChecked():
            streuungImNG = 'gross'
        elif self.w.radioButton_StreuungImNG_sehrgross.isChecked():
            streuungImNG = 'sehrgross'
        else:
            streuungImNG = 'normal'
            text = 'Grundeinstellungwindow/LeseDatenAusFenster: Die Streuung im Neugeschäft konnte nicht zugerdnet werden. Es wurde daher festgelegt: ' + str(streuungImNG)
            self.oprot.SchreibeInProtokoll(text)
            
        key = 'streuungImNG'
        text = str(streuungImNG)   
        self.oopt.SchreibeInOptionen(key, text)
        
        self.SchliesseFenster()
        
    def SchliesseFenster(self):
        self.w.close()
        
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.LeseDatenAusFenster)
        self.ZeigeStartWerte()
        
        self.w.exec_()
    
        