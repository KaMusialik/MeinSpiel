#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
import provision
import kosten

class Bilanz(object):

    def __init__(self, f_dict):
        
        self.file_dict = f_dict
        
        file_protokoll=f_dict.get('protokoll_file_bilanz')
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_bilanz_start=f_dict.get('file_bilanz_start')
        text = 'Bilanz/__init__: File für Startbilanz: '+str(self.file_bilanz_start)
        self.oprot.SchreibeInProtokoll(text)
        
        self.file_bilanz=f_dict.get('file_bilanz')
        text = 'Bilanz/__init__: File für Bilanz: '+str(self.file_bilanz)
        self.oprot.SchreibeInProtokoll(text)
        
        self.dtype_dic= f_dict.get('file_bilanz_struktur')
        text = 'Bilanz/__init__: es wurde eine Beschreibung der Binalnztabelle angelegt: '+str(self.dtype_dic)
        self.oprot.SchreibeInProtokoll(text)

        self.dtype_dic_start= { 'jahr':int, 'rgl':str, 'avbg': str, 'name':str, 'wert':str}
        text = 'Bilanz/__init__: es wurde eine Beschreibung der Start-Binalnztabelle angelegt: '+str(self.dtype_dic_start)
        self.oprot.SchreibeInProtokoll(text)
 
        self.file_system_fortschreibung=f_dict.get('file_system_fortschreibung')
        self.dtype_fortschteibung=f_dict.get('file_system_fortschreibung_struktur')
        
        self.file_provision = f_dict.get('file_provision')
        self.file_provision_struktur = f_dict.get('file_provision_struktur')

        self.file_kosten = f_dict.get('file_kosten')
        self.file_kosten_struktur = f_dict.get('file_kosten_struktur')
        
        self.file_kapitalanlagen_csv = f_dict.get('file_kapitalanlagen_csv')
        self.file_kapitalanlagen_csv_struktur = f_dict.get('file_kapitalanlagen_csv_struktur')

        self.LegeBilanzAn()
        
    def Init_Bilanz(self, jahr):
        key_dict={}
        key_dict.clear()

        name='eigenkapital_ende'
        avbg='999'
        rl='bilanz'
        key_dict['name']=name
        key_dict['avbg']=avbg
        key_dict['jahr']=jahr-1
        key_dict['rl']=rl 
        key_dict['wert']=self.LeseStartBilanzCSV(key_dict)

        name='eigenkapital_ende'
        key_dict['name']=name
        key_dict['jahr']=jahr-1
        self.SchreibeInBilanzCSV(key_dict)

        key_dict['rl']='bilanz'
        key_dict['name']='kasse_ende'
        key_dict['jahr']=jahr-1
        key_dict['avbg']='999'
        self.SchreibeInBilanzCSV(key_dict)
    
    def LegeBilanzAn(self):
        datei=self.file_bilanz
        ocsv=pd.DataFrame()
        ocsv["jahr"]=None
        ocsv["rl"]=None
        ocsv["avbg"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv[['jahr', 'rl', 'avbg', 'name', 'wert']] = ocsv[['jahr', 'rl', 'avbg', 'name', 'wert']].astype(str)
        ocsv.to_csv(datei, ';', index=False)
        
        text='Bilanz/LegeBilanzAn: bilanztabelle wurde angelegt: '+str(self.file_bilanz)
        self.oprot.SchreibeInProtokoll(text)
    
    
    def ErstelleBilanzAnfang(self, jahr):
        self.Eigenkapital_Anfang(jahr)
        self.BilDK_Anfang(jahr)
        self.Kapitalanlagen_Anfang(jahr)        
    
    
    def LeseBilanzVorjahr(self, key_dict):
        name_alt=key_dict['name']
        name=name_alt+'_ende'
        jahr_alt=key_dict['jahr']
        key_dict['name']=name
        key_dict['jahr']=jahr_alt-1
        
        datei=self.file_bilanz
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
        
        jahr=key_dict.get('jahr')
        rl=key_dict.get('rl')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == jahr) & (df.rl==rl) & (df.name==name)]
        if df1.__len__() != 0:
            for index, row in df1.iterrows():
                avbg=row['avbg']
                wert=row['wert']
                key_dict['avbg']=avbg
                key_dict['wert']=wert
                name=name_alt+'_anfang'
                key_dict['name']=name
                key_dict['jahr']=jahr_alt
                
                self.SchreibeInBilanzCSV(key_dict)
                
    
    def Kapitalanlagen_Anfang(self, jahr):  # Initialisierung der Bilanz zum Beginn des GJ
        key_dict={}
        
        #kasse_ende:
        key_dict.clear()
        name = 'kasse_ende'
        avbg = '999'
        rl = 'bilanz'
        key_dict['name'] = name
        key_dict['avbg'] = avbg
        key_dict['jahr'] = jahr-1 
        key_dict['rl'] = rl
        key_dict['wert'] = self.LeseBilanzCSV(key_dict)

        name='kasse_anfang'
        key_dict['name'] = name
        key_dict['jahr'] = jahr

        self.SchreibeInBilanzCSV(key_dict)
        #******************************************
   
        # Kapitalanlagen_ende:
        key_dict.clear()
        name = 'kapitalanlagen_ende'
        avbg = '999'
        rl = 'bilanz'
        key_dict['name'] = name
        key_dict['avbg'] = avbg
        key_dict['jahr'] = jahr-1 
        key_dict['rl'] = rl
        key_dict['wert'] = self.LeseBilanzCSV(key_dict)

        name='kapitalanlagen_anfang'
        key_dict['name'] = name
        key_dict['jahr'] = jahr

        self.SchreibeInBilanzCSV(key_dict)
        #******************************************


    def Eigenkapital_Anfang(self, jahr):       
        key_dict={}

        #Egenkapital_Ende:
        key_dict.clear()
        name='eigenkapital_ende'
        avbg='999'
        rl='bilanz'
        key_dict['name']=name
        key_dict['avbg']=avbg
        key_dict['jahr']=jahr-1 
        key_dict['rl']=rl
        key_dict['wert']=self.LeseBilanzCSV(key_dict)

        name='eigenkapital_anfang'
        key_dict['name']=name
        key_dict['jahr']=jahr

        self.SchreibeInBilanzCSV(key_dict)
        #*******************************************
        
    
    def BilDK_Anfang(self, jahr):
        key_dict={}
        key_dict['jahr']=jahr
        key_dict['rl']='bilanz'

        key_dict['name']='bil_derue1'
        self.LeseBilanzVorjahr(key_dict)

        key_dict['name']='bil_derue2'
        self.LeseBilanzVorjahr(key_dict)
        
        key_dict['name']='bil_derue3'
        self.LeseBilanzVorjahr(key_dict)
        
        key_dict['name']='bil_derue5'
        self.LeseBilanzVorjahr(key_dict)

        key_dict['name']='bil_derue7'
        self.LeseBilanzVorjahr(key_dict)

        key_dict['name']='bil_bio_nachreservierung'
        self.LeseBilanzVorjahr(key_dict)

        key_dict['name']='bil_zzr_nachreservierung'
        self.LeseBilanzVorjahr(key_dict)

        key_dict['name']='bil_unisex_nachreservierung'
        self.LeseBilanzVorjahr(key_dict)
        
    
    def ErstelleBilanzEnde(self, jahr):
        self.BilanzPositionenAusFortschreibung(jahr)
        
        self.BilanzPositionenAusProvision(jahr)
        self.BilanzPositionenAusKosten(jahr)
        
        self.BilanzPositionenAusKapitalanlagen(jahr)  # Kapitalanlagen für die Aktivseite

        self.Veraenderungspositionen(jahr)
        
        self.Jahresueberschuss(jahr)
        
        self.Eigenkapital_Ende(jahr)
        
    
    def Jahresueberschuss(self, jahr):
        key_dict={}
        
        key_dict['jahr']=jahr
        key_dict['rl']='guv'
        key_dict['avbg']='999'
        
        key_dict['name'] = 'bil_gebuchter_beitrag'
        gebbtg = float(self.LeseBilanzCSV(key_dict))

        key_dict['name'] = 'bil_derue7_veraenderung'
        veranderung_derue = float(self.LeseBilanzCSV(key_dict))

        key_dict['name'] = 'ap'
        ap = float(self.LeseBilanzCSV(key_dict))

        key_dict['name'] = 'iAK'
        iAK = float(self.LeseBilanzCSV(key_dict))

        key_dict['name'] = 'VK_Stueck'
        VK_Stueck = float(self.LeseBilanzCSV(key_dict))
        
        key_dict['name'] = 'kapitalertraege'
        kapitalertraege = float(self.LeseBilanzCSV(key_dict))

        key_dict['name'] = 'zinsAufKasse'
        zinsAufKasse = float(self.LeseBilanzCSV(key_dict))

    
        jahresueberschuss = gebbtg - veranderung_derue - ap - iAK - VK_Stueck + kapitalertraege + zinsAufKasse
        
        key_dict['name'] = 'jahresueberschuss'
        key_dict['wert'] = jahresueberschuss
        self.SchreibeInBilanzCSV(key_dict)
    
    
    def Veraenderungspositionen(self, jahr):
        #hir werden die Positionen festgelegt, für die die Veränderung zum Vorjahr bestimmt werden sollte
        
        name='bil_derue7'
        self.VeraenderungspositionenName(jahr, name)
        
    
    def VeraenderungspositionenName(self, jahr, name_quelle):
        #hier wird für eine Bilanzposition 'name_quelle' die Veränderung zum Vorjahr ermittelt:
        datei=self.file_bilanz
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)

        name_alt=name_quelle
        
        key_dict={}
        
        key_dict['jahr']=jahr
        rl='bilanz'
        key_dict['rl']=rl
        name=name_alt+'_ende'
        key_dict['name']=name
        
        df1 = df[(df.jahr==int(jahr)) & (df.rl==rl) & (df.avbg!='999') & (df.name==name)]
        if df1.__len__() != 0:
            for index, row in df1.iterrows():
                avbg=row['avbg']
                wert_ende=float(row['wert'])
                key_dict['avbg']=avbg
                key_dict['rl']='bilanz'
                
                name=name_alt+'_anfang'
                key_dict['name']=name
                wert_anfang=float(self.LeseBilanzCSV(key_dict))
                
                wert_veraenderung=wert_ende-wert_anfang
                name=name_alt+'_veraenderung'
                key_dict['name']=name
                key_dict['wert']=wert_veraenderung
                key_dict['rl']='guv'
                self.SchreibeInBilanzCSV(key_dict)
        else:
            text = 'Bilanz/VeraenderungspositionenName: keine Datensätzte gefunden' + str(df1)
            self.oprot.SchreibeInProtokoll(text)

         
        wert=self.KumuliereAlleAvbgInBilanz(key_dict)
        key_dict['wert']=wert
        key_dict['avbg']='999'
        self.SchreibeInBilanzCSV(key_dict)
    
    
    def BilanzPositionenAusProvision(self, jahr):
        key_dict = {}
        key_dict['rl'] = 'guv'
        key_dict['jahr'] = jahr
        key_dict['name'] = 'ap'
        
        self.LeseAusProvisionAP(key_dict)

    
    def BilanzPositionenAusKapitalanlagen(self, jahr):
        key_dict = {}
        
        # Stand der Kapitalanlagen am Ende des Jahres:
        key_dict['topf'] = '999'
        key_dict['jahr'] = jahr
        key_dict['name'] = 'kapitalanlagen_ende'
        key_dict['name_fuer_bilanz_csv'] = 'kapitalanlagen_ende'
        key_dict['rl'] = 'bilanz'
        key_dict['avbg'] = '999'
        self.LeseAusKapitalanlagen(key_dict)

        # Stand Kasse am Ende des Jahres:
        key_dict['topf'] = '999'
        key_dict['jahr'] = jahr
        key_dict['name'] = 'kasse_ende'
        key_dict['name_fuer_bilanz_csv'] = 'kasse_ende'
        key_dict['rl'] = 'bilanz'
        key_dict['avbg'] = '999'
        self.LeseAusKapitalanlagen(key_dict)

        # Kapitalerträge:
        key_dict['topf'] = '999'
        key_dict['jahr'] = jahr
        key_dict['name'] = 'kapitalertraege'
        key_dict['name_fuer_bilanz_csv'] = 'kapitalertraege'
        key_dict['rl'] = 'guv'
        key_dict['avbg'] = '999'
        self.LeseAusKapitalanlagen(key_dict)
        
        # Kapitalerträge/Darlehenszins auf Kasse zu Beginn des Jahres:
        key_dict['topf'] = '999'
        key_dict['jahr'] = jahr
        key_dict['name'] = 'zinsAufKasse'
        key_dict['name_fuer_bilanz_csv'] = 'zinsAufKasse'
        key_dict['rl'] = 'guv'
        key_dict['avbg'] = '999'
        self.LeseAusKapitalanlagen(key_dict)

    
    def BilanzPositionenAusKosten(self, jahr):
        key_dict = {}
        key_dict['rl'] = 'guv'
        key_dict['jahr'] = jahr
        
        key_dict['name'] = 'iAK'
        self.LeseAusKosten(key_dict)

        key_dict['name'] = 'VK_Stueck'
        self.LeseAusKosten(key_dict)
    
    
    def BilanzPositionenAusFortschreibung(self, jahr):
        key_dict={}
        
        bis=str(jahr)+'12'+'31'
        key_dict['bis']=bis
        key_dict['jahr']=jahr
        key_dict['rl']='bilanz'
       
        key_dict['name']='bil_derue1_ende'
        self.LeseAusFortschreibung(key_dict)
        
        key_dict['name']='bil_derue2_ende'
        self.LeseAusFortschreibung(key_dict)
        
        key_dict['name']='bil_derue3_ende'
        self.LeseAusFortschreibung(key_dict)
        
        key_dict['name']='bil_derue5_ende'
        self.LeseAusFortschreibung(key_dict)
        
        key_dict['name']='bil_derue7_ende'
        self.LeseAusFortschreibung(key_dict)

        key_dict['name']='nachreservierung_ende'
        self.LeseAusFortschreibung(key_dict)
        
        #**********************************************************
        key_dict['rl']='guv'
        
        key_dict['name']='bil_gebuchter_beitrag'
        self.LeseAusFortschreibung(key_dict)

        key_dict['name']='bil_verdienter_beitrag_nw216'
        self.LeseAusFortschreibung(key_dict)


    def KumuliereAlleAvbgInBilanz(self, key_dict):
        datei=self.file_bilanz
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
        
        jahr=int(key_dict.get('jahr'))
        rl=str(key_dict.get('rl'))
        name=key_dict.get('name')

        df1 = df[(df.jahr == jahr) & (df.rl==str(rl)) & (df.avbg!='999') &(df.name==str(name))]
        
        if df1.empty:
            wert = 0.0
            text = 'Bilanz/KumuliereAlleAvbgInBilanz: Eintrag in der Tabelle nicht gefunden. Keine Kumulierung möglich!'
            self.oprot.SchreibeInProtokoll(text)
        else:
            df2=df1[['name', 'wert']]
            df2['wert'] = pd.to_numeric(df2['wert']) 

            df3=df2.groupby('name')['wert'].sum()
            
            if len(df3) != 1:
                wert = 0
                text = 'Bilanz/KumuliereAlleAvbgInBilanz: Unerwartete anzahl der kummulierten Sätze!' + str(df3)
                self.oprot.SchreibeInProtokoll(text)
            else:
                wert = df3[0]
       
        return wert   
    

    def LeseAusKosten(self, key_dict):
        datei = self.file_kosten
        struktur = self.file_kosten_struktur
        df = pd.read_csv(datei, sep=";", dtype = struktur)
        
        jahr = int(key_dict.get('jahr'))
        name = str(key_dict.get('name')) 
        
        #welche verträge mit welchen Bestandsgruppen sind betroffen:
        df1 = df[( (df.jahr == jahr) & (df.name == name) )]
        df2 = df1[['jahr','avbg', 'wert']].groupby(['jahr', 'avbg']).sum().reset_index()

        for index, row in df2.iterrows():
            
            avbg = str(row['avbg'])
            wert = float(row['wert'])
            
            key_dict['avbg'] = avbg
            key_dict['wert'] = wert
            
            self.SchreibeInBilanzCSV(key_dict)


        wert = self.KumuliereAlleAvbgInBilanz(key_dict)
        key_dict['wert']=wert
        key_dict['avbg']='999'
        self.SchreibeInBilanzCSV(key_dict)
    
    
    def LeseAusKapitalanlagen(self, key_dict):
        datei = self.file_kapitalanlagen_csv
        df = pd.read_csv(datei, sep=";", dtype=self.file_kapitalanlagen_csv_struktur)

        jahr = int(key_dict.get('jahr'))
        topf = key_dict.get('topf')
        name = key_dict.get('name')

        df1 = df[( (df.jahr == jahr) & (df.name == name) & (df.topf == topf) )]

        if df1.empty:
            wert = 0.0
            text = 'bilanz/LeseAusKapitalanlagen: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: '+str(key_dict)
            self.oprot.SchreibeInProtokoll(text)
        else:
            if df1.__len__() != 1:
                wert = 999999999
                text = 'bilanz/LeseAusKapitalanlagen: mehrere Eintraeg in der Tabelle gefunden. Es wurde ein Wert von '+str(wert)+ ' verwendet: '+str(key_dict)
                self.oprot.SchreibeInProtokoll(text)
            else:
                index = df1.index[0]
                wert = df1.at[index, 'wert']

        key_dict['wert'] = wert
        key_dict['name'] = key_dict.get('name_fuer_bilanz_csv')
        self.SchreibeInBilanzCSV(key_dict)


    def LeseAusProvisionAP(self, key_dict):
        datei = self.file_provision
        df = pd.read_csv(datei, sep=";", dtype=self.file_provision_struktur)
        
        jahr= int(key_dict.get('jahr'))
        
        #welche verträge mit welchen Bestandsgruppen sind betroffen:
        df1 = df[( (df.jahr == jahr) )]
        df2=df1.groupby(['jahr', 'vsnr']).count().reset_index()

        listeDerVertraege = []
        for index, row in df2.iterrows():
            wert = str(row['vsnr'])
            listeDerVertraege.append(wert)
 
        oprov = provision.Provision(self.file_dict)
 
        keyProv_dict = {}
        keyProv_dict['jahr'] = jahr
        keyProv_dict['gevo'] = 'Neuzugang'
        for vsnr in listeDerVertraege:
            keyProv_dict['vsnr'] = vsnr
   
            name = 'avbg'
            keyProv_dict['name'] = name
            avbg = oprov.LeseAusProvisionCSV(keyProv_dict)
            key_dict['avbg'] = avbg
            
            name = 'ap'
            keyProv_dict['name'] = name
            ap = oprov.LeseAusProvisionCSV(keyProv_dict)
            key_dict['name'] = 'ap'
            key_dict['wert'] = ap
            
            self.SchreibeInBilanzCSV(key_dict)


        wert = self.KumuliereAlleAvbgInBilanz(key_dict)
        key_dict['wert']=wert
        key_dict['avbg']='999'
        self.SchreibeInBilanzCSV(key_dict)


    def LeseAusFortschreibung(self,key_dict):
        datei = self.file_system_fortschreibung
        df = pd.read_csv(datei, sep=";", dtype=self.dtype_fortschteibung)
        
        bis = key_dict.get('bis')
        name = key_dict.get('name')

        #es werden nur die relevanten Positionen genommen:
        df1 = df[(df.name == name) | (df.name == 'anzahl') | (df.name == 'avbg')]

        #nur die datensätze mit richtigem bis:
        df2 = df1[df1.bis == int(bis)][['vsnr', 'name', 'wert']]        

        #die Tabelle wird transpniert:
        df3 = pd.pivot_table(df2, values = 'wert', index = 'vsnr', columns = 'name', aggfunc = 'sum')
        
        #aus der pivot-Tabelle wird dateframe erstellet:
        df4 = df3.reset_index()
        
        #Berechnung pro vertrag von dem ausgewählten Feld "name" * anzahl:
        df5 = df4.assign( wert =  pd.to_numeric(df4[name])* pd.to_numeric(df4['anzahl']))
        
        #und jetz nach avbg gruppieren und in dem Feld wert summieren:
        df6 = df5.groupby(['avbg'])['wert'].sum().reset_index()
        
        #schreiben in die Tabelle bilanz:
        for index, row in df6.iterrows():
            avbg = str(row['avbg'])
            wert = float(row['wert'])
            key_dict['avbg'] = avbg
            key_dict['wert'] = wert
            self.SchreibeInBilanzCSV(key_dict)
            
        wert=self.KumuliereAlleAvbgInBilanz(key_dict)
        key_dict['wert']=wert
        key_dict['avbg']='999'
        self.SchreibeInBilanzCSV(key_dict)

    
    def Eigenkapital_Ende(self, jahr):
        key_dict={}
        
        name='eigenkapital_anfang'
        avbg='999'
        key_dict['name']=name
        key_dict['avbg']=avbg
        key_dict['jahr']=jahr
        key_dict['rl']='bilanz'
        ek_anfang=self.LeseBilanzCSV(key_dict)
        
        name='jahresueberschuss'
        key_dict['name']=name
        key_dict['rl']='guv'

        jue=self.LeseBilanzCSV(key_dict)

        ek_ende=ek_anfang+jue
        key_dict['wert']=ek_ende
        name='eigenkapital_ende'
        key_dict['rl']='bilanz'
        key_dict['name']=name
        
        self.SchreibeInBilanzCSV(key_dict)
        

    def LeseBilanzCSV(self, key_dict):
        datei=self.file_bilanz
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
       
        jahr=int(key_dict.get('jahr'))
        rl=str(key_dict.get('rl'))
        avbg=str(key_dict.get('avbg'))
        name=str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.rl==rl) & (df.avbg==avbg) & (df.name==name)]

        if df1.empty:
            wert=0
            text='bilanz/LeseBilanzCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: '+str(key_dict)
            self.oprot.SchreibeInProtokoll(text)
        else:
            if df1.__len__() != 1:
                wert=999999999
                text='bilanz/LeseBilanzCSV: mehrere Eintraeg in der Tabelle gefunden. Es wurde ein Wert von '+str(wert)+ ' verwendet: '+str(key_dict)
                self.oprot.SchreibeInProtokoll(text)
            else:
                index=df1.index[0]
                wert=df1.at[index, 'wert']

        return float(wert)   


    def LeseStartBilanzCSV(self, key_dict):
        datei=self.file_bilanz_start
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic_start)
        
        jahr=int(key_dict.get('jahr'))
        rl=str(key_dict.get('rl'))
        avbg=str(key_dict.get('avbg'))
        name=str(key_dict.get('name'))
 
        df1 = df[(df.jahr==jahr) & (df.rl==rl) & (df.avbg==avbg) & (df.name==name)]
        if df1.__len__() == 0:
            text='LeseStartBilanzCSV: fuer diese parameter: '+str(key_dict)+' wurden keine Werte gefunden. Es wird 0 verwendet'
            self.oprot.SchreibeInProtokoll(text)
            wert=0
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
       
        return wert   
    

    def SchreibeInBilanzCSV(self, key_dict):
        datei=self.file_bilanz
        
        jahr=key_dict.get('jahr')
        rl=key_dict.get('rl')
        avbg=key_dict.get('avbg')
        name=key_dict.get('name')
        wert=key_dict.get('wert')
        
        if self.LeseBilanzCSV(key_dict) != 0:
            self.ZeileLoeschenInBilanzCSV(key_dict)
        
        text=str(jahr)+';'+str(rl)+';'+str(avbg)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       
        

    def ZeileLoeschenInBilanzCSV(self, key_dict):
        datei=self.file_bilanz
        
        jahr=key_dict.get('jahr')
        rl=key_dict.get('rl')
        avbg=key_dict.get('avbg')
        name=key_dict.get('name')
        
        if self.LeseBilanzCSV(key_dict) != 0:
            df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
            df1=df[(df['jahr'] != jahr) & (df['rl']!=rl) & (df['avbg']!=avbg) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            
            text='Bilanz/ZeileLoeschenInBilanzCSV: Eintrag in der Bilanztabelle geloescht: jahr='+str(jahr)+' rl='+str(rl)+' avbg='+str(avbg)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)
