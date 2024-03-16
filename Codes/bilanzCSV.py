import pandas as pd
from pathlib import Path


class BilanzCSV():
    
    def __init__(self, f_dict):

        self.f_dict = f_dict         

        self.file = f_dict.get('file_bilanz')
        datei = Path(self.file)
        if datei.is_file():
            text = 'BilanzCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'BilanzCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

        self.file_struktur = f_dict.get('file_bilanz_struktur')
        datei = Path(self.file)
        if datei.is_file():
            text = 'BilanzCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'BilanzCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

    def LeseBilanzCSV(self, key_dict):
        datei = self.file
        struktur = self.file_struktur
        df = pd.read_csv(datei, sep=";", dtype=struktur)
       
        jahr = int(key_dict.get('jahr'))
        rl = str(key_dict.get('rl'))
        avbg = str(key_dict.get('avbg'))
        name = str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.rl == rl) & (df.avbg == avbg) & (df.name == name)]
        if df1.__len__() == 0:
            wert = 0.0
            text = 'BilanzCSV/LeseBilanzCSV: Eintrag in der Tabelle nicht gefunden. Es wird null verwendet. Es muss noch nichts heissen .... . Input: ' + str(key_dict)
            print(text)
        else:
            index = df1.index[0]
            wert = df1.at[index, 'wert']
       
        return float(wert)

    def KumuliereAlleAvbgInBilanz(self, key_dict):  # hier werden die werte für alle avbg zusammenaddiert (kumuliert)
        datei = self.file
        struktur = self.file_struktur

        df = pd.read_csv(datei, sep=";", dtype=struktur)

        jahr = int(key_dict.get('jahr'))
        rl = str(key_dict.get('rl'))
        name = key_dict.get('name')

        df1 = df[(df.jahr == jahr) & (df.rl == rl) & (df.avbg != '999') & (df.name == str(name))]

        if df1.empty:
            wert = 0.0
            text = 'BilanzCSV/KumuliereAlleAvbgInBilanz: Eintrag in der Tabelle nicht gefunden. Keine Kummulierung möglich!'
            print(text)
        else:
            df2 = df1[['name', 'wert']]

            df3 = df2.groupby('name')['wert'].sum()

            if len(df3) != 1:  # es wir genau ein Satz erwartet. Sonst gibt es hier ein Problem:
                wert = 0.0
                text = 'BilanzCSV/KumuliereAlleAvbgInBilanz: Unerwartete anzahl der kummulierten Sätze!' + str(df3)
                print(text)
            else:
                df4 = df3.reset_index()
                index = df4.index[0]
                wert = df4.at[index, 'wert']

        return float(wert)

    def SchreibeInBilanzCSV(self, key_dict):
        datei = self.file
        struktur = self.file_struktur

        jahr = int(key_dict.get('jahr'))
        rl = key_dict.get('rl')
        avbg = key_dict.get('avbg')
        name = key_dict.get('name')
        wert = float(key_dict.get('wert'))

        if self.LeseBilanzCSV(key_dict) != 0.0:
            self.ZeileLoeschenInBilanzCSV(key_dict)

        text = str(jahr) + ';' + str(rl) + ';' + str(avbg) + ';' + str(name) + ';' + str(wert) + '\n'
        f = open(datei, "a")
        f.write(text)
        f.close()

    def ZeileLoeschenInBilanzCSV(self, key_dict):
        datei = self.file
        struktur = self.file_struktur

        jahr = int(key_dict.get('jahr'))
        rl = key_dict.get('rl')
        avbg = key_dict.get('avbg')
        name = key_dict.get('name')

        if self.LeseBilanzCSV(key_dict) != 0.0:  # da ist schonetwas in der Tabelle
            df = pd.read_csv(datei, sep=";", dtype=struktur)  # in diesem df muss der eine Datensatz gelöscht werden
            index = self.ErmillteIndexZumLoeschen(df, key_dict)
            if index == 0:  # die Zeile zum löschen wurde nicht eindeutig gefunden
                text = 'BilanzCSV/ZeileLoeschenInBilanzCSV: Eintrag in der Bilanztabelle konnte nicht geslöscht werden: jahr=' + str(
                    jahr) + ' rl=' + str(rl) + ' avbg=' + str(avbg) + ' name=' + str(name)
                print(text)
                return
            else:
                df1 = df.drop([index])
                df1.to_csv(datei, sep=';', index=False)
                text = 'BilanzCSV/ZeileLoeschenInBilanzCSV: Eintrag in der Bilanztabelle wurde geslöscht: jahr=' + str(
                    jahr) + ' rl=' + str(rl) + ' avbg=' + str(avbg) + ' name=' + str(name)
                print(text)

    def ErmillteIndexZumLoeschen(self, df, key_dict):
        jahr = int(key_dict.get('jahr'))
        rl = key_dict.get('rl')
        avbg = key_dict.get('avbg')
        name = key_dict.get('name')

        df1 = df[(df.jahr == jahr) & (df.rl == rl) & (df.avbg != avbg) & (df.name == str(name))]
        wert = df1.index

        if len(wert) == 1:  # es wurde, wie erwartet, nur ein wert gefunden. es ist okay
            return wert[0]  # index nr wird zurückgegeben
        else:
            return 0
