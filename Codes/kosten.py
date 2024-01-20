# -*- coding: utf-8 -*-

import protokoll as prot
import hilfe_statistik as hs
import optionen_grundeinstellungCSV
import kostenCSV

import pandas as pd
import random 
import os
from pathlib import Path


class Kosten():

    def __init__(self, f_dict):
        self.optionenCSV = optionen_grundeinstellungCSV.Optionen_GrundeinstellungCSV(f_dict) 
        self.kostenCSV = kostenCSV.KostenCSV(f_dict)
        
        self.oprot = prot.Protokoll(f_dict.get('protokoll_file_kosten'))
        
        self.file_kosten = f_dict.get('file_kosten')
        self.file_kosten_struktur = f_dict.get('file_kosten_struktur')
        
        self.file_system_fortfreibung = f_dict.get('file_system_fortschreibung')
        self.file_system_fortschteibung_struktur = f_dict.get('file_system_fortschreibung_struktur')

        self.LegeFileKosten()
        self.fixkosten = 0.0  # fixer Betrag in Euro
        self.iak = 0.0  # in %0 der BS
        self.vk_stueck = 0.0  # in Euro

        self.InitalisiereKosten()  # hier werden die Kostensätze aus optionen gelesen
    
    def InitalisiereKosten(self):  # hier werden die Kosten aus Optionen gelesen
        keyOptionenDict = {}
        
        # Fixkosten:
        key = 'fixkosten'
        keyOptionenDict['key'] = key
        wert_s = self.optionenCSV.LeseWertAusCSV(keyOptionenDict)
        wert_f = float(wert_s)
        self.fixkosten = wert_f
        keyOptionenDict.clear()

        # iAK:
        key = 'iak'
        keyOptionenDict['key'] = key
        wert_s = self.optionenCSV.LeseWertAusCSV(keyOptionenDict)
        wert_f = float(wert_s)
        self.iak = wert_f
        keyOptionenDict.clear()

        # vk_stueck:
        key = 'vk_stueck'
        keyOptionenDict['key'] = key
        wert_s = self.optionenCSV.LeseWertAusCSV(keyOptionenDict)
        wert_f = float(wert_s)
        self.vk_stueck = wert_f
        keyOptionenDict.clear()
    
    
    def LegeTabelleKostenAn(self):
        self.kostenCSV.LegeTabelleKostenCSVAn()
        
        datei = self.file_kosten
        text='Kosten/LegeTabelleKostenAn: Tabelle fuer Kosten wurde angelegt: ' + str(datei)
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

    
    def Rechne_iAK(self, vtg_dict):
        key_dict = {}
        key_dict['avbg'] = vtg_dict.get('avbg')
        key_dict['name'] = 'iAK'
        
        satz_iAK = self.iak
        bs = float(vtg_dict.get('beitragssumme'))
        anzahl = float(vtg_dict.get('anzahl'))
        
        vtg_dict['iAK'] = satz_iAK * bs * anzahl
 
        
        return vtg_dict
    
    
    def RechneVerwaltungskostenStueck(self, vtg_dict):
        key_dict = {}
        key_dict['avbg'] = vtg_dict.get('avbg')
        key_dict['name'] = 'VK_Stueck'
        
        satz = self.vk_stueck
        anzahl = float(vtg_dict.get('anzahl'))
        
        vtg_dict['VK_Stueck'] = satz * anzahl
 
        return vtg_dict


    def RechneFixkosten(self, vtg_dict):
        key_dict = {}
        key_dict['avbg'] = vtg_dict.get('avbg')
        key_dict['name'] = 'fixkosten'
        
        vtg_dict['fixkosten'] = self.file_kosten
 
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
                
            
            self.kostenCSV.SchreibeInKosten(eintrag_dict)
            
            #Verwaltungskosten Stückkosten:
            eintrag_dict['name'] = 'VK_Stueck'
            
            vtg_dict = self.RechneVerwaltungskostenStueck(vtg_dict)
            eintrag_dict['avbg'] = vtg_dict.get('avbg')            
            eintrag_dict['wert'] = vtg_dict.get('VK_Stueck')
            self.kostenCSV.SchreibeInKosten(eintrag_dict)

        #Fixkosten:
        eintrag_dict['vsnr'] = '999'
        eintrag_dict['jahr'] = str(jahr)
        eintrag_dict['name'] = 'fixkosten'
        eintrag_dict['avbg'] = '999' 
        
        vtg_dict = self.RechneFixkosten(vtg_dict)           
        eintrag_dict['wert'] = vtg_dict.get('fixkosten')
        self.kostenCSV.SchreibeInKosten(eintrag_dict)
            