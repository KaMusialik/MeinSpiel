import pandas as pd
from pathlib import Path



class KostenCSV():
    
    def __init__(self, f_dict):

        self.f_dict = f_dict         

        self.file = f_dict.get('file_kosten')
        datei = Path(self.file)
        if datei.is_file():
            text = 'KostenCSV/init: Die Datei ' + self.file + ' existiert. Also alles okay. Es geht weiter'
            print(text)
        else:
            text = 'KostenCSV/init: Die Datei ' + self.file + ' existiert nicht! Ups! Baustelle!'
            print(text)

        self.file_struktur = f_dict.get('file_kosten_struktur')

    def LegeTabelleKostenCSVAn(self):
        datei = self.file
        
        ocsv = pd.DataFrame()
        ocsv['jahr'] = None
        ocsv['vsnr'] = None
        ocsv['avbg'] = None
        ocsv['name'] = None
        ocsv["wert"] = None
        
        ocsv[['jahr', 'vsnr', 'avbg', 'name', 'wert']] = ocsv[['jahr', 'vsnr', 'avbg', 'name', 'wert']].astype(str)
        ocsv.to_csv(path_or_buf=datei, sep=';', index=False)
        
        
    def SchreibeInKosten(self, eintrag_dict):
        datei = self.file
        
        jahr = eintrag_dict.get('jahr')
        vsnr = eintrag_dict.get('vsnr')
        avbg = eintrag_dict.get('avbg')
        name = eintrag_dict.get('name')
        wert = eintrag_dict.get('wert')
                
        text = str(jahr) + ';' + str(vsnr) + ';' + str(avbg) + ';' + str(name) + ';' + str(wert) + '\n'
        
        f=open(datei, "a")
        f.write(text)    
        f.close()

    def LeseKostenCSV(self, key_dict):  # hier wird aus der KostenCSV gelesen
        datei = self.file
        struktur = self.file_struktur
        df = pd.read_csv(datei, sep=";", dtype=struktur)

        # jahr und name sind Mindesteingaben sie müssen existieren:
        jahr = int(key_dict.get('jahr'))
        name = str(key_dict.get('name'))

        df1 = df[(df.jahr == jahr) & (df.name == name)]
        if df1.empty:
            wert = 0.0
            text = 'KostenCSV/LeseKostenCSV: für diesen key wurde nichts gefunden. Es wurde null verwendet. Key: jahr=' + str(jahr) + ' name=' + str(name)
            print(text)
            return wert

        vsnr = int(key_dict.get('vsnr'))
        if vsnr == 999:  # das bedeutet, dass über alle vsnr gruppiert werden soll, bzw. sollte das Feld vsnr nicht weiterbetrchtet werden
            df2 = df1[['avbg', 'wert']]
        else:
            df2 = df1[(df1.vsnr == vsnr)]
            if df2.empty:
                wert = 0.0
                text = 'KostenCSV/LeseKostenCSV: Eintrag in der Tabelle KostenCSV nicht gefunden. Es wurde null verwendet: jahr=' + str(
                        jahr) + ' name=' + str(name) + ' vsnr= ' + str(vsnr)
                print(text)
                return wert
            else:  # hier darf nur ein Satz sein.
                if len(df2) == 1:  # alles okay
                    index = df2.index[0]
                    wert = float(df2.at[index, 'wert'])
                    return wert

        avbg = str(key_dict.get('avbg'))
        if avbg == '999':  # das bedeutet, dass über alle avbg gruppiert werden soll
            wert = df2['wert'].sum()
            return wert
        else:
            df3 = df2[(df2.avbg == avbg)]

        if df3.empty:
            wert = 0.0
            text = 'KostenCSV/LeseKostenCSV: Eintrag in der Tabelle KostenCSV nicht gefunden. Es wurde null verwendet: jahr=' + str(
                    jahr) + ' name=' + str(name) + ' vsnr= ' + str(vsnr) + ' avbg= ' + str(avbg)
            print(text)
            return wert
        else:  # hier darf nur ein Satz sein.
            if len(df3) == 1:  # alles okay
                index = df3.index[0]
                wert = float(df3.at[index, 'wert'])
                return wert
            else:  # wenn mehr als ein Satz hier sind, dann ist etwas falsch
                wert = 0.0
                text = 'KostenCSV/LeseKostenCSV: Es wurden zu viele Einträge in der Tabelle KostenCSV gefunden. Da ist etwas falsch. Key: jahr=' + str(
                    jahr) + ' name=' + str(name) + ' vsnr= ' + str(vsnr) + ' avbg= ' + str(avbg)
                print(text)
                return wert




