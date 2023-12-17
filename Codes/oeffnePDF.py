# -*- coding: utf-8 -*-

from pathlib import Path
import PyPDF2
from colorama import Fore, Back, Style

class OeffnePDF():
    
    def __init__(self, file):
        
        self.dateiPDF = file

        datei = Path(self.dateiPDF)
        if datei.is_file():
            print("Datei " + self.dateiPDF + " existiert.")
            self.ZeigePDF()
        else:
            print(Fore.RED + "Datei " + self.dateiPDF + " existiert nicht!!!")
            print(Style.RESET_ALL)

    def ZeigePDF(self):
        # creating a pdf File object of original pdf
        pdfFileObj = open(self.dateiPDF, 'rb')
    
        # creating a pdf Reader object
        pdfReader = PyPDF2.PdfReader(pdfFileObj)
    
        # creating a pdf writer object for new pdf
        pdfWriter = PyPDF2.PdfWriter(pdfReader)
    
        # closing the original pdf file object
        pdfFileObj.close()
