import pandas as pd
from pathlib import Path


class KA_rentenCSV():
    
    def __init__(self, f_dict):

        self.f_dict = f_dict         

        self.file = f_dict.get('file_kapitalanlagen_renten_csv')
        datei = Path(self.file)
        if datei.is_file():
            text = 'KA_rentenCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'KA_rentenCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

        self.file_struktur = f_dict.get('file_renten_csv_struktur')
        datei = Path(self.file)
        if datei.is_file():
            text = 'KA_rentenCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'KA_rentenCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

    def LeseRentenCSV(self, key_dict):
        datei = self.file
        struktur = self.file_struktur
        df=pd.read_csv(datei, sep=";", dtype=struktur)
       
        jahr=int(key_dict.get('jahr'))
        nr=int(key_dict.get('nr'))
        von=int(key_dict.get('von'))
        bis=int(key_dict.get('bis'))
        name=str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.nr == nr) & (df.von==von) & (df.bis==bis) & (df.name==name)]
        
        if df1.empty:
            wert=0
            text='ka_renten/LeseRentenSaCSV: Eintrag in der Tabelle fuer Renten nicht gefunden. Es wurde null verwendet: nr='+str(nr)+' von='+str(von)+' bis='+str(bis)+' name='+str(name)
            print(text)
        else:
            index=df1.index[0]
            wert=df1.at[index, 'wert']
        
        return wert   
