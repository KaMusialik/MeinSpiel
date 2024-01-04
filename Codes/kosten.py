# -*- coding: utf-8 -*-

import protokoll as prot
import hilfe_statistik as hs

import pandas as pd
import random 
import os
from pathlib import Path


class Kosten():

    def __init__(self, f_dict):
        self.optionen_file_kosten = f_dict.get('optionen_file_kosten')  
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_kosten'))
        
        self.file_kosten = f_dict.get('file_kosten')
        self.file_kosten_struktur = f_dict.get('file_kosten_struktur')
        
        self.file_system_fortfreibung = f_dict.get('file_system_fortschreibung')
        self.file_system_fortschteibung_struktur = f_dict.get('file_system_fortschreibung_struktur')
    
    
    def LegeTabelleKostenAn(self):
        datei = self.file_kosten
        ocsv = pd.DataFrame()
        ocsv['jahr'] = None
        ocsv['vsnr'] = None
        ocsv['avbg'] = None
        ocsv['name'] = None
        ocsv["wert"] = None
        
        ocsv[['jahr', 'vsnr', 'avbg', 'name', 'wert']] = ocsv[['jahr', 'vsnr', 'avbg', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='Kosten/LegeTabelleKostenAn: Tabelle fuer Kosten wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)
        
    
    def LegeFileKosten(self):
        datei= Path(self.file_kosten)
        if datei.is_file():
            text="Kosten/LegeFileKosten " +str(datei)+ " existiert bereits. Daher muss die Datein zuerst entfernt werden."
            print(text)
            self.oprot.SchreibeInProtokoll(text)
            os.remove(datei)
        else:
            print("Kosten/LegeFileKosten: " +str(datei)+ " existiert nicht!!!")   
            
        self.LegeTabelleKostenAn()
        
    
    def ErmittleListeDerAktivenVertraege(self, jahr):
        datei = self.file_system_fortfreibung
        struktur = self.file_system_fortschteibung_struktur
        
        df = pd.read_csv(datei, sep=";", dtype = struktur)
        
        bis_s = str(jahr) + '12' + '31'
        bis_i = int(bis_s)
        
        df1 = df[(df.bis == bis_i)]

        df2=df1.groupby(['vsnr']).count().reset_index()
        df3=df2[['vsnr']]
    
        liste = []
        for index, row in df3.iterrows():
            wert = str(row['vsnr'])
            liste.append(wert)
                    
        return liste
    
    
    def LeseVertragAusFortschreibung(self, vtg_dict, jahr):
        datei = self.file_system_fortfreibung
        struktur = self.file_system_fortschteibung_struktur
        
        df = pd.read_csv(datei, sep=";", dtype = struktur)
        
        vsnr = str(vtg_dict.get('vsnr'))
        
        #jahr = vtg_dict.get('jahr')        
        bis_s = str(jahr) + '12' + '31'
        bis_i = int(bis_s)
        
        df1 = df[(df.bis == bis_i) & (df.vsnr == vsnr)]
        
        for index, row in df1.iterrows():
            name = str(row['name'])
            wert = str(row['wert'])
            
            vtg_dict[name] = wert

        return vtg_dict
    
    
    def LeseAusOptionenCSV(self, key_dict):
        datei = self.optionen_file_kosten
        df = pd.read_csv(datei, sep=";")
        
        name = str(key_dict.get('name')).replace(' ', '')
        avbg = str(key_dict.get('avbg')).replace(' ', '')

        df1 = df[((df.name == name) & (df.avbg == avbg))]
        
        if df1.empty:
            wert=0
            text='In der OptionenKostentabelle: ' + datei + ' zu den Daten: ' +str(key_dict ) + ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
 
        return wert

    
    def LeseAusKostenCSV(self, key_dict):
        datei = self.file_kosten
        struktur = self.file_kosten_struktur
        
        df = pd.read_csv(datei, sep=";",  dtype = struktur)
        
        jahr = int(key_dict.get('jahr'))
        vsnr = int(key_dict.get('vsnr'))
        avbg = str(key_dict.get('avbg'))
        name = str(key_dict.get('name'))

        df1 = df[( (df.jahr == jahr) & (df.vsnr == vsnr) & (df.name == name) & (df.avbg == avbg))]
        
        if df1.empty:
            wert=0
            text='In der Kostentabelle: ' + datei + ' zu den Daten: ' +str(key_dict ) + ' wurden keine Daten gefunden'
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
 
        return wert
    
    
    def Rechne_iAK(self, vtg_dict):
        key_dict = {}
        key_dict['avbg'] = vtg_dict.get('avbg')
        key_dict['name'] = 'iAK'
        
        satz_iAK = float(self.LeseAusOptionenCSV(key_dict))
        bs = float(vtg_dict.get('beitragssumme'))
        anzahl = float(vtg_dict.get('anzahl'))
        
        vtg_dict['iAK'] = satz_iAK * bs * anzahl
 
        
        return vtg_dict
    
    
    def SchreibeInKosten(self, eintrag_dict):
        datei = self.file_kosten
        
        jahr = eintrag_dict.get('jahr')
        vsnr = eintrag_dict.get('vsnr')
        avbg = eintrag_dict.get('avbg')
        name = eintrag_dict.get('name')
        wert = eintrag_dict.get('wert')
                
        text = str(jahr) + ';' + str(vsnr) + ';' + str(avbg) + ';' + str(name) + ';' + str(wert) + '\n'
        
        f=open(datei, "a")
        f.write(text)    
        f.close()     

    
    def RechneVerwaltungskostenStueck(self, vtg_dict):
        key_dict = {}
        key_dict['avbg'] = vtg_dict.get('avbg')
        key_dict['name'] = 'VK_Stueck'
        
        satz = float(self.LeseAusOptionenCSV(key_dict))
        anzahl = float(vtg_dict.get('anzahl'))
        
        vtg_dict['VK_Stueck'] = satz * anzahl
 
        return vtg_dict

    
    def ErmittleKosten(self, jahr):
        listeVertraege = []
        listeVertraege = self.ErmittleListeDerAktivenVertraege(jahr)  # Liste aller aktiven Verträge
        
        eintrag_dict = {}
        vtg_dict = {}    
        
        for vsnr in listeVertraege:  # jetzt werden aller aktiven aus der Liste nacheinander abgearbeitet:
            vtg_dict.clear()
            eintrag_dict.clear()
            vtg_dict['vsnr'] = str(vsnr)
            eintrag_dict['vsnr'] = str(vsnr)
            eintrag_dict['jahr'] = str(jahr)
            vtg_dict = self.LeseVertragAusFortschreibung(vtg_dict, jahr)
            
            #interne Abschlusskosten:
            eintrag_dict['name'] = 'iAK'
            
            if ((vtg_dict.get('gevo') == 'Neuzugang') and (int(vtg_dict.get('jahr')) == int(jahr))):
                
                vtg_dict = self.Rechne_iAK(vtg_dict)
            
                eintrag_dict['avbg'] = vtg_dict.get('avbg')            
                eintrag_dict['wert'] = vtg_dict.get('iAK')
            else:
                eintrag_dict['avbg'] = vtg_dict.get('avbg')            
                eintrag_dict['wert'] = 0.0
                
            
            self.SchreibeInKosten(eintrag_dict)
            
            #Verwaltungskosten Stückkosten:
            eintrag_dict['name'] = 'VK_Stueck'
            
            vtg_dict = self.RechneVerwaltungskostenStueck(vtg_dict)
            eintrag_dict['avbg'] = vtg_dict.get('avbg')            
            eintrag_dict['wert'] = vtg_dict.get('VK_Stueck')
            self.SchreibeInKosten(eintrag_dict)
            