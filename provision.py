# -*- coding: utf-8 -*-
import pandas as pd

class Provision():
    def __init__(self, f_dict):
        
        self.file_provision = f_dict.get('file_provision')
        self.dtype_dic= f_dict.get('file_provision_struktur')
        
    def BereiteProvisionVor(self):
        self._LegeProvisiontabelleAn()
    
    
    def _LegeProvisiontabelleAn(self):
        datei = self.file_provision
        ocsv = pd.DataFrame()
        
        ocsv["vsnr"]=None
        ocsv["jahr"]=None
        ocsv["gevo"]=None
        ocsv["name"]=None
        ocsv["wert"]=None
        ocsv.to_csv(datei, ';', index=False)

    
    def LeseAusProvisionCSV(self, key_dict):
        datei = self.file_provision
        df=pd.read_csv(datei, sep=";", dtype=self.dtype_dic)
       
        jahr = int(key_dict.get('jahr'))
        vsnr = int(key_dict.get('vsnr'))
        gevo = str(key_dict.get('gevo'))
        name = str(key_dict.get('name'))
 
        df1 = df[(df.jahr == jahr) & (df.vsnr == vsnr) & (df.gevo == gevo) & (df.name == name)]

        if df1.empty:
            wert = 0
            text='provision/LeseAusProvisionCSV: Eintrag in der Tabelle nicht gefunden. Es wurde null verwendet: '+str(key_dict)
        else:
            if df1.__len__() != 1:
                wert=999999999
                text='provision/LeseAusProvisionCSV: mehrere Eintraeg in der Tabelle gefunden. Es wurde ein Wert von '+str(wert)+ ' verwendet: '+str(key_dict)
            else:
                index=df1.index[0]
                wert=df1.at[index, 'wert']

        return wert   

    
    def BerechneAP(self, jahr):
        
        datei = self.file_provision
                
        df = pd.read_csv(datei, sep=";")
        df1 = df[( (df.jahr == jahr) & (df.gevo == 'Neuzugang') )]

        #für welche Verträge muss die AP berechnet werden?
        df2=df1.groupby(['vsnr']).count().reset_index()
    
        listeDerVertraege = []
        for index, row in df2.iterrows():
            wert = str(row['vsnr'])
            listeDerVertraege.append(wert)
        
        key_dict = {}
        key_dict['jahr'] = jahr
        key_dict['gevo'] = 'Neuzugang'
        for vsnr in listeDerVertraege:
            key_dict['vsnr'] = vsnr
            
            name = 'beitragssumme'
            key_dict['name'] = name
            bs = float(self.LeseAusProvisionCSV(key_dict))

            name = 'provisionsniveau'
            key_dict['name'] = name
            pv = float(self.LeseAusProvisionCSV(key_dict))

            name = 'provisionMarkt'
            key_dict['name'] = name
            pm = float(self.LeseAusProvisionCSV(key_dict))
            
            ap = pm * pv * bs
            
            key_dict['name'] = 'ap'
            self.SchreibeInProvisionCSV(key_dict, ap)
            
        
    
    def SchreibeInProvisionCSV(self, key, wert):
        datei=self.file_provision
        
        vsnr = key.get('vsnr')
        jahr = key.get('jahr')
        gevo = key.get('gevo')
        name = key.get('name')
        
        text=str(vsnr) + ";" + str(jahr) + ";" + str(gevo) + ";" + str(name) + ";" + str(wert) + "\n"
        
        f=open(datei, "a")
        f.write(text)    
        f.close()    