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
            wert=0
            text='BilanzCSV/LeseBilanzCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: termin='+str(print(key_dict))
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
       
        return float(wert)   
