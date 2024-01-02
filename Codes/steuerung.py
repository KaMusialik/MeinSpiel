# -*- coding: utf-8 -*-

import sys
import PyQt5.QtCore as core
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.uic as uic

import optionen as opt
import protokoll as prot

import grundeinstellungwindow as gW
import statistikwindow as sW
import produktwindow as pW
import vertragswindow as vW
import guvwindow as guvW
import bilanzWindow
import zeigedatenintabelle as zD

import bilanz as bil
import vertrieb as ver
import antrag as antrag
import system
import kapitalanlagen as kap
import provision
import nachreservierung
import kosten
import vertraegeausfortschreibungwindow


files_dict = {}
# work directory:
files_dict['work_dir'] = '/home/karol/Projekte/MeinSpiel/Dateien/'

# einzelne Dateien:
files_dict['grundeinstellungwindow_file'] = files_dict.get('work_dir')+'grundeinstellungwindow.ui'
files_dict['spielwindow_file'] = files_dict.get('work_dir')+'spielwindow.ui'
files_dict['leereswindow_file'] = files_dict.get('work_dir')+'leereswindow.ui'
files_dict['statistikwindow_file'] = files_dict.get('work_dir')+'statistikwindow.ui'
files_dict['produktwindow_file'] = files_dict.get('work_dir')+'produktwindow.ui'
files_dict['vertragswindow_file'] = files_dict.get('work_dir')+'vertragswindow.ui'
files_dict['guvwindow_file'] = files_dict.get('work_dir')+'guvwindow.ui'
files_dict['bilanzWindow_file'] = files_dict.get('work_dir')+'bilanzWindow.ui'
files_dict['fortschreibungwindow_file'] = files_dict.get('work_dir')+'fortschreibungwindow.ui'

# icons:
files_dict['file_icon_grundeinstellungwindow'] = files_dict.get('work_dir')+'iconGrundeinstellungWindow.png'
files_dict['file_icon_statistikwindow'] = files_dict.get('work_dir')+'iconStatistikWindow.png'
files_dict['file_icon_guvwindow'] = files_dict.get('work_dir')+'iconGuvWindow.png'

# Kapitalanlagen:
files_dict['protokoll_file_kapitalanlagen'] = files_dict.get('work_dir') + 'protokoll_kapitalanlagen.txt'
files_dict['file_kapitalanlagen_csv'] = files_dict.get('work_dir') + 'kapitalanlagen.csv'
files_dict['file_kapitalanlagen_csv_struktur'] = {'jahr': int, 'topf': str, 'name': str, 'wert': float}
files_dict['file_kapitalanlagen_renten_csv'] = files_dict.get('work_dir') + 'ka_renten.csv'
files_dict['file_kapitalanlagen_aktien_csv'] = files_dict.get('work_dir') + 'ka_aktien.csv'
files_dict['file_kapitalanlagen_sa_csv'] = files_dict.get('work_dir') + 'ka_sa.csv'

files_dict['file_grafik_zsk'] = files_dict.get('work_dir')+'grafik_zsk.png'
files_dict['grafik_file_entwicklung_renten'] = files_dict.get('work_dir')+'grafik_renten.png'

files_dict['optionen_file_grundeinstellungwindow'] = files_dict.get('work_dir')+'optionen_grundeinstellungwindow.csv'
files_dict['protokoll_file_grundeinstellungwindow'] = files_dict.get('work_dir')+'protokoll_grundeinstellungwindow.txt'

files_dict['protokoll_file_guvwindow'] = files_dict.get('work_dir')+'protokoll_guvwindow.txt'
files_dict['protokoll_file_bilanzWindow'] = files_dict.get('work_dir')+'protokoll_bilanzWindow.txt'


files_dict['optionen_file_main'] = files_dict.get('work_dir')+'optionen_main.csv'
files_dict['protokoll_file_main'] = files_dict.get('work_dir')+'protokoll_main.txt'

files_dict['optionen_file_vertrieb'] = files_dict.get('work_dir')+'optionen_vertrieb.csv'
files_dict['protokoll_file_vertrieb'] = files_dict.get('work_dir')+'protokoll_vertrieb.txt'
files_dict['file_vertrieb'] = files_dict.get('work_dir')+'vertrieb.csv'

files_dict['optionen_file_nachreservierung'] = files_dict.get('work_dir')+'optionen_nachreservierung.csv'
files_dict['protokoll_file_nachreservierung'] = files_dict.get('work_dir')+'protokoll_nachreservierung.txt'
files_dict['file_nachreservierung'] = files_dict.get('work_dir')+'nachreservierung.csv'
files_dict['file_nachreservierung_struktur'] = {'jahr': int, 'tkz': int, 'name': str, 'wert': str}

# Dateien zu Thema Antrag:
files_dict['optionen_file_antrag'] = files_dict.get('work_dir')+'optionen_antrag.csv'
files_dict['file_system_antrag'] = files_dict.get('work_dir')+'system_antrag.csv'
files_dict['protokoll_file_antrag'] = files_dict.get('work_dir')+'protokoll_antrag.txt'

files_dict['optionen_file_antrag_oe'] = files_dict.get('work_dir')+'optionen_antrag_oe.csv'
files_dict['protokoll_file_antrag_oe'] = files_dict.get('work_dir')+'protokoll_antrag_oe.txt'

files_dict['protokoll_file_bilanz'] = files_dict.get('work_dir')+'protokoll_bilanz.txt'
files_dict['file_bilanz'] = files_dict.get('work_dir')+'bilanz.csv'
files_dict['file_bilanz_start'] = files_dict.get('work_dir')+'bilanz_start.csv'
files_dict['file_bilanz_struktur'] = {'jahr': int, 'rgl': str, 'avbg': str, 'name': str, 'wert': str}

#hier stehen die Produktdaten:
files_dict['file_produkt'] = files_dict.get('work_dir')+'produkt.csv'
files_dict['file_produkt_struktur'] = {'tkz': str, 'sra': str, 'zw': int, 'von': int, 'bis': int, 'name': str, 'wert': str}

#hier stehen die Systemdateien:
files_dict['protokoll_file_system'] = files_dict.get('work_dir')+'protokoll_system.txt'
files_dict['file_system_fortschreibung_struktur'] = {'vsnr': str, 'histnr': int, 'von': int, 'bis': int, 'name': str, 'wert': str}
files_dict['file_system_bestand'] = files_dict.get('work_dir')+'system_bestand.csv'
files_dict['file_system_bestand_struktur'] = {'vsnr': str, 'histnr': int, 'von': int, 'bis': int, 'name': str, 'wert': str}
files_dict['file_system_fortschreibung'] = files_dict.get('work_dir')+'system_fortschreibung.csv'
files_dict['grafik_file_statistik_anzahl'] = files_dict.get('work_dir')+'grafik_statistik_anzahl.png'
files_dict['file_system_statistik'] = files_dict.get('work_dir')+'system_statistik.csv'

#hier stehen die Provisionsdaten:
files_dict['file_provision'] = files_dict.get('work_dir')+'provision.csv'
files_dict['file_provision_struktur'] = { 'vsnr':int, 'jahr':int, 'gevo':str, 'name':str, 'wert':str}
    
files_dict['protokoll_file_statistikwindow'] = files_dict.get('work_dir')+'protokoll_statistikwindow.txt'
files_dict['protokoll_file_produktwindow'] = files_dict.get('work_dir')+'protokoll_produktwindow.txt'
files_dict['protokoll_file_vertragswindow'] = files_dict.get('work_dir')+'protokoll_vertragswindow.txt'

#Dialog für Verträge aus der Fortschreibung:
files_dict['protokoll_file_vertraegeausderfortschreibungwindow'] = files_dict.get('work_dir')+'protokoll_vertraegeausderfortschreibungwindow.txt'
        
#Kosten:
files_dict['optionen_file_kosten'] = files_dict.get('work_dir')+'optionen_kosten.csv'
files_dict['protokoll_file_kosten'] = files_dict.get('work_dir')+'protokoll_kosten.txt'
files_dict['file_kosten'] = files_dict.get('work_dir')+'kosten.csv'
files_dict['file_kosten_struktur'] = { 'jahr':int, 'vsnr':int, 'avbg':str, 'name':str, 'wert':float }


# in diesem dictionary werden Infos zu Kapitalallokation abgelegt:
ka_sa_dict = {}
ka_renten_sa_dict = {}

# in diesem dictionary werden Infos zum Neugeschäft abgelegt:
vertrieb_dict = {}

# Startjahr der Simulation:
jahr_beginn = 2020

files_dict['Startjahr_Simulation'] = jahr_beginn


def LeseGroesseEinesButtonsAus(btn):
    dim_dict = {}
    w = btn.width()
    h = btn.height()
    dim_dict['hoehe'] = h
    dim_dict['breite'] = w
    return dim_dict


def LegeDefoultEinstellungenfest():
    index = wSpielwindow.comboBox_L1.findText("5")
    wSpielwindow.comboBox_L1.setCurrentIndex(index)
    index = wSpielwindow.comboBox_L2.findText("10")
    wSpielwindow.comboBox_L2.setCurrentIndex(index)
    index = wSpielwindow.comboBox_L3.findText("20")
    wSpielwindow.comboBox_L3.setCurrentIndex(index)

    index = wSpielwindow.comboBox_A1.findText("50")
    wSpielwindow.comboBox_A1.setCurrentIndex(index)
    index = wSpielwindow.comboBox_A2.findText("30")
    wSpielwindow.comboBox_A2.setCurrentIndex(index)
    index = wSpielwindow.comboBox_A3.findText("20")
    wSpielwindow.comboBox_A3.setCurrentIndex(index)

    wSpielwindow.horizontalSlider_Renten.setValue(70)
    AnteilImSliderRenten()

    # Slider für Produkte:
    # Renten:
    wSpielwindow.horizontalSlider_ProduktRenteZumMarkt.setMinimum(0)
    wSpielwindow.horizontalSlider_ProduktRenteZumMarkt.setMaximum(200)
    wSpielwindow.horizontalSlider_ProduktRenteZumMarkt.setValue(100)
 
    # BU:
    wSpielwindow.horizontalSlider_ProduktBuZumMarkt.setMinimum(0)
    wSpielwindow.horizontalSlider_ProduktBuZumMarkt.setMaximum(200)
    wSpielwindow.horizontalSlider_ProduktBuZumMarkt.setValue(100)    # Slider für Produkte:
    
    #Slider für Provision:    
    # Renten:
    wSpielwindow.horizontalSlider_ProvisionRenteZumMarkt.setMinimum(0)
    wSpielwindow.horizontalSlider_ProvisionRenteZumMarkt.setMaximum(200)
    wSpielwindow.horizontalSlider_ProvisionRenteZumMarkt.setValue(100)
 
    # BU:
    wSpielwindow.horizontalSlider_ProvisionBuZumMarkt.setMinimum(0)
    wSpielwindow.horizontalSlider_ProvisionBuZumMarkt.setMaximum(200)
    wSpielwindow.horizontalSlider_ProvisionBuZumMarkt.setValue(100)

    #Slider für Laufzeit:    
    # Rente:
    wSpielwindow.horizontalSlider_LaufzeitRente.setMinimum(1)
    wSpielwindow.horizontalSlider_LaufzeitRente.setMaximum(35)
    wSpielwindow.horizontalSlider_LaufzeitRente.setValue(5)
    # Bu:
    wSpielwindow.horizontalSlider_LaufzeitBu.setMinimum(1)
    wSpielwindow.horizontalSlider_LaufzeitBu.setMaximum(35)
    wSpielwindow.horizontalSlider_LaufzeitBu.setValue(10)
    
    wSpielwindow.pushButton_GrundeinstellungWindow.setIcon(gui.QIcon(files_dict.get('file_icon_grundeinstellungwindow')))
    wSpielwindow.pushButton_GrundeinstellungWindow.setIconSize(core.QSize(41, 41))

    wSpielwindow.pushButton_statistik.setIcon(gui.QIcon(files_dict.get('file_icon_statistikwindow')))
    wSpielwindow.pushButton_statistik.setIconSize(core.QSize(100, 100))

    wSpielwindow.pushButton_GuvWindow.setIcon(gui.QIcon(files_dict.get('file_icon_guvwindow')))
    wSpielwindow.pushButton_GuvWindow.setIconSize(core.QSize(100, 100))


def ZeigeGuVTabelleAn():
    
    tabelle = wSpielwindow.tableWidget_GuV
    ozD = zD.ZeigeDatnInTabelle(tabelle)
    file_daten = files_dict.get('file_bilanz')
    ozD.SchreibeDatenIntabelle(file_daten)


def ZeigeStatistikTabelleAn():
    #Hier wird die Statistik CSV angezeigt
    tabelle = wSpielwindow.tableWidget_StatistikCSV
    ozD = zD.ZeigeDatnInTabelle(tabelle)
    file_daten = files_dict.get('file_system_statistik')
    ozD.SchreibeDatenIntabelle(file_daten)


def ZeigeKostenModellTabelleAn():
    #Hier wird die Kosten-Optionentabelle angezeigt
    tabelle = wSpielwindow.tableWidget_Kostenmodell
    ozD = zD.ZeigeDatnInTabelle(tabelle)
    file_daten = files_dict.get('optionen_file_kosten')
    ozD.SchreibeDatenIntabelle(file_daten)


def LegeLaufzeitAuswahlBeiRentenFestInKa():
    
    for i in range(1,21):
        wSpielwindow.comboBox_L1.insertItem(i, str(i))
        wSpielwindow.comboBox_L2.insertItem(i, str(i))
        wSpielwindow.comboBox_L3.insertItem(i, str(i))
    
    for i in range(25, 51, 5):
        wSpielwindow.comboBox_L1.insertItem(i, str(i))
        wSpielwindow.comboBox_L2.insertItem(i, str(i))
        wSpielwindow.comboBox_L3.insertItem(i, str(i))
        
    for i in range(0, 101, 10):
        wSpielwindow.comboBox_A1.insertItem(i, str(i))        
        wSpielwindow.comboBox_A2.insertItem(i, str(i))        
        wSpielwindow.comboBox_A3.insertItem(i, str(i)) 


'''
def LegeBilanzTabelleAn(obil):
    # hier werden die Ergebnisse der Bilanz in eine Tabelle im Dialog ausgegeben:
    jahr_beginn = files_dict.get('Startjahr_Simulation')
    jahr_aktuell = files_dict.get('jahr_aktuell')

    anzahl_jahre = int(jahr_aktuell)-int(jahr_beginn)

    wSpielwindow.tableWidget_Bilanz.setColumnCount(anzahl_jahre+1)
    wSpielwindow.tableWidget_Bilanz.setRowCount(1)

    vektor_jahre = []
    for i in range(0, anzahl_jahre+1):
        jahr = str(jahr_beginn+i-1)
        vektor_jahre.append(jahr)

    wSpielwindow.tableWidget_Bilanz.setHorizontalHeaderLabels(vektor_jahre)

    vektor_namen = []
    index_row = 0
    namen = {}

    key_bilanz = {}
    key_bilanz['rl'] = 'Bilanz'
    key_bilanz['avbg'] = '999'

    name = 'eigenkapital_ende'
    key_bilanz['name'] = name
    namen[name] = 'Eigenkapital'
    index_row += 1
    wSpielwindow.tableWidget_Bilanz.setRowCount(index_row)
    vektor_namen.append(namen.get(name))
    for i in range(0, anzahl_jahre+1):
        jahr = str(jahr_beginn+i-1)
        key_bilanz['jahr'] = jahr
        wert = obil.LeseBilanzCSV(key_bilanz)
        wSpielwindow.tableWidget_Bilanz.setItem(
            index_row-1, i, widgets.QTableWidgetItem(str(wert)))

    name = 'bil_derue7_ende'
    key_bilanz['name'] = name
    namen[name] = 'Bilanz Deckungsrückstellung auf Risiko VU'
    index_row += 1
    wSpielwindow.tableWidget_Bilanz.setRowCount(index_row)
    vektor_namen.append(namen.get(name))
    for i in range(0, anzahl_jahre+1):
        jahr = str(jahr_beginn+i-1)
        key_bilanz['jahr'] = jahr
        wert = obil.LeseBilanzCSV(key_bilanz)
        wSpielwindow.tableWidget_Bilanz.setItem(
            index_row-1, i, widgets.QTableWidgetItem(str(wert)))

    wSpielwindow.tableWidget_Bilanz.setVerticalHeaderLabels(vektor_namen)
'''

def LeseAusSpielfensterKA():
    # es werden aus dem Dialog die Eingaben zu Kapitalanlagen ausgelesen:

    # Jahr der Simulation:
    ka_sa_dict['jahr'] = wSpielwindow.label_Jahr.text()

    # laufzeiten der Renten:
    l1 = int(wSpielwindow.comboBox_L1.currentText())
    l2 = int(wSpielwindow.comboBox_L2.currentText())
    l3 = int(wSpielwindow.comboBox_L3.currentText())

    ka_renten_sa_dict['laufzeit'] = [l1, l2, l3]
    ka_renten_sa_dict['anzahl'] = 3

    # Anteile der Renten:
    a1 = float(wSpielwindow.comboBox_A1.currentText())/100
    a2 = float(wSpielwindow.comboBox_A2.currentText())/100
    a3 = float(wSpielwindow.comboBox_A3.currentText())/100

    ka_renten_sa_dict['aufteilung'] = [a1, a2, a3]

    # Aufteilung auf Renten und Aktien:
    anteil_renten = float(wSpielwindow.label_Anteil_Renten.text())/100
    anteil_aktien = float(wSpielwindow.label_Anteil_Aktien.text())/100

    ka_sa_dict['anteil_renten'] = anteil_renten
    ka_sa_dict['anteil_aktien'] = anteil_aktien

    ka_sa_dict['vola_aktien'] = 0.1

    # das gesamtem Dict zu Renten wird in das Dict zu KA reingeschrieben:
    ka_sa_dict['renten'] = ka_renten_sa_dict
    t = 'Aus dem Dialog zu Kapitalanlagen wurden für Renten ausgelesen:' + \
        str(ka_renten_sa_dict)
    oprot.SchreibeInProtokoll(t)


def SchreibeMessage(text):
    msg = widgets.QMessageBox()
    msg.setIcon(widgets.QMessageBox.Warning)
    msg.setText(text)
    msg.setWindowTitle('Info')

    msg.exec()


def ZeigeGrafik(file):
    w = uic.loadUi(files_dict.get('leereswindow_file'))
    pixmap = gui.QPixmap(file)
    w.label_Grafik.setPixmap(pixmap)
    w.label_Grafik.setScaledContents(True)
    w.exec_()


def ZeigeGrafik_ZSK():
    file = files_dict.get('file_grafik_zsk')
    ZeigeGrafik(file)


def ZeigeGrafik_Entwicklung_Renten():
    file = files_dict.get('grafik_file_entwicklung_renten')
    ZeigeGrafik(file)


def ZeigeWindowGuv():
    oguvW = guvW.GuVWindow(files_dict)
    oguvW.RufeFensterAuf()


def ZeigeWindowBilanz():
    oWindow = bilanzWindow.BilanzWindow(files_dict)
    oWindow.RufeFensterAuf()


def ZeigeWindowStatistik():
    osW = sW.StatistikWindow(files_dict)
    osW.RufeFensterAuf()


def ZeigeWindowProdukt():
    opW = pW.ProduktWindow(files_dict)
    opW.RufeFensterAuf()
    

def ZeigeWindowVertrag():
    ovW = vW.VertragsWindow(files_dict)
    ovW.RufeFensterAuf()


def ZeigeWindowVertraegeAusFortschreibung():
    objekt = vertraegeausfortschreibungwindow.VertraegeAusFortschreibungWindow(files_dict)
    jahr = int(files_dict.get('jahr_aktuell'))
    objekt.RufeFensterAuf(jahr)


def LeseAusFensterSpielVertriebEingaben():
    # hier werden die Eingaben zum Thema Neugeschäft aus dem Dialog Spiel ausgelesen:

    # Jahr der Simulation:
    vertrieb_dict['jahr'] = wSpielwindow.label_Jahr.text()

    #Beitrag im Vergleich zum Markt:
    beitrag_RentenZumMarkt = int(wSpielwindow.label_BeitragRenteZumMarkt.text())
    vertrieb_dict['beitrag_RentenZumMarkt']=beitrag_RentenZumMarkt

    beitrag_BuZumMarkt = int(wSpielwindow.label_BeitragBuZumMarkt.text())
    vertrieb_dict['beitrag_BuZumMarkt']=beitrag_BuZumMarkt
    
    #Provision im Vergleich zum Markt:
    #Rente:
    provision = int(wSpielwindow.label_ProvisionRenteZumMarkt.text())
    vertrieb_dict['provision_RentenZumMarkt'] = provision
    #BU:
    provision = int(wSpielwindow.label_ProvisionBuZumMarkt.text())
    vertrieb_dict['provision_BuZumMarkt'] = provision     
    
    #Laufzeit der Verträge:
    #Rente:
    laufzeit = int(wSpielwindow.label_LaufzeitRente.text())   
    vertrieb_dict['laufzeitRente'] = laufzeit     
    #Bu:
    laufzeit = int(wSpielwindow.label_LaufzeitBu.text())   
    vertrieb_dict['laufzeitBu'] = laufzeit     
        
    #Neugeschäft oder Runoff:
    #Renten:
    if wSpielwindow.radioButton_Rente_Neugeschaeft.isChecked() == True:
        vertrieb_dict['neugeschaeft_Rente'] = True
    else:
        vertrieb_dict['neugeschaeft_Rente'] = False

    #Bu:
    if wSpielwindow.radioButton_Bu_Neugeschaeft.isChecked() == True:
        vertrieb_dict['neugeschaeft_Bu'] = True
    else:
        vertrieb_dict['neugeschaeft_Bu'] = False
        
    text = 'Aus dem Dialog zum Vertrieb wurden für folgende Eingaben ausgelesen:' + \
        str(vertrieb_dict)
    oprot.SchreibeInProtokoll(text)


def LeseAusFensterSpielAlleEingaben():
    # Das Dialog Spielfenster wird ausgelesen:

    ka_renten_sa_dict['jahr'] = wSpielwindow.label_Jahr.text()

    # lese Eingaben zu Kapitalanlagen:
    LeseAusSpielfensterKA()

    # lese Eingaben zum Neugeschäft:
    LeseAusFensterSpielVertriebEingaben()


def AnteilImSliderRenten():
    wert_renten = wSpielwindow.horizontalSlider_Renten.value()
    wert_aktien = 100 - int(wert_renten)
    wSpielwindow.horizontalSlider_Aktien.setValue(wert_aktien)
    wSpielwindow.label_Anteil_Renten.setText(str(wert_renten))
    wSpielwindow.label_Anteil_Aktien.setText(str(wert_aktien))
    

def BeitragProdukteRentenZumMarktmSlider():
    beitrag = wSpielwindow.horizontalSlider_ProduktRenteZumMarkt.value()
    wSpielwindow.label_BeitragRenteZumMarkt.setText(str(beitrag))


def BeitragProdukteBuZumMarktmSlider():
    beitrag = wSpielwindow.horizontalSlider_ProduktBuZumMarkt.value()
    wSpielwindow.label_BeitragBuZumMarkt.setText(str(beitrag))


def ProvisionRenteZumMarktmSlider():
    beitrag = wSpielwindow.horizontalSlider_ProvisionRenteZumMarkt.value()
    wSpielwindow.label_ProvisionRenteZumMarkt.setText(str(beitrag))


def ProvisionBuZumMarktmSlider():
    beitrag = wSpielwindow.horizontalSlider_ProvisionBuZumMarkt.value()
    wSpielwindow.label_ProvisionBuZumMarkt.setText(str(beitrag))


def LaufzeitRenteSlider():
    laufzeit = wSpielwindow.horizontalSlider_LaufzeitRente.value()
    wSpielwindow.label_LaufzeitRente.setText(str(laufzeit))


def LaufzeitBuSlider():
    laufzeit = wSpielwindow.horizontalSlider_LaufzeitBu.value()
    wSpielwindow.label_LaufzeitBu.setText(str(laufzeit))


def KontrolleAnteilRentenInKa():
    anteil1 = wSpielwindow.comboBox_A1.currentText()
    anteil2 = wSpielwindow.comboBox_A2.currentText()
    anteil3 = wSpielwindow.comboBox_A3.currentText()

    summe = int(anteil1)+int(anteil2)+int(anteil3)

    if summe == 100:
        ergebnis = True
    else:
        text = 'Fehler: Summe = '+str(summe)+'. Es sollten aber 100 sein!'
        SchreibeMessage(text)
        ergebnis = False

    return ergebnis


def Kontrollen():

    if KontrolleAnteilRentenInKa() == False:
        text = 'KontrolleAnteilRenten: Fehler in der Aufteilung der Renten'
        oprot.SchreibeInProtokoll(text)
        return False

    return True


def Steuerung():

    overtrieb = ver.Vertrieb(files_dict)
    oprot.SchreibeInProtokoll('Vertrieb wurde angelegt')

    oantrag = antrag.Antrag(files_dict)
    oprot.SchreibeInProtokoll('Anträge wurden angelegt')

    file_vertrieb = overtrieb.file_vertrieb
    oantrag.LegeVerriebstabelleFest(file_vertrieb)

    #oantrag_oe = oe_antrag.OE_Antarg(files_dict)

    osys = system.System(files_dict)

    file_system_antrag = oantrag.file_system_antrag
    osys.LegeAntragstabelleFest(file_system_antrag)

    obil = bil.Bilanz(files_dict)
    oprot.SchreibeInProtokoll('Bilanz wurde angelegt')
    obil.Init_Bilanz(jahr_beginn)

    oprovision = provision.Provision(files_dict)
    oprovision.BereiteProvisionVor()
    
    okap = kap.Kapitalanlagen(files_dict)
    oprot.SchreibeInProtokoll('Kapitalanlagen wurden angelegt')

    okap.Init_KA(jahr_beginn)

    jahr = int(jahr_beginn)
    files_dict['jahr_aktuell'] = jahr

    ka_sa_dict.clear()
    #LeseAusFensterMainAlleEingaben()

    wSpielwindow.label_Jahr.setText(str(jahr))

    # die Tabelle im Dialog mit Ergebnissen der Bilanz wird angelegt:
    #LegeBilanzTabelleAn(obil)

    # die Tabelle im Dialog mit Ergebnissen der GuV wird angelegt:
    ZeigeGuVTabelleAn()

    # die Tabelle mit Kostenmodell wird angezeigtt:
    ZeigeKostenModellTabelleAn()
    
    okosten = kosten.Kosten(files_dict)
    okosten.LegeFileKosten()
    
    # Nachreservierung:
    onachres = nachreservierung.Nachreservierung(files_dict)
    onachres.LegeFileNachreservierung()
    
    wSpielwindow.tabWidget_2.setCurrentIndex(0)

    # solange im Spielwindow okay geclickt wird, dann wird ein Jahr weiter gespielt:
    while wSpielwindow.exec_() == widgets.QDialog.Accepted:

        files_dict['jahr_aktuell'] = jahr

        if Kontrollen() == False:
            continue

        # es werden alle Eingaben aus dem Dialog ausgelesen:
        LeseAusFensterSpielAlleEingaben()

        von = str(jahr)+'01'+'01'
        bis = str(jahr)+'12'+'31'

        LeseAusFensterSpielAlleEingaben()

        okap.Init_SA(ka_sa_dict)

        obil.ErstelleBilanzAnfang(jahr)  # die Endwerte des Vorjahres werden auf den Anfanf des aktuellen GJ fortgetragen

        overtrieb.SchreibeNeugeschaeft(vertrieb_dict)

        okap.Beginn(jahr)
        okap.Fortschreibung(jahr)

        onachres.StelleNachreservierungFest(jahr) #hier wird eine potentielle Nachreservierung festgelegt
        
        osys.Fortschreibung(von, bis)

        oantrag.LeseVertrieb(jahr)

        osys.Policiere(jahr)
        osys.ErstelleStatistik(von, bis)
        
        oprovision.BerechneAP(jahr) #hier wird die AP für die policiereten Verträge berechnet

        okosten.ErmittleKosten(jahr) #hier werden die Kosten ermittelt

        okap.ErmittleStandKasseAmEnde(jahr)  # hier wird der Stand in der Kasse am Jahresende ermittelt
        okap.KonsolidiereDieKapitalanlageEnde(jahr)  # hier werden die End-Werte der Kapitalanlage der Aktien und Renten konsoliediert
        
        obil.ErstelleBilanzEnde(jahr)

        okap.ZeichneKapitalanlagen(jahr)

        jahr += 1
        files_dict['jahr_aktuell'] = jahr
        #LegeBilanzTabelleAn(obil)  # Ergebnisse der Bilanz
        
        ZeigeGuVTabelleAn()  # Ergebnisse der GuV
        ZeigeStatistikTabelleAn() #Hier wird die Statistiktabelle angezeigt
        ZeigeKostenModellTabelleAn() # die Tabelle mit KOstenmodell wird angezeigtt:

        wSpielwindow.label_Jahr.setText(str(jahr))

        file_grafik = files_dict.get('grafik_file_entwicklung_renten')
        icon = gui.QIcon(file_grafik)
        wSpielwindow.pushButton_Entwicklung_Renten.setIcon(icon)
        hoehe = LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_Entwicklung_Renten).get('hoehe')-10
        breite = LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_Entwicklung_Renten).get('breite')-10
        wSpielwindow.pushButton_Entwicklung_Renten.setIconSize(core.QSize(breite, hoehe))

        file_grafik = files_dict.get('file_grafik_zsk')
        icon = gui.QIcon(file_grafik)
        wSpielwindow.pushButton_ZSK.setIcon(icon)
        hoehe = LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_ZSK).get('hoehe')-10
        breite = LeseGroesseEinesButtonsAus(wSpielwindow.pushButton_ZSK).get('breite')-10
        wSpielwindow.pushButton_ZSK.setIconSize(core.QSize(breite, hoehe))

        #Der Focus der Tabs muss wieder ausgerichtet werden:
        wSpielwindow.tabWidget_2.setCurrentIndex(0)
        wSpielwindow.tabWidget_Ergebnisse.setCurrentIndex(0)


    oprot.SchreibeInProtokoll("ENDE erreicht!!!")
    print("**** Ende ****")

def RufeGrundeinstellungAuf():
    ogw = gW.GrundEinstelleungWindow(files_dict)
    ogw.RufeFensterAuf()


if __name__ == "__main__":
    app = widgets.QApplication(sys.argv)
    
    RufeGrundeinstellungAuf()

    wSpielwindow = uic.loadUi(files_dict.get('spielwindow_file'))
    
    wSpielwindow.pushButton_ZSK.clicked.connect(ZeigeGrafik_ZSK)
    wSpielwindow.pushButton_statistik.clicked.connect(ZeigeWindowStatistik)
    wSpielwindow.pushButton_produkt.clicked.connect(ZeigeWindowProdukt)
    wSpielwindow.pushButton_vertrag.clicked.connect(ZeigeWindowVertrag)
    wSpielwindow.pushButton_GrundeinstellungWindow.clicked.connect(RufeGrundeinstellungAuf)
    wSpielwindow.pushButton_GuvWindow.clicked.connect(ZeigeWindowGuv)
    wSpielwindow.pushButton_bilanzErgebnisse.clicked.connect(ZeigeWindowBilanz)
    wSpielwindow.pushButton_vertraegeAusFortschreibung.clicked.connect(ZeigeWindowVertraegeAusFortschreibung)
    
    wSpielwindow.pushButton_Entwicklung_Renten.clicked.connect(ZeigeGrafik_Entwicklung_Renten)
    wSpielwindow.horizontalSlider_Renten.valueChanged.connect(AnteilImSliderRenten)
    
    wSpielwindow.horizontalSlider_ProduktRenteZumMarkt.valueChanged.connect(BeitragProdukteRentenZumMarktmSlider)
    wSpielwindow.horizontalSlider_ProduktBuZumMarkt.valueChanged.connect(BeitragProdukteBuZumMarktmSlider)
    wSpielwindow.horizontalSlider_ProvisionBuZumMarkt.valueChanged.connect(ProvisionBuZumMarktmSlider)
    wSpielwindow.horizontalSlider_ProvisionRenteZumMarkt.valueChanged.connect(ProvisionRenteZumMarktmSlider)
    wSpielwindow.horizontalSlider_LaufzeitRente.valueChanged.connect(LaufzeitRenteSlider)
    wSpielwindow.horizontalSlider_LaufzeitBu.valueChanged.connect(LaufzeitBuSlider)
    
    LegeLaufzeitAuswahlBeiRentenFestInKa()
    
    LegeDefoultEinstellungenfest()
    
    oopt = opt.Optionen(files_dict.get('optionen_file_main'))
    
    oprot = prot.Protokoll(files_dict.get('protokoll_file_main'))
    
    Steuerung()
    
    app.exec_()
