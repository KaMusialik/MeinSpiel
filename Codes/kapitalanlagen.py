#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import protokoll as prot
import pandas as pd
import ka_renten as ka_rente
import ka_aktien
import kapitalanlagenCSV
import bilanzCSV
import ka_rentenCSV
import ka_aktienCSV
import kostenCSV

class Kapitalanlagen:
        
    def __init__(self, f_dict):

        self.f_dict = f_dict

        file_protokoll = f_dict.get('protokoll_file_kapitalanlagen')
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_kapitalanlagen = f_dict.get('file_kapitalanlagen_csv')
        self.file_kapitalanlagen_struktur = f_dict.get('file_kapitalanlagen_csv_struktur')
        self.file_renten_tabelle = f_dict.get('file_kapitalanlagen_renten_csv')
        self.file_aktien_tabelle = f_dict.get('file_kapitalanlagen_aktien_csv')
        self.file_sa_tabelle = f_dict.get('file_kapitalanlagen_sa_csv')

        self.file_system_fortschreibung = f_dict.get('file_system_fortschreibung')
        self.dtype_fortschteibung = f_dict.get('file_system_fortschreibung_struktur')
        
        self.file_provision = f_dict.get('file_provision')
        self.file_provision_struktur = f_dict.get('file_provision_struktur')

        self.file_kosten = f_dict.get('file_kosten')
        self.file_kosten_struktur = f_dict.get('file_kosten_struktur')

        self.file_bilanz = f_dict.get('file_bilanz')

        self.optionen_file_grundeinstellungen = f_dict.get('optionen_file_grundeinstellungwindow')  # hier stehen die Grunddaten
        self.darlehenszins = 0.0  #dieser Wert wird dann aus den Optionen gelesen und damit verändert

        self.oka_renten = ka_rente.KA_Renten(f_dict)  # Objekt/Tabelle für Renten wird angelegt
        self.oka_aktien = ka_aktien.KA_Aktien(f_dict)  # Objekt/Tabelle für Aktien wird angelegt
        
        self.LegeKapitalanlagenAn()
        
        self.LegeSATabelleAn()
        self.LeseDatenAusGrundeinstellungen()

        self.kapitalanlagenCSV = kapitalanlagenCSV.KapitalanlagenCSV(f_dict)  # Funktionen, um die Daten in der Kapitalanlage-CSV zu bearbeiten
        self.bilanzCSV = bilanzCSV.BilanzCSV(f_dict)  # Funktionen, um die Daten in der Bilanz-CSV zu bearbeiten
        self.ka_rentenCSV = ka_rentenCSV.KA_rentenCSV(f_dict)  # Funktionen, um die Daten in der Renten-CSV zu bearbeiten
        self.ka_aktienCSV = ka_aktienCSV.KA_AktienCSV(f_dict)  # Funktionen, um die Daten in der Aktien-CSV zu bearbeiten
        
    
    def LeseCsvOptinen(self, file, key):
        df = pd.read_csv(file, sep=";")
        df1 = df[df.key == key]
        
        if df1.empty:
            wert = 0
            text = 'Kapitalanlagen/LeseCsvOptinen: Kein Eintrag gefunden. Es wurde null verwendet: key='+str(print(key))
            print(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
            
        return wert 

    
    def LeseDatenAusGrundeinstellungen(self):

        file = self.optionen_file_grundeinstellungen 
        # Darlehenszins:
        key = 'darlehenszins'
        wert = self.LeseCsvOptinen(file, key)
        self.darlehenszins = float(wert)

    
    def Init_KA(self, jahr):  # hier wird die Kapitalanlage aus der Startbilanz vorbereitet:
        
        self.oka_aktien.Init_Aktien(jahr)  # Initialisierung der Aktien

        key_bilanz_dict = {}
        key_ka_dict = {}
        
        # Kasse_ende wird aus der Bialnz geholt. Dieser Wert steht bereits in der Bilanztabelle und muss nur abgeholt werden:
        name = 'kasse_ende'
        key_bilanz_dict['jahr'] = jahr - 1
        key_bilanz_dict['rl'] = 'bilanz'
        key_bilanz_dict['avbg'] = '999'
        key_bilanz_dict['name'] = name
        wert = float(self.bilanzCSV.LeseBilanzCSV(key_bilanz_dict))

        key_ka_dict['name'] = name
        key_ka_dict['topf'] = '999'
        key_ka_dict['jahr'] = jahr - 1
        key_ka_dict['wert'] = wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_ka_dict)
        
    
    def Init_SA(self, eintrag_dict):
        jahr=eintrag_dict.get('jahr')
        
        satz={}
        satz_renten={}
        satz_renten = eintrag_dict.get('renten')
        self.oka_renten.Init_SA(satz_renten)
        
        name='renten'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()

        name='anteil_aktien'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()

        name='anteil_renten'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()

        name='vola_aktien'
        betrag=eintrag_dict.get(name)
        satz['jahr']=jahr
        satz['name']=name
        satz['wert']=betrag
        self.SchreibeInSACSV(satz)
        satz.clear()
        
    
    def ZeichneKapitalanlagen(self, jahr):
        self.oka_renten.ZeichneRenten()
    
    
    def Fortschreibung(self, jahr):
        self.oka_renten.Fortschreibung(jahr)
        self.oka_aktien.Fortschreibung(jahr)
        
        key_dict={}
        key_renten_dict={}
        
        von = int(str(jahr)+'0101')
        bis = int(str(jahr)+'1231')
        
        key_renten_dict['jahr']=jahr
        key_renten_dict['nr']=999
        key_renten_dict['von']=von
        key_renten_dict['bis']=bis

        key_renten_dict['name']='ende'
        wert = self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        
        name='ende'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        key_renten_dict['name']='zins'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='zins'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        key_renten_dict['name']='zugang'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='zugang'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        key_renten_dict['name']='ablauf'
        wert= self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name='ablauf'
        key_dict['jahr']=jahr
        key_dict['name']=name
        key_dict['topf']='renten'
        key_dict['wert']=wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

    
    def LeseAusFortschreibung(self,key_dict):
        datei = self.file_system_fortschreibung
        df = pd.read_csv(datei, sep=";", dtype=self.dtype_fortschteibung)
        
        bis = key_dict.get('bis')
        name = key_dict.get('name')

        #es werden nur die relevanten Positionen genommen:
        df1 = df[(df.name == name) | (df.name == 'anzahl')]

        #nur die datensätze mit richtigem bis:
        df2 = df1[df1.bis == int(bis)][['vsnr', 'name', 'wert']]        

        #die Tabelle wird transpniert:
        df3 = pd.pivot_table(df2, values = 'wert', index = 'vsnr', columns = 'name', aggfunc = 'sum')
        
        #aus der pivot-Tabelle wird dateframe erstellet:
        df4 = df3.reset_index()
        
        #Berechnung pro vertrag von dem ausgewählten Feld "name" * anzahl:
        df5 = df4.assign( wert =  pd.to_numeric(df4[name])* pd.to_numeric(df4['anzahl']))
        
        #und jetz in dem Feld wert summieren:
        wert = df5['wert'].sum()

        return wert        

    
    def LeseAusProvisionAP(self, key_dict):
        datei = self.file_provision
        df = pd.read_csv(datei, sep=";", dtype=self.file_provision_struktur)
        
        jahr= int(key_dict.get('jahr'))
        name = key_dict.get('name')
        
        #welche verträge sind betroffen:
        df1 = df[ ( (df.jahr == jahr) & (df.gevo == 'Neuzugang') & (df.name == name) ) ]
        df1 = df1.astype({'wert':float})  # Umwandlung des Feldes wert in float
        wert = df1['wert'].sum()

        return wert

    
    def KonsolidiereDieKapitalanlageEnde(self, jahr):  # hier werde die Werte der Kapitalanlage zum Ende des Jahres aus Aktien und Renten addiert
        key_dict = {}
        
        # Stände zum Ende des Jahres:
        # lese Renten:
        key_dict['jahr'] = jahr
        key_dict['name'] = 'ende'
        key_dict['nr'] = 999
        bis = str(jahr)+'12'+'31'
        key_dict['bis'] = int(bis)
        von = str(jahr)+'01'+'01'
        key_dict['von'] = int(von)
        renten = float(self.ka_rentenCSV.LeseRentenCSV(key_dict))

        # lese Aktien:
        key_dict['jahr'] = jahr
        key_dict['name'] = 'aktien_ende'
        aktien_ende = float(self.ka_aktienCSV.LeseWertAusCSV(key_dict))
    
        kapitalanlage_ende = renten  + aktien_ende  # hier fehlen noch Aktien
        key_dict['jahr'] = jahr
        key_dict['name'] = 'kapitalanlagen_ende'
        key_dict['topf'] = '999'
        key_dict['wert'] = kapitalanlage_ende
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        # Zinsen bzw. Veränderung der Kapitalanlagen:
        # Renten:
        key_dict['jahr'] = jahr
        key_dict['name'] = 'zins'
        key_dict['topf'] = 'renten'
        zinsenRenten = self.kapitalanlagenCSV.LeseKapitalanlageCSV(key_dict)

        # Aktien:
        key_dict['jahr'] = jahr
        key_dict['name'] = 'kursertraege'
        kursertraege = self.ka_aktienCSV.LeseWertAusCSV(key_dict)

        kapitalertraege = zinsenRenten + kursertraege # hier fehlen noch Aktien
        key_dict['jahr'] = jahr
        key_dict['name'] = 'kapitalertraege'
        key_dict['topf'] = '999'
        key_dict['wert'] = kapitalertraege
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)



    def ErmittleKosten(self, jahr):  # hier werden die Kosten für cf ermittelt

        oKostenCSV = kostenCSV.KostenCSV(self.f_dict)

        key_dict = {}
        
        # interne AK (iAK):
        key_dict['jahr'] = jahr
        key_dict['name'] = 'iAK'
        key_dict['vsnr'] = 999
        key_dict['avbg'] = '999'
        iAK = oKostenCSV.LeseKostenCSV(key_dict)
        
        # Verwaltungskosten (VK_Stück):
        key_dict['jahr'] = jahr
        key_dict['name'] = 'VK_Stueck'
        key_dict['vsnr'] = 999
        key_dict['avbg'] = '999'
        vk_Stueck = oKostenCSV.LeseKostenCSV(key_dict)

        # fixkosten:
        key_dict['jahr'] = jahr
        key_dict['name'] = 'fixkosten'
        key_dict['vsnr'] = 999
        key_dict['avbg'] = '999'
        fixkosten = oKostenCSV.LeseKostenCSV(key_dict)

        wert = iAK + vk_Stueck + fixkosten
        return wert

    
    def ErmittleProvisionen(self, jahr):  # hier werden die im GJ gezahlten Provisionen ermittelt 
        key_dict = {}
        key_dict['jahr'] = jahr
        key_dict['name'] = 'ap'
        
        wert = self.LeseAusProvisionAP(key_dict)
        return wert

    
    def ErmittleBeitraege(self, jahr):  # hier werden die Beiträge im GJ ermittelt
        key_dict = {}
        
        bis = str(jahr)+'12'+'31'
        key_dict['bis'] = bis
        key_dict['jahr'] = jahr
        key_dict['name']='bil_verdienter_beitrag_nw216'
        wert = self.LeseAusFortschreibung(key_dict)  # hier wird der Wert aus der Tabelle Fortschreibung der einzelnen Verträge gelesen
        return wert
    
    
    def ErmittleStandKasseAmEnde(self, jahr):  # das cashflow des Jahres wird in die Kasse am Ende geschrieben
        key_dict={}

        #Beiträge:
        beitraege = self.ErmittleBeitraege(jahr)
        name='beitraege'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        key_dict['wert'] = beitraege
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)
    
        # Provisionen:
        provisionen = self.ErmittleProvisionen(jahr)
        name = 'provisionen_ap'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        key_dict['wert'] = provisionen
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        # Kosten:
        kosten = self.ErmittleKosten(jahr)
        name = 'kosten'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        key_dict['wert'] =kosten
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        # Cash flow:
        cf = beitraege - provisionen - kosten
        name = 'cashflow'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        key_dict['wert'] = cf
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        # Kasse am Ende des Jahres:
        
        # erstmal wird der Kassesatnd zu Beginn des Jahres gelesen:
        name = 'kasse_anfang_nach_umbuchung_von_kasse_zu_ka'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        kasse_anfang_nach_umbuchung_von_kasse_zu_ka = float(self.kapitalanlagenCSV.LeseKapitalanlageCSV(key_dict))

        # Zinsen, fass die Kasse zu Beginn negativ war:
        zinsenAufKasse = kasse_anfang_nach_umbuchung_von_kasse_zu_ka * self.darlehenszins
        name = 'zinsenAufKasse'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        key_dict['wert'] = zinsenAufKasse
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)

        kasse_endeVorCF = kasse_anfang_nach_umbuchung_von_kasse_zu_ka + zinsenAufKasse
        kasse_ende = kasse_endeVorCF + cf
        
        name = 'kasse_ende'
        key_dict['jahr'] = jahr
        key_dict['name'] = name
        key_dict['topf'] = '999'
        key_dict['wert'] = kasse_ende
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_dict)


    def LeseSACSV(self, key_dict):
        datei=self.file_sa_tabelle
        df=pd.read_csv(datei, sep=";")
        df[['jahr', 'name', 'wert']] = df[['jahr', 'name', 'wert']].astype(str)
       
        jahr=key_dict.get('jahr')
        name=key_dict.get('name')
 
        df1 = df[(df.jahr == str(jahr)) & (df.name==str(name))]
        if df1.__len__() == 0:
            wert=0
            text='kapitalanlagen/LeseSACSV: kein Eintrag in der Tabelle gefunden. Es wurde null verwendet'+str(print(key_dict))
            self.oprot.SchreibeInProtokoll(text)
        else:
            index=df1.index[0]
            wert=df1['wert'][index]
   
        return wert   
        
    
    def ZeileLoeschenInSACSV(self, key_dict):
        datei=self.file_sa_tabelle
        
        jahr=key_dict.get('jahr')
        name=key_dict.get('name')
        
        if self.LeseSACSV(key_dict) != 0:
            df = pd.read_csv(datei, sep=';')
            df1=df[(df['jahr'] != jahr) & (df['name']!=name)]
            df1.to_csv(datei, ';', index=False)
            
            text='Kapitalanlage: Eintrag in der Tabelle SA geloescht: jahr='+str(jahr)+' name='+str(name)
            self.oprot.SchreibeInProtokoll(text)

    
    def SchreibeInSACSV(self, eintrag_dict):
        datei=self.file_sa_tabelle
        
        jahr=eintrag_dict.get('jahr')
        name=eintrag_dict.get('name')
        wert=eintrag_dict.get('wert')
        
        if self.LeseSACSV(eintrag_dict) != 0:
            self.ZeileLoeschenInSACSV(eintrag_dict)
        
        text=str(jahr)+';'+str(name)+';'+str(wert)+'\n'
        f=open(datei, "a")
        f.write(text)    
        f.close()       
        
    
    def LegeKapitalanlagenAn(self):
        datei=self.file_kapitalanlagen
        ocsv=pd.DataFrame()
        ocsv["jahr"]=None
        ocsv["topf"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv[['jahr', 'topf','name', 'wert']] = ocsv[['jahr', 'topf','name', 'wert']].astype(str)
        ocsv.to_csv(path_or_buf=datei, sep=';', index=False)
        
        text='Kapitalanlegen: Tabelle fuer die Kapitalanlagen wurde angelegt: '+str(self.file_kapitalanlagen)
        self.oprot.SchreibeInProtokoll(text)
    
    
    def LegeSATabelleAn(self):
        datei=self.file_sa_tabelle
        ocsv=pd.DataFrame()
        ocsv['jahr']=None
        ocsv['name']=None
        ocsv["wert"]=None
        ocsv[['jahr', 'name', 'wert']] = ocsv[['jahr', 'name', 'wert']].astype(str)
        ocsv.to_csv(path_or_buf=datei, sep=';', index=False)
        
        text='Kapitalanlegen: Tabelle fuer die SA wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    
    def ErstelleKapitalanlagenAnfang(self, jahr):  # hier wird die Kapitalanlage zum Beginn des Jahres vorbereitet
        
        self.oka_aktien.ErstelleStandZumAnfangGJ(jahr)  # hier wirde der Staund zum Beginn des GJs erstellt

        key_ka_dict = {}
        
        # Stand der Kapitalanlage vom Vorjahr:
        key_ka_dict['jahr'] = jahr - 1
        key_ka_dict['name'] = 'kapitalanlagen_ende'
        key_ka_dict['topf'] = '999'
        wert = float(self.kapitalanlagenCSV.LeseKapitalanlageCSV(key_ka_dict))
        key_ka_dict['wert'] = wert
        # .... und schreiben den Anfangswert in die Tabelle rein:
        key_ka_dict['jahr'] = jahr
        key_ka_dict['name'] = 'kapitalanlagen_anfang'
        key_ka_dict['topf'] = '999'
        key_ka_dict['wert'] = wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_ka_dict)
    
        key_ka_dict.clear()
        # Stand der Kasse vom Vorjahr:
        key_ka_dict['jahr'] = jahr - 1
        key_ka_dict['name'] = 'kasse_ende'
        key_ka_dict['topf'] = '999'
        wert = float(self.kapitalanlagenCSV.LeseKapitalanlageCSV(key_ka_dict))
        key_ka_dict['wert'] = wert
        # .... und schreiben den Anfangswert in die Tabelle rein:
        key_ka_dict['jahr'] = jahr
        key_ka_dict['name'] = 'kasse_anfang'
        key_ka_dict['topf'] = '999'
        key_ka_dict['wert'] = wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_ka_dict)


    def UmschichtungInDerKapitalanlage(self, jahr):  # Hier werden die Anfangswerte der Bilanz der Kapitalanlage zusammengestellt
        self.oka_renten.Beginn(jahr)
        
        key_dict = {}
        key_bilanz_dict = {}
        key_ka_dict = {}
        key_renten_dict = {}
        
        # Kasse_anfang wird geholt. Dieser Wert steht bereits in der tabelle und muss nur abgeholt werden:
        name = 'kasse_anfang'
        key_ka_dict['name'] = name
        key_ka_dict['topf'] = '999'
        key_ka_dict['jahr'] = jahr
        wert = float(self.kapitalanlagenCSV.LeseKapitalanlageCSV(key_ka_dict))
        kasse_anfang = wert
        
        name = 'umbuchung_von_kasse_zu_ka_zugang'
        key_ka_dict['jahr'] = jahr
        key_ka_dict['name'] = name
        key_ka_dict['topf'] = '999'
        if kasse_anfang > 0:  # nur wenn etwas positives in der Kasse ist, wird es in die KA umgebucht
            umbuchung_von_kasse_zu_ka_zugang = kasse_anfang
            key_ka_dict['wert'] = umbuchung_von_kasse_zu_ka_zugang
        else:
            umbuchung_von_kasse_zu_ka_zugang = 0.0
            key_ka_dict['wert'] = umbuchung_von_kasse_zu_ka_zugang

        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_ka_dict)

        name = 'kasse_anfang_nach_umbuchung_von_kasse_zu_ka'
        wert = kasse_anfang - umbuchung_von_kasse_zu_ka_zugang
        key_ka_dict['jahr'] = jahr
        key_ka_dict['name'] = name
        key_ka_dict['topf'] = '999'
        key_ka_dict['wert'] = wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_ka_dict)
        
        bis_vj = str(int(jahr-1))+'1231'
        von_vj = str(int(jahr-1))+'0101'
        
        key_renten_dict['jahr'] = int(jahr)-1
        key_renten_dict['nr'] = 999
        key_renten_dict['von'] = von_vj
        key_renten_dict['bis'] = bis_vj
        key_renten_dict['name'] = 'ende'
        wert = self.oka_renten.WertAusRentenTabelle(key_renten_dict)
        name = 'anfang'
        key_ka_dict['jahr'] = jahr
        key_ka_dict['name'] = name
        key_ka_dict['topf'] = 'renten'
        key_ka_dict['wert'] = wert
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(key_ka_dict)

        self.UmschichteKapitalanlagen(jahr)
    
    def UmschichteKapitalanlagen(self, jahr):
        ka_dict = {}
        ka_renten_dict = {}
        ka_aktien_dict = {}
        sa_dict = {}
        
        ka_dict['jahr'] = jahr
        ka_dict['name'] = 'umbuchung_von_kasse_zu_ka_zugang'
        ka_dict['topf'] = '999'
        umbuchung = self.kapitalanlagenCSV.LeseKapitalanlageCSV(ka_dict)  # dieser Wert soll von der Kasse in die KA umgeschichtet werden

        ka_dict['jahr'] = jahr
        ka_dict['name'] = 'anfang'
        ka_dict['topf'] = '999'
        ka_dict['topf'] = 'renten'
        ka_renten_anfang = self.kapitalanlagenCSV.LeseKapitalanlageCSV(ka_dict)

        ka_dict['jahr'] = jahr
        ka_dict['name'] = 'anfang'
        ka_dict['topf'] = 'aktien'
        ka_aktien_anfang = self.kapitalanlagenCSV.LeseKapitalanlageCSV(ka_dict)
    
        sa_dict['jahr'] = jahr
        sa_dict['name'] = 'anteil_renten'
        anteil_renten = float(self.LeseSACSV(sa_dict))
        sa_dict.clear()        

        sa_dict['jahr'] = jahr
        sa_dict['name'] = 'anteil_aktien'
        anteil_aktien = float(self.LeseSACSV(sa_dict))
        sa_dict.clear()        
        
        ka_anfang = ka_renten_anfang + ka_aktien_anfang + umbuchung
        umbuchung_renten = anteil_renten * umbuchung
        umbuchung_aktien = anteil_aktien * umbuchung
        
        '''
        max_betrag_aktien = anteil_aktien * ka_anfang
        if ka_aktien_anfang+umbuchung_aktien <= max_betrag_aktien:
            #man kann noch mehr zu aktien verschieben:
            verschiebung_zu_aktien=max(max_betrag_aktien-(ka_aktien_anfang+umbuchung_aktien), 0)
            umbuchung_renten= umbuchung_renten-verschiebung_zu_aktien
            umbuchung_aktien= umbuchung_aktien+verschiebung_zu_aktien
        else:
            #zu viel Aktien. Reduktion erforderilch:
            verschiebung_zu_renten=ka_aktien_anfang+umbuchung_aktien-max_betrag_aktien
            umbuchung_renten= umbuchung_renten+verschiebung_zu_renten
            umbuchung_aktien= umbuchung_aktien-verschiebung_zu_renten
        '''
            
        ka_renten_anfang_nach_reallokation=ka_renten_anfang+umbuchung_renten
        ka_aktien_anfang_nach_reallokation=ka_aktien_anfang+umbuchung_aktien
        
        #Schreibe Renten:
        
        ka_renten_dict.clear()
        von = str(jahr)+'0101'
        bis = str(jahr)+'1231'

        ka_dict.clear()
        ka_dict['jahr'] = jahr
        ka_dict['name'] = 'anfang'
        ka_dict['topf'] = 'renten'
        ka_dict['wert'] = ka_renten_anfang_nach_reallokation
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(ka_dict)
        
        #***********************************************
        
        #Schreibe Aktien:
        ka_dict.clear()
        ka_dict['jahr'] = jahr
        ka_dict['name'] = 'anfang'
        ka_dict['topf'] = 'aktien'
        ka_dict['wert'] = ka_aktien_anfang_nach_reallokation
        self.kapitalanlagenCSV.SchreibeInKapitalanlagenCSV(ka_dict)
        #************************************************
        
        if umbuchung_aktien>0:
            self.KaufeAktien(jahr, umbuchung_aktien)
        else:
            self.VerkaufeAktien(jahr, umbuchung_aktien)

        if umbuchung_renten>0:
            self.oka_renten.KaufeRenten(jahr, umbuchung_renten)
        else:
            self.VerkaufeRenten(jahr, umbuchung_renten)


    def VerkaufeAktien(self, jahr, betrag):
        pass
    
    
    def KaufeAktien(self, jahr, betrag):
        aktien_dict={}
        
        aktien_dict['jahr']=jahr        
        aktien_dict['name']='anlage_betrag'
        aktien_dict['wert']=betrag
        self.ka_aktienCSV.SchreibeInCSV(aktien_dict)
        aktien_dict.clear()

    def VerkaufeRenten(self, jahr, betrag):
        pass

            
    


