# -*- coding: utf-8 -*-
import optionen as opt
import protokoll as prot
import pandas as pd
import oeffnePDF as pdf
import optionen_grundeinstellungCSV

import hilfe_system as hs

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
        
            
        #self.oopt = opt.Optionen(f_dict.get('optionen_file_grundeinstellungwindow'))  
        
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
            
        self.ohs = hs.ZahlenFormatieren()
    
        self.optionenCSV = optionen_grundeinstellungCSV.Optionen_GrundeinstellungCSV(f_dict)
        
        startwertDarlehenszins = 5
        self.w.horizontalSlider_Darlehenszins.setMinimum(0)
        self.w.horizontalSlider_Darlehenszins.setMaximum(10)
        self.w.horizontalSlider_Darlehenszins.setValue(int(startwertDarlehenszins))
        self.w.horizontalSlider_Darlehenszins.valueChanged.connect(self.DarlehenszinsSlider)
        self.w.label_Darlehenszins.setText(str(startwertDarlehenszins))


        self.infoDict = {}
        verzeichnis = f_dict.get('work_dir') + 'Dokumente/'
        self.infoDict['RisikoInKapitalanlage'] = verzeichnis + 'Dialog_1_RisikoInDerKapitalanlage.pdf'
        self.w.pushButton_Info_RisikoInKapitalanlage.clicked.connect(self.InfoRisikoInKapitalanlage)
        self.w.setWindowTitle = 'Einstellungen/Startparameter'

        # fix-Kosten:
        self.w.horizontalSlider_fixkosten.setMinimum(0)
        self.w.horizontalSlider_fixkosten.setMaximum(10)
        self.w.horizontalSlider_fixkosten.setValue(int(2))
        self.w.horizontalSlider_fixkosten.valueChanged.connect(self.HorizontalSlider_fixkosten)
        # iAK:
        self.w.horizontalSlider_iak.setMinimum(0)
        self.w.horizontalSlider_iak.setMaximum(20)
        self.w.horizontalSlider_iak.setValue(int(10))
        self.w.horizontalSlider_iak.valueChanged.connect(self.HorizontalSlider_iak)
        # fix-Kosten:
        self.w.horizontalSlider_vk_stueck.setMinimum(0)
        self.w.horizontalSlider_vk_stueck.setMaximum(50)
        self.w.horizontalSlider_vk_stueck.setValue(int(20))
        self.w.horizontalSlider_vk_stueck.valueChanged.connect(self.HorizontalSlider_vk_stueck)

        self.LeseStartDatenAusOptionen()

    def HorizontalSlider_fixkosten(self):
        betrag = self.w.horizontalSlider_fixkosten.value()
        self.w.label_fixkosten.setText(str(betrag))


    def HorizontalSlider_vk_stueck(self):
        betrag = self.w.horizontalSlider_vk_stueck.value()
        self.w.label_vk_stueck.setText(str(betrag))


    def HorizontalSlider_iak(self):
        betrag = self.w.horizontalSlider_iak.value()
        self.w.label_iak.setText(str(betrag))


    def DarlehenszinsSlider(self):
        betrag = self.w.horizontalSlider_Darlehenszins.value()
        self.w.label_Darlehenszins.setText(str(betrag))


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

        #Einstellungen zur Nachreservierung:
        nachreservierungJaNein = self.start_dict.get('nachreservierungJaNein')
        if nachreservierungJaNein == 'ja':
            self.w.radioButton_nachreservierung_ja.setChecked(True)
            self.w.radioButton_nachreservierung_nein.setChecked(False)
        else:
            self.w.radioButton_nachreservierung_ja.setChecked(False)
            self.w.radioButton_nachreservierung_nein.setChecked(True)

        if streuungImNG == 'gross':
            self.w.radioButton_StreuungImNG_gross.setChecked(True)
        else:
            self.w.radioButton_StreuungImNG_gross.setChecked(False)

        if streuungImNG == 'sehrgross':
            self.w.radioButton_StreuungImNG_sehrgross.setChecked(True)
        else:
            self.w.radioButton_StreuungImNG_sehrgross.setChecked(False)
        
        
        wert_s = self.start_dict.get('provisionMarktRente')
        if wert_s == '':
            wert_s = '0'
            
        wert_f = float(wert_s) * 1000
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f, 1)
        self.w.lineEdit_ProvisionRente.setText(wert_s)        

        wert_s = self.start_dict.get('anzahlMarktRente')
        if wert_s == '':
            wert_s = '0'

        wert_f = float(wert_s)
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f,1)
        self.w.lineEdit_AnzahlRente.setText(wert_s)        
        
        wert_s = self.start_dict.get('provisionMarktBu')
        if wert_s == '':
            wert_s = '0'

        wert_f = float(wert_s) * 1000
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f,1)
        self.w.lineEdit_ProvisionBu.setText(wert_s)

        wert_s = self.start_dict.get('anzahlMarktBu')
        if wert_s == '' or wert_s == None:
            wert_s = '0'

        wert_f = float(wert_s)
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f,1)
        self.w.lineEdit_AnzahlBu.setText(wert_s)

        # Wert für Fixkosten:
        key = 'fixkosten'
        wert_s = self.start_dict.get(key)
        if wert_s == '' or wert_s == None:
            wert_s = '0.0'
        
        wert_f = float(wert_s) / 1000000.0
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f,1)
        self.w.label_fixkosten.setText(wert_s)
    
        # Wert für iAK:
        key = 'iak'
        wert_s = self.start_dict.get(key)
        if wert_s == '' or wert_s == None:
            wert_s = '0.0'
        
        wert_f = float(wert_s) * 1000.0
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f,1)
        self.w.label_iak.setText(wert_s)

        # Wert für vk_stueck:
        key = 'vk_stueck'
        wert_s = self.start_dict.get(key)
        if wert_s == '' or wert_s == None:
            wert_s = '0.0'
        
        wert_f = float(wert_s)
        wert_s = self.ohs.FloatZuStgMitTausendtrennzeichen(wert_f,1)
        self.w.label_vk_stueck.setText(wert_s)
    
    
    def LeseStartDatenAusOptionen(self):
        keyDict = {}
        
        #Wert für Kapitalanlagen Renten:
        
        key = 'ka_renten_sa'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Streuung im Neugeschäft:
        key = 'streuungImNG'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()
        
        #Wert für Provison Renten:
        key = 'provisionMarktBu'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Wert für Provison Renten:
        key = 'provisionMarktRente'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Wert für Anzahl Renten:
        key = 'anzahlMarktRente'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Wert für Anzahl BU:
        key = 'anzahlMarktBu'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Wert für Anzahl BU:
        key = 'nachreservierungJaNein'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Wert für Fixkosten:
        key = 'fixkosten'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

        #Wert für iAK:
        key = 'iAK'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()
        
        #Wert für vk_Stueck:
        key = 'vk_stueck'
        keyDict['key'] = key
        wert = self.optionenCSV.LeseWertAusCSV(keyDict)
        self.start_dict[key] = wert
        keyDict.clear()

    
    def LeseDatenAusFenster(self):
        
        keyDict = {}  # hier werden die Daten abgelegt, die in die Tabelle Optionen reingeschrieben müssen
        
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
        
        # einstellung zu den Rentenpapieren:
        key = 'ka_renten_sa'
        text = str(ka_renten_sa)   
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()

        # Einstellung zu Aktien:
        key = 'ka_aktien_sa'
        text = str(ka_renten_sa)   
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()
        
        wert_s = self.w.lineEdit_ProvisionRente.text()
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s) / 1000
        key = 'provisionMarktRente'
        text = str(wert_f)
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()

        wert_s = self.w.lineEdit_AnzahlRente.text()
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s) 
        key = 'anzahlMarktRente'
        text = str(wert_f)
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()
       
        wert_s = self.w.lineEdit_ProvisionBu.text()
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s) / 1000
        key = 'provisionMarktBu'
        text = str(wert_f)
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()

        wert_s = self.w.lineEdit_AnzahlBu.text()
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s) 
        key = 'anzahlMarktBu'
        text = str(wert_f)
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()
        
        if self.w.radioButton_StreuungImNG_normal.isChecked():
            streuungImNG = 'normal'
        elif self.w.radioButton_StreuungImNG_gross.isChecked():
            streuungImNG = 'gross'
        elif self.w.radioButton_StreuungImNG_sehrgross.isChecked():
            streuungImNG = 'sehrgross'
        elif self.w.radioButton_keineStreuungImNeugeschaeft.isChecked():
            streuungImNG = 'keine Streuung'
        else:
            streuungImNG = 'normal'
            text = 'Grundeinstellungwindow/LeseDatenAusFenster: Die Streuung im Neugeschäft konnte nicht zugerdnet werden. Es wurde daher festgelegt: ' + str(streuungImNG)
            self.oprot.SchreibeInProtokoll(text)
            
        key = 'streuungImNG'
        text = str(streuungImNG)   
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()
        
        ### Nachreservierung:
        key = 'nachreservierungJaNein'
        if self.w.radioButton_nachreservierung_ja.isChecked():
            nachreservierungJaNein= 'ja'
        else:
            nachreservierungJaNein= 'nein'
            
        text = str(nachreservierungJaNein)   
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()
        
        ### Ende Nachreservierung
        
        ### Darlehenszins:
        key = 'darlehenszins'
        wert = float(self.w.label_Darlehenszins.text())/100.0
        text = str(wert)   
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()

        ### Ende Darlehenszins

        ### Kosten:
        # Fixkosten:
        key = 'fixkosten'
        wert_s = str(self.w.label_fixkosten.text())
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s) * 1000000.0  # Wert auf der Maske ist in Mio.
        text = str(wert_f)   
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()

        # iAK:
        key = 'iAK'
        wert_s = str(self.w.label_iak.text())
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s) / 1000.0  # Wert auf der Maske ist in Promille
        text = str(wert_f)     
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()

        # vk_stueck:
        key = 'vk_stueck'
        wert_s = str(self.w.label_vk_stueck.text())
        wert_f = self.ohs.StgMitTausendtrennzeichenZuFloat(wert_s)  # Wert auf der Maske ist in Euro
        text = str(wert_f)     
        keyDict['key'] = key
        keyDict['wert'] = text
        self.optionenCSV.SchreibeInCSV(keyDict)
        keyDict.clear()


        ### Ende Kosten
        
        
        
        self.SchliesseFenster()
    

    def InfoRisikoInKapitalanlage(self):
        filePDF = self.infoDict.get('RisikoInKapitalanlage')
        opdf = pdf.OeffnePDF(filePDF)
    
    
    def SchliesseFenster(self):
        self.w.close()
        
    
    def RufeFensterAuf(self):
        self.w.pushButton_weiter.clicked.connect(self.LeseDatenAusFenster)
        self.ZeigeStartWerte()
        
        self.w.exec_()
    
        