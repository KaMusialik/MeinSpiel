# -*- coding: utf-8 -*-

import optionen as opt
import protokoll as prot
import hilfe_statistik as hs

import pandas as pd
import random 
import os
from pathlib import Path


class Nachreservierung():

    def __init__(self, f_dict):
        self.oopt = opt.Optionen(f_dict.get('optionen_file_nachreservierung'))  
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_nachreservierung'))
        
        self.file_nachreservierung = f_dict.get('file_nachreservierung')
        
        self.optionen_file_grundeinstellungen = f_dict.get('optionen_file_grundeinstellungwindow') #hier stehen die Grunddaten bzw. Marktdaten

        self.file_produkt = f_dict.get('file_produkt')
        self.file_produkt_struktur = f_dict.get('file_produkt_struktur')
        
    def LegeTabelleNachreservierungAn(self):
        datei=self.file_nachreservierung
        ocsv=pd.DataFrame()
        ocsv['jahr'] = None
        ocsv['tkz'] = None
        ocsv['name'] = None
        ocsv["wert"] = None
        
        ocsv[['jahr', 'tkz', 'name', 'wert']] = ocsv[['jahr', 'tkz', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='nachreservierun/LegeTabelleVertriebAn: Tabelle fuer Vertrieb/Neugeschäft wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    def LegeFileNachreservierung(self):
        datei= Path(self.file_nachreservierung)
        if datei.is_file():
            text="Nachreservierung/LegeFileNachreservierung " +str(datei)+ " existiert bereits. Daher muss die Datein zuerst entfernt werden."
            print(text)
            self.oprot.SchreibeInProtokoll(text)
            os.remove(datei)
        else:
            print("Nachreservierung/LegeFileNachreservierung: " +str(datei)+ " existiert nicht!!!")   
            
        self.LegeTabelleNachreservierungAn()


    def LeseCsvGrundeinstellung(self, key_dict):
        wert = ""
        file = self.optionen_file_grundeinstellungen
        
        key = key_dict.get('name')
        
        df=pd.read_csv(file, sep=";")
        df1 = df[df.key == key]
        
        if df1.empty:
            wert=""
            text='System/LeseCsvOptinen: Kein Eintrag gefunden. Es wurde null verwendet: key='+str(print(key))
            print(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert

    def ErmittleListeDerTkz(self, jahr):
        datei = self.file_produkt
        df = pd.read_csv(datei, sep=";", dtype = self.file_produkt_struktur)
        
        bis_s = str(jahr) + '12' + '31'
        bis_i = int(bis_s)
        
        df1 = df[(df.bis > bis_i)]

        #zuerst müssen die Jahre ermittelt werden, die in der Tabelle existieren
        df2=df1.groupby(['tkz']).count().reset_index()
        df3=df2[['tkz']]
    
        liste = []
        for index, row in df3.iterrows():
            wert = str(row['tkz'])
            liste.append(wert)
        
            
        return liste

    def SchreibeInTabelleNachreservierung(self, eintrag_dict):
        datei=self.file_nachreservierung
        
        jahr = eintrag_dict.get('jahr')
        tkz = eintrag_dict.get('tkz')
        name = eintrag_dict.get('name')
        wert = eintrag_dict.get('wert')
                
        text = str(jahr) + ';' +str(tkz)+ ';' +str(name) + ';' +str(wert)+'\n'
        
        f=open(datei, "a")
        f.write(text)    
        f.close()     

    def Nachreservierungswert(self, key_dict):
        tkz = key_dict.get('tkz')
        
        ex = 0.1
        
        stat_dict = {}
        stat_dict['risiko'] = 'normal'
        ohs = hs.Hilfe_Statistik(stat_dict)
        zufallszahl = ohs.NeueZufallszahl()
        nv = ohs.Phi(zufallszahl)
        if nv < 0:
            wert = 0
        else:
            wert = nv * ex

        return wert
    
    def StelleNachreservierungFest(self, jahr):
        key = {}
        key['jahr'] = jahr
        key['name'] = 'nachreservierungJaNein'
        nachreservierungJaNein = self.LeseCsvGrundeinstellung(key)
        
        tkz_liste = []
        tkz_liste = self.ErmittleListeDerTkz(jahr)
        
        for tkz in tkz_liste:
            key['tkz'] = tkz
            if nachreservierungJaNein == 'ja':
                key['name'] = 'nachreservierungJaNein'
                key['wert'] = 'ja'
                self.SchreibeInTabelleNachreservierung(key)
                
                nachreservierungswert = self.Nachreservierungswert(key)
            else:
                key['name'] = 'nachreservierungJaNein'
                key['wert'] = 'nein'
                self.SchreibeInTabelleNachreservierung(key)
                
                nachreservierungswert = 0
                
            key['name'] = 'nachreservierungswert'
            key['wert'] = nachreservierungswert
            self.SchreibeInTabelleNachreservierung(key)