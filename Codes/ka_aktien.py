import protokoll as prot
import pandas as pd
import ka_aktienCSV
import optionen_grundeinstellungCSV
from statistics import NormalDist
import random

class KA_Aktien:
        
    def __init__(self, f_dict):
        file_protokoll = f_dict.get('protokoll_file_aktien')
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_aktien_csv  = f_dict.get('file_kapitalanlagen_aktien_csv')
        self.file_aktien_csv_struktur  = f_dict.get('file_aktien_csv_struktur')

        self.LegeAktienTabelleAn()
        self.ka_aktienCSV = ka_aktienCSV.KA_AktienCSV(f_dict)
    
        self.ogrundCSV = optionen_grundeinstellungCSV.Optionen_GrundeinstellungCSV(f_dict)
        self.ka_aktien_sa = ''
        self.ex_aktien = 0.0072  # durchnittliche Aktienentwicklung pro Monat. Dazu gibt es ein Excel
        self.sigma_aktien = 0.050822496  # errechnetes Sigma aus den Daten vom DAX. dazu gibt es ein Excel
        self.sigma = 0.0

    def BestimmeSigmaAktien(self):  # hier wird das Sigma ggf. gestreckt.
        self.risiko = self.ka_aktien_sa
        sigma = self.sigma_aktien
        
        if self.risiko == 'normal':
            self.sigma = sigma
        elif self.risiko == 'risky' or self.risiko == 'gross':
            self.sigma = 2.0 * sigma
        elif self.risiko == 'high_risky' or self.risiko == 'sehrgross':
            self.sigma = 3.0 * sigma
        else:
            self.sigma = 5.0 * sigma

    
    def LegeAktienTabelleAn(self):  # Tabelle für Aktien wird angelegt
        datei = self.file_aktien_csv
        ocsv = pd.DataFrame()
        ocsv['jahr'] = None
        ocsv['name'] = None
        ocsv["wert"] = None
        ocsv.to_csv(path_or_buf=datei, sep=';', index=False)
        
        text = 'KA_Aktien/LegeAktienTabelleAn: Tabelle fuer die Aktien wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    
    def LeseGrundeinstellung(self):  # hier werden die Grundeinstellungen zu den Aktien gelesen:
        key_dict = {}
        
        # wir riskant soll sollen die Aktien angelegt werden: 
        key = 'ka_aktien_sa'
        key_dict['key'] = key
        wert = self.ogrundCSV.LeseWertAusCSV(key_dict)
        self.ka_aktien_sa = wert

        stat_dict = {}
        stat_dict['risiko'] = self.ka_aktien_sa
    
    
    def Init_Aktien(self, jahr):  # hier werden die Aktien zu Beginn des GJ initialisiert
        
        self.LeseGrundeinstellung()
        self.BestimmeSigmaAktien()

        key_aktien_dict = {}
        
        # kurs_ende im Startjahr -1
        name = 'kurs_ende'
        key_aktien_dict['jahr'] = jahr - 1
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = 100.0
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

    
    def ErstelleStandZumAnfangGJ(self, jahr):  # hier wird die Kapitalanlage zum Beginn des Jahres vorbereitet
        key_aktien_dict = {}

        # aktien_ende wird aus dem Vorjahr geholt.
        name = 'aktien_ende'
        key_aktien_dict['jahr'] = jahr - 1
        key_aktien_dict['name'] = name
        wert = float(self.ka_aktienCSV.LeseWertAusCSV(key_aktien_dict))
        key_aktien_dict.clear()

        # aktien_anfang wird in die Tabelle reingeschrieben.
        name = 'aktien_anfang'
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = wert
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # kurs_ende wird aus dem Vorjahr geholt.
        name = 'kurs_ende'
        key_aktien_dict['jahr'] = jahr - 1
        key_aktien_dict['name'] = name
        wert = float(self.ka_aktienCSV.LeseWertAusCSV(key_aktien_dict))
        key_aktien_dict.clear()

        # kurs_anfang wird in die Tabelle reingeschrieben.
        name = 'kurs_anfang'
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = wert
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # anteile_ende wird aus dem Vorjahr geholt.
        name = 'anteile_ende'
        key_aktien_dict['jahr'] = jahr - 1
        key_aktien_dict['name'] = name
        wert = float(self.ka_aktienCSV.LeseWertAusCSV(key_aktien_dict))
        key_aktien_dict.clear()

        # anteile_anfang wird in die Tabelle reingeschrieben.
        name = 'anteile_anfang'
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = wert
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

    def Fortschreibung(self, jahr):  # hier werden die Aktien fortgeschrieben
        key_aktien_dict = {}

        # anteile_anfang wird geholt:
        name = 'anteile_anfang'
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        anteile_anfang = float(self.ka_aktienCSV.LeseWertAusCSV(key_aktien_dict))
        key_aktien_dict.clear()

        # Anlagebetrag:
        name = 'anlage_betrag'
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        anlage_betrag = float(self.ka_aktienCSV.LeseWertAusCSV(key_aktien_dict))
        key_aktien_dict.clear()

        # Kurs:
        name = 'kurs_anfang'
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        kurs_anfang = float(self.ka_aktienCSV.LeseWertAusCSV(key_aktien_dict))
        key_aktien_dict.clear()

        # Anteile_neu:
        name = 'anteile_neu'
        anteile_neu = anlage_betrag / kurs_anfang
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = anteile_neu
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # Anteile_ende:
        name = 'anteile_ende'
        anteile_ende = anteile_anfang + anteile_neu
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = anteile_ende
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # Kurs_ende:
        name = 'kurs_ende'
        kurs_ende = self.KursEnde(kurs_anfang)
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = kurs_ende
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # Kursveränderung:
        name = 'kurs_veraenderung'
        kurs_veraenderung = kurs_ende - kurs_anfang
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = kurs_veraenderung
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # aktien_ende:
        name = 'aktien_ende'
        aktien_ende = anteile_ende * kurs_ende
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = aktien_ende
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()

        # Kurserträge:
        name = 'kursertraege'
        kursertraege = anteile_ende * (kurs_ende - kurs_anfang)
        key_aktien_dict['jahr'] = jahr
        key_aktien_dict['name'] = name
        key_aktien_dict['wert'] = kursertraege
        self.ka_aktienCSV.SchreibeInCSV(key_aktien_dict)
        key_aktien_dict.clear()
        

    def KursEnde(self, kurs_anfang):
            
            for i in range(0,12):  #monatliche Fortschreibung der Aktienkurse
                zufallszahl = random.random()
                xi = NormalDist(mu=self.ex_aktien, sigma=self.sigma).inv_cdf(zufallszahl)
                kurs_anfang = kurs_anfang * (1 + xi)
                print('KA_Aktien:KursEnde: i= ' + str(i) + 'aktien_kurs= ' +str(kurs_anfang))    
            
            return kurs_anfang




 
