# -*- coding: utf-8 -*-

class Hilfe_System():    
    def __init__(self):
        pass
    
    def DictAusDatum(self, datum_str):
        jahr=datum_str[0:4]
        monat=datum_str[4:6]   
        tag=datum_str[6:8]
        dic={}
        dic['jahr'] = jahr
        dic['monat'] = monat
        dic['tag'] = tag
        dic['jjjjmmtt'] = datum_str
        
        s=''
        if tag[0]=='0':
            s=tag[1]
        else:
            s=tag
        
        dic['tt_int']=int(s)

        s=''
        if monat[0]=='0':
            s=monat[1]
        else:
            s=monat
        
        dic['mm_int']=int(s)
        dic['jjjj_int']=int(jahr)
        
        return dic

class VerketteteListe(object):
    
    def __init__(self, vsnr, histnr, von, bis, nxt):
        self.vsnr=vsnr
        self.histnr=histnr
        self.von=von
        self.bis=bis
        self.nxt=nxt

class ZahlenFormatieren():
    def __init__(self):
        self.darstellungKomma = ','
        self.darstellungTausendtrennzeichen = '.'
    
    
    def FloatZuStgMitTausendtrennzeichen(self, wert_f_alt, nachkommastellen):
        wert_f = round(wert_f_alt, nachkommastellen)
        wert_s = str(wert_f)
    
        wert_s_neu = ''
        laenge = len(wert_s)
        iVorKomma = -1
        kommaPosition = wert_s.find('.')
        for i in range(laenge-1, -1, -1):
            s = wert_s[i]
            if i == kommaPosition:
                s = ','
                iVorKomma = 1
            else:
                if i > kommaPosition:
                    #d.h. noch im Nachkommabereich:
                    pass
                else:
                    #im Vorkommabereich:
                    if iVorKomma % 3 == 0:
                        if i != 0:
                            s = '.' + s
    
                    iVorKomma += 1
    
            wert_s_neu = s + wert_s_neu
    
        return wert_s_neu  
        
    def StgMitTausendtrennzeichenZuFloat(self, wert_s_alt):
        wert_s_neu = wert_s_alt.replace('.', '')
        wert_s_neu = wert_s_neu.replace(',', '.')
        wert_f_neu = float(wert_s_neu)
        return wert_f_neu
    