import protokoll as prot
import pandas as pd
import ka_aktienCSV


class KA_Aktien:
        
    def __init__(self, f_dict):
        file_protokoll = f_dict.get('protokoll_file_aktien')
        self.oprot = prot.Protokoll(file_protokoll)

        self.file_aktien_csv  = f_dict.get('file_kapitalanlagen_aktien_csv')
        self.file_aktien_csv_struktur  = f_dict.get('file_aktien_csv_struktur')

        self.LegeAktienTabelleAn()
        self.ka_aktienCSV = ka_aktienCSV.KA_AktienCSV(f_dict)
    
    def LegeAktienTabelleAn(self):  # Tabelle für Aktien wird angelegt
        datei = self.file_aktien_csv
        ocsv = pd.DataFrame()
        ocsv['jahr'] = None
        ocsv['name'] = None
        ocsv["wert"] = None
        ocsv.to_csv(datei, ';', index=False)
        
        text = 'KA_Aktien/LegeAktienTabelleAn: Tabelle fuer die Aktien wurde angelegt: '+str(datei)
        self.oprot.SchreibeInProtokoll(text)

    def Init_Aktien(self, jahr):  # hier werden die Aktien zu Beginn des GJ initialisiert
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
            return kurs_anfang




 
