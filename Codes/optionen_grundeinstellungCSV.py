import pandas as pd
from pathlib import Path

class Optionen_GrundeinstellungCSV():
    
    def __init__(self, f_dict):

        self.f_dict = f_dict         

        self.file = f_dict.get('optionen_file_grundeinstellungwindow')
        datei = Path(self.file)
        if datei.is_file():
            text = 'Optionen_GrundeinstellungCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'Optionen_GrundeinstellungCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

        self.file_struktur = f_dict.get('optionen_file_grundeinstellungwindow_struktur')


    def LeseWertAusCSV(self, key_dict):
        datei = self.file
        df = pd.read_csv(datei, sep=";", dtype=self.file_struktur)
       
        key = str(key_dict.get('key'))
 
        df1 = df[(df.key == key)]
        if df1.__len__() == 0:
            wert = 0.0
            text = 'Optionen_GrundeinstellungCSV/LeseWertAusCSV: Eintrag in der Tabelle Optionen_GrundeinstellungCSV nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            print(text)
        else:
            index = df1.index[0]
            wert = df1.at[index, 'wert']
       
        return wert   
    
    def SchreibeInCSV(self, key_dict):
        datei = self.file
        
        key = key_dict.get('key')
        wert = key_dict.get('wert')
        
        if self.LeseWertAusCSV(key_dict) != 0:
            self.ZeileLoeschenInCSV(key_dict)
        
        text = str(key) + ';' + str(wert)+'\n'
        f = open(datei, "a")
        f.write(text)    
        f.close()      

    def ErmillteIndexZumLoeschen(self, df, key_dict):
        key = str(key_dict.get('key'))
        
        df1 = df[(df['key'] == key)]
        wert = df1.index
        
        if len(wert) == 1:  # es wurde, wie erwartet, nur ein wert gefunden. es ist okay
            return wert[0]  # index nr wird zurückgegeben
        else:
            return 0 

    def ZeileLoeschenInCSV(self, key_dict):
        datei = self.file

        key = str(key_dict.get('key'))
        
        if self.LeseWertAusCSV(key_dict) != 0:  # da ist schon etwas in der Tabelle
            df = pd.read_csv(datei, sep=';', dtype=self.file_struktur)  # in diesem df muss der eine Datensatz gelöscht werden 
            indexListe = []
            indexListe = self.ErmillteIndexZumLoeschen(df, key_dict)
            if len(indexListe) == 0:  # die Zeile zum löschen wurde nicht eindeutig gefunden
                text='Optionen_GrundeinstellungCSV/ZeileLoeschenInCSV: Eintrag in der Optionen_GrundeinstellungCSV konnte nicht gelöscht werden. Daten: key='+str(key)
                print(text)
                return
            else:
                df1 = df.drop(indexListe)
                df1.to_csv(path_or_buf=datei, sep=';', index=False)
                text='Optionen_GrundeinstellungCSV/ZeileLoeschenInCSV: Eintrag in der Optionen_GrundeinstellungCSV geloescht: key='+str(key)
                print(text)

    def ErmillteIndexZumLoeschen(self, df, key_dict):

        key = str(key_dict.get('key'))

        df1 = df[(df['key'] == key)]
        wert = df1.index

        return wert