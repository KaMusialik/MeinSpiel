# -*- coding: utf-8 -*-

from random import gauss
import math

class Hilfe_Statistik(object):

    def __init__(self, stat_dict):
        #Standartnormalverteilung:
        self.ex = 0
        self.risiko=stat_dict.get('risiko')
        sigma=1
        
        if self.risiko == 'normal':
            self.sigma = sigma
        elif self.risiko == 'risky' or self.risiko == 'gross':
            self.sigma = 2*sigma
        elif self.risiko == 'high_risky' or self.risiko == 'sehrgross':
            self.sigma = 3*sigma
        else:
            self.sigma = 5*sigma
        
    def NeuerWert(self): 
        wert = gauss(self.ex, self.sigma)
        wert = wert/(3*self.sigma)
        if wert > 1:
            wert = 1
        elif wert < -1:
            wert = -1
        
        return wert
    
    def NeueZufallszahl(self):
        #hier wird eine Zufallszahl erstellt:
        x = gauss(self.ex, self.sigma)
        return x
    
    def Phi(self, x):
        #Wert der Normalverteilung für x, d.h. P(X < x):
        wert = (1+math.erf((x-self.ex) / self.sigma / math.sqrt(2)))/2
        return wert

