# -*- coding: utf-8 -*-

import random
import math

class Hilfe_Statistik(object):

    def __init__(self, stat_dict):
        #Standartnormalverteilung:
        self.risiko = stat_dict.get('risiko')
        sigma = 0.1
        
        if self.risiko == 'normal':
            self.sigma = sigma
        elif self.risiko == 'risky' or self.risiko == 'gross':
            self.sigma = 2.0 * sigma
        elif self.risiko == 'high_risky' or self.risiko == 'sehrgross':
            self.sigma = 3.0 * sigma
        else:
            self.sigma = 5.0 * sigma

        self.ex = 3.0 * sigma
        
    def MeineZufallszahl(self):
        zf = random.uniform(0, 6.0 * self.sigma)
        prozAbweichung = (zf - self.ex) / self.ex
        return prozAbweichung
    
    def NeuerWert(self): 
        wert = random.gauss(self.ex, self.sigma)
        wert = wert/(3*self.sigma)
        if wert > 1:
            wert = 1
        elif wert < -1:
            wert = -1
        
        return wert
    
    def NeueZufallszahl(self):
        #hier wird eine Zufallszahl erstellt:
        x = random.gauss(self.ex, self.sigma)
        return x
    
    def Phi(self, x):
        #Wert der Normalverteilung für x, d.h. P(X < x):
        wert = (1+math.erf((x-self.ex) / self.sigma / math.sqrt(2)))/2
        return wert

