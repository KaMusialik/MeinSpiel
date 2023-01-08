# -*- coding: utf-8 -*-

import protokoll as prot
import produkt as prod

class Produktmanager():
    
    def __init__(self, f_dict, dic):
        
        pfad_pm=f_dict.get('work_dir_pm')

        vsnr=dic.get('vsnr')
        histnr=dic.get('histnr')
        gevo=dic.get('gevo')
        
        file_protokoll = str(pfad_pm) + 'protokoll_pm_' + str(vsnr) + '_' + str(histnr) + '_' + str(gevo)+'.txt'
        self.oprot = prot.Protokoll(file_protokoll)

        self.oprod = prod.Produkt(f_dict)
        
        #Produktdaten werden geholt:
        self.produkt = {}
        tkz = dic.get('tkz')
        self.produkt['tkz'] = tkz
        von = dic.get('von')
        self.produkt['von'] = von
        
        self.produkt = self.oprod.LeseProduktDaten(self.produkt)
        
    def HoleWertFloat(self, dic, name):
        s=str(dic.get(name))
        s.strip()
        
        try:
            wert=float(s)

        except ValueError:
            wert=0.0

        return wert
        
    def Rechne(self, vertrag_alt, vertrag_neu):
        if vertrag_neu.get('gevo') == 'Neuzugang':
            vertrag_neu = self.Beitrag(vertrag_neu)
            vertrag_neu = self.Versicherungssumme(vertrag_neu)
            vertrag_neu = self.Beitragssumme(vertrag_neu)
            vertrag_neu = self.KostenImBeitrag(vertrag_neu)
            
        return vertrag_neu
            
    def FortschreibungVonBis(self, von_dict, bis_dict, vertrag):
        if int(von_dict.get('jahr')) != int(bis_dict.get('jahr')):
            self.oprot.SchreibeInProtokoll('FortschreibungVonBis: Fortschreibung nicht möglich, da jahre in von bis nicht identisch!')

        if int(von_dict.get('monat')) > int(bis_dict.get('monat')):
            self.oprot.SchreibeInProtokoll('FortschreibungVonBis: Fortschreibung nicht möglich, da monate in von und bis nicht passen!')
            
        vertrag['avbg']=self.produkt.get('avbg')
        vertrag['rz']=self.produkt.get('rz')
        vertrag=self.Bilanz_Beitrag(von_dict, bis_dict, vertrag)
        vertrag=self.Bilanz_Deckungsrueckstellung(von_dict, bis_dict, vertrag)
        
        return vertrag
    
    def Bilanz_Beitrag(self, von_dict, bis_dict, vertrag):
        #hier werden die bilanziellen Beiträge, also die auf das Jahresende abgegrentzten Beiträge gerechnet:
        von_mm = int(von_dict.get('monat'))
        bis_mm = int(bis_dict.get('monat'))
        faktor =  (bis_mm+1-von_mm)/12 
        
        bruttojahresbeitrag = float(vertrag.get('bruttojahresbeitrag'))
        bruttozahljahresbeitrag = float(vertrag.get('bruttozahljahresbeitrag'))
        
        bil_gebuchter_beitrag = faktor * bruttozahljahresbeitrag
        vertrag['bil_gebuchter_beitrag'] = bil_gebuchter_beitrag
        
        bil_verdienter_beitrag_nw216 = bil_gebuchter_beitrag
        vertrag['bil_verdienter_beitrag_nw216'] = bil_verdienter_beitrag_nw216
        
        bil_bruttojahresbeitrag = faktor * bruttojahresbeitrag
        
        rb_quote = self.GetWert(self.produkt, 'rb_quote', 'f')
        
        bil_risikobeitrag_nw216 = bil_bruttojahresbeitrag * rb_quote
        vertrag['bil_risikobeitrag_nw216'] = bil_risikobeitrag_nw216        
        
        vk_beitrag = float(vertrag.get('beitragszuschlagFuerVerwaltung'))
        bil_vkbeitrag_nw216 = faktor * vk_beitrag
        vertrag['bil_vk_beitrag_nw216'] = bil_vkbeitrag_nw216
        
        ak1_beitrag = float(vertrag.get('ak1'))
        bil_ak1_beitrag = faktor * ak1_beitrag
        
        ak2_beitrag = float(vertrag.get('ak2'))
        bil_ak2_beitrag = faktor * ak2_beitrag
        
        ak3_beitrag = float(vertrag.get('ak3'))
        bil_ak3_beitrag = faktor * ak3_beitrag
 
        bil_ak_beitrag_nw216 = bil_ak1_beitrag + bil_ak2_beitrag + bil_ak3_beitrag
        vertrag['bil_ak_beitrag_nw216'] = bil_ak_beitrag_nw216
        
        bil_sparbeitrag_nw216 = bil_verdienter_beitrag_nw216 - (bil_risikobeitrag_nw216 + bil_vkbeitrag_nw216 + bil_ak_beitrag_nw216)
        vertrag['bil_sparbeitrag_nw216'] = bil_sparbeitrag_nw216
        
        return vertrag

    def Bilanz_Deckungsrueckstellung(self, von, bis, vertrag):
        
        spb = self.HoleWertFloat(vertrag, 'bil_sparbeitrag_nw216')
        rz = self.HoleWertFloat(self.produkt, 'rz')
        
        derue1_anfang = self.HoleWertFloat(vertrag, 'bil_derue1_anfang')
        
        rz_zinsen = (derue1_anfang+spb)*rz
        
        derue1_ende = derue1_anfang+spb+rz_zinsen
        
        rw=max(derue1_ende*0.8, 0)
        
        derue2_ende=max(derue1_ende,rw,0)
        
        bio_nachreservierung_ende=max(derue1_ende*0.1, 0)

        derue3_ende=derue2_ende+bio_nachreservierung_ende
        
        zzr_nachreservierung_ende=max(derue1_ende*0.3,0)
        
        derue5_ende=derue3_ende+zzr_nachreservierung_ende
        
        unisex_nachreservierung_ende=max(derue1_ende*0.0,0)
        
        derue7_ende=derue5_ende+unisex_nachreservierung_ende
        
        vertrag['bil_rz_nw217'] = rz_zinsen
        vertrag['bil_derue1_ende'] = derue1_ende
        vertrag['bil_rueckkaufswert'] = rw
        vertrag['bil_derue2_ende'] = derue2_ende
        vertrag['bil_bio_nachreservierung_ende'] = bio_nachreservierung_ende
        vertrag['bil_derue3_ende'] = derue3_ende
        vertrag['bil_zzr_nachreservierung_ende'] = zzr_nachreservierung_ende
        vertrag['bil_derue5_ende'] = derue5_ende
        vertrag['bil_unisex_nachreservierung_ende'] = unisex_nachreservierung_ende
        vertrag['bil_derue7_ende'] = derue7_ende
        
        return vertrag
    
    def Beitrag(self, vertrag):
        #hier werden alle Beiträge ausgerechnet:
            
        bruttobeitrag = float(self.produkt.get('bruttobeitrag')) #Bruttojahresbeitrag ist im Produkt abgelegt
        
        beitragsniveau = float(vertrag.get('beitragsniveau')) #Beitragsniveau wurde im Dialog vorbelegt
        
        vertrag['bruttojahresbeitrag'] = bruttobeitrag #Beitrag vor Rabatt
        
        bruttozahljahresbeitrag = bruttobeitrag * beitragsniveau #Zahlbeitrag nach Rabatt
        vertrag['bruttozahljahresbeitrag'] = bruttozahljahresbeitrag #Zahlbeitrag nach Rabatt
        
        #Der Beitrag wird erhöht bzw. reduziert um einen um einen Beitragsrabatt:
        vertrag['beitragsrabatt'] = bruttobeitrag * (1 - beitragsniveau)
                
        return vertrag        

    def Beitragssumme(self, vertrag):

        bruttobeitrag = float(vertrag.get('bruttozahljahresbeitrag'))

        laufzeit = float(vertrag.get('laufzeit'))
        
        vertrag['beitragssumme'] = bruttobeitrag * laufzeit
        
        return vertrag        

    def Versicherungssumme(self, vertrag):

        bruttojahresbeitrag = vertrag.get('bruttojahresbeitrag')
        
        vs = bruttojahresbeitrag * 12
        
        vertrag['versicherungssumme'] = vs
        
        return vertrag    

    def KostenImBeitrag(self, vertrag):
        
        rabatt = float(vertrag.get('beitragsrabatt')) #der Rabatt reduziert die VK-Zuschläge
        
        bruttobeitrag = float(vertrag.get('bruttojahresbeitrag'))
        
        beitragssumme = float(vertrag.get('beitragssumme'))
        
        bzd = int(vertrag.get('laufzeit'))

        #kostenzuschläge für Verwaltungskosten:
        beta1 = float(self.produkt.get('beta1')) 
        vk = beta1 * bruttobeitrag - rabatt
        
        vertrag['beitragszuschlagFuerVerwaltung'] = vk

        #kostenzuschläge für Abschlusskosten:
        alpha1 = float(self.produkt.get('alpha1')) 
        alpha2 = float(self.produkt.get('alpha2')) 
        alpha3 = float(self.produkt.get('alpha3')) 

        ak1 = alpha1 * beitragssumme / bzd
        vertrag['ak1'] = ak1

        ak2 = alpha2 * beitragssumme / bzd
        vertrag['ak2'] = ak2

        ak3 = alpha3 * beitragssumme / bzd
        vertrag['ak3'] = ak3
        
        return vertrag
    
    def GetWert(self, vertrag, name, typ):

        if name in (None, ''):
            text = 'PM/GetWert: keine name!' 
            self.oprot.SchreibeInProtokoll(text)
            wert=0
            return wert
            
        wert=str(vertrag.get(name))
        if wert in (None, ''):
            vsnr=str(vertrag.get('vsnr'))
            text = 'PM/GetWert: bei vsnr: ' +vsnr+ ' zu dem namen: '+str(name)+ ' konnte kein wert zugeordnet werden' 
            self.oprot.SchreibeInProtokoll(text)
            wert=0
            return wert
        
        if typ == 'f':
            wert=float(str(vertrag.get(name)))
        elif typ == 'i':
            wert=int(str(vertrag.get(name)))
        else:
            text = 'PM/GetWert: typ falsch ' + str(typ) 
            self.oprot.SchreibeInProtokoll(text)
            wert=0
            
        return wert
    
    
    def JahrAusDatum(self, datum):
        jahr=datum[0:4]
        return jahr

    def MonatAusDatum(self, datum):
        monat=datum[5:6]
        return monat

    def TagAusDatum(self, datum):
        tag=datum[7:8]
        return tag
    
            
