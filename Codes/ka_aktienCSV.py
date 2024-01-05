import pandas as pd
from pathlib import Path


class KA_AktienCSV():
    
    def __init__(self, f_dict):

        self.f_dict = f_dict         

        self.file = f_dict.get('file_kapitalanlagen_aktien_csv')
        datei = Path(self.file)
        if datei.is_file():
            text = 'KA_AktienCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'KA_AktienCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

        self.file_struktur = f_dict.get('file_aktien_csv_struktur')


    def LeseWertAusCSV(self, key_dict):
        datei = self.file
        df = pd.read_csv(datei, sep=";", dtype=self.file_struktur)
       
        jahr = int(key_dict.get('jahr'))
        name = str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.name == name)]
        if df1.__len__() == 0:
            wert = 0.0
            text = 'KA_AktienCSV/LeseWertAusCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
            print(text)
        else:
            index = df1.index[0]
            wert = df1.at[index, 'wert']
       
        return float(wert)   
    
    def SchreibeInCSV(self, key_dict):
        datei = self.file
        
        jahr = key_dict.get('jahr')
        name = key_dict.get('name')
        wert = key_dict.get('wert')
        
        if self.LeseWertAusCSV(key_dict) != 0:
            self.ZeileLoeschenInCSV(key_dict)
        
        text = str(jahr) +';' + str(name) + ';' + str(wert)+'\n'
        f = open(datei, "a")
        f.write(text)    
        f.close()      

    def ErmillteIndexZumLoeschen(self, df, key_dict):
        jahr = int(key_dict.get('jahr'))
        name = str(key_dict.get('name'))
        
        df1 = df[(df['jahr'] == jahr) & (df['name'] == name)]
        wert = df1.index
        
        if len(wert) == 1:  # es wurde, wie erwartet, nur ein wert gefunden. es ist okay
            return wert[0]  # index nr wird zurückgegeben
        else:
            return 0 

    def ZeileLoeschenInCSV(self, key_dict):
        datei = self.file

        jahr = int(key_dict.get('jahr'))
        name = str(key_dict.get('name'))
        
        if self.LeseKapitalanlageCSV(key_dict) != 0:  # da ist schon etwas in der Tabelle
            df = pd.read_csv(datei, sep=';', dtype=self.file_struktur)  # in diesem df muss der eine Datensatz gelöscht werden 
            index = self.ErmillteIndexZumLoeschen(df, key_dict)
            if index == 0:  # die Zeile zum löschen wurde nicht eindeutig gefunden
                text='KA_AktienCSV/ZeileLoeschenInCSV: Eintrag in der KapitalanlagenCSV konnte nicht gelöscht werden. Daten: jahr='+str(jahr)+' topf='+str(topf)+' name='+str(name)
                print(text)
                return
            else:
                df1 = df.drop([index])
                df1.to_csv(datei, ';', index=False)
                text='KA_AktienCSV/ZeileLoeschenInCSV: Eintrag in der Bilanztabelle geloescht: jahr='+str(jahr)+' topf='+str(topf)+' name='+str(name)
                print(text)
