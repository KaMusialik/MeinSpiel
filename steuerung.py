# -*- coding: utf-8 -*-

import sys
import PyQt5.QtCore as core
import PyQt5.QtWidgets as widgets
import PyQt5.QtGui as gui
import PyQt5.uic as uic


import optionen as opt
import protokoll as prot

import grundeinstellungwindow as gW
import bilanz as bil
import vertrieb as ver
#import oe_antrag as oe_antrag
import antrag as antrag
import system
import kapitalanlagen as kap


files_dict = {}
# work directory:
files_dict['work_dir'] = '/home/karol_laptop/MeineProjekte/MeinSpiel/csv_fuer_mein_Spiel/'

# einzelne Dateien:
files_dict['grundeinstellungwindow_file'] = files_dict.get('work_dir')+'grundeinstellungwindow.ui'
files_dict['spielwindow_file'] = files_dict.get('work_dir')+'spielwindow.ui'
files_dict['leereswindow_file'] = files_dict.get('work_dir')+'leereswindow.ui'

files_dict['file_grafik_zsk'] = files_dict.get('work_dir')+'grafik_zsk.png'
files_dict['grafik_file_entwicklung_renten'] = files_dict.get(
    'work_dir')+'grafik_renten.png'

files_dict['optionen_file_grundeinstellungwindow'] = files_dict.get(
    'work_dir')+'optionen_grundeinstellungwindow.csv'
files_dict['protokoll_file_grundeinstellungwindow'] = files_dict.get(
    'work_dir')+'protokoll_grundeinstellungwindow.txt'

files_dict['optionen_file_main'] = files_dict.get(
    'work_dir')+'optionen_main.csv'
files_dict['protokoll_file_main'] = files_dict.get(
    'work_dir')+'protokoll_main.txt'

files_dict['optionen_file_vertrieb'] = files_dict.get(
    'work_dir')+'optionen_vertrieb.csv'
files_dict['protokoll_file_vertrieb'] = files_dict.get(
    'work_dir')+'protokoll_vertrieb.txt'
files_dict['file_vertrieb'] = files_dict.get('work_dir')+'vertrieb.csv'

# Dateien zu Thema Antrag:
files_dict['optionen_file_antrag'] = files_dict.get(
    'work_dir')+'optionen_antrag.csv'
files_dict['file_system_antrag'] = files_dict.get(
    'work_dir')+'system_antrag.csv'
files_dict['protokoll_file_antrag'] = files_dict.get(
    'work_dir')+'protokoll_antrag.txt'

files_dict['optionen_file_antrag_oe'] = files_dict.get(
    'work_dir')+'optionen_antrag_oe.csv'
files_dict['protokoll_file_antrag_oe'] = files_dict.get(
    'work_dir')+'protokoll_antrag_oe.txt'

files_dict['protokoll_file_bilanz'] = files_dict.get(
    'work_dir')+'protokoll_bilanz.txt'
files_dict['file_bilanz'] = files_dict.get('work_dir')+'bilanz.csv'
files_dict['file_bilanz_start'] = files_dict.get('work_dir')+'bilanz_start.csv'
files_dict['file_bilanz_struktur'] = {
    'jahr': int, 'rgl': str, 'avbg': str, 'name': str, 'wert': str}

files_dict['protokoll_file_system'] = files_dict.get(
    'work_dir')+'protokoll_system.txt'
files_dict['file_system_fortschreibung_struktur'] = {
    'vsnr': str, 'histnr': int, 'von': int, 'bis': int, 'name': str, 'wert': str}
files_dict['file_system_bestand_struktur'] = {
    'vsnr': str, 'histnr': int, 'von': int, 'bis': int, 'name': str, 'wert': str}
files_dict['file_system_fortschreibung'] = files_dict.get(
    'work_dir')+'system_fortschreibung.csv'
files_dict['grafik_file_statistik_anzahl'] = files_dict.get(
    'work_dir')+'grafik_statistik_anzahl.png'

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


def LegeGuVTabelleAn(obil):
    # Im Dialog werden die Ergebnisse der GuV ausgegeben:
    jahr_beginn = files_dict.get('Startjahr_Simulation')
    jahr_aktuell = files_dict.get('jahr_aktuell')

    anzahl_jahre = int(jahr_aktuell)-int(jahr_beginn)

    wSpielwindow.tableWidget_GuV.setColumnCount(anzahl_jahre+1)
    wSpielwindow.tableWidget_GuV.setRowCount(1)

    vektor_jahre = []
    for i in range(0, anzahl_jahre+1):
        jahr = str(jahr_beginn+i-1)
        vektor_jahre.append(jahr)

    wSpielwindow.tableWidget_GuV.setHorizontalHeaderLabels(vektor_jahre)

    vektor_namen = []
    index_row = 0
    namen = {}

    key_bilanz = {}
    key_bilanz['rl'] = 'guv'
    key_bilanz['avbg'] = '999'

    name = 'bil_gebuchter_beitrag'
    key_bilanz['name'] = name
    namen[name] = 'Gebuchter Beitrag'
    index_row += 1
    wSpielwindow.tableWidget_GuV.setRowCount(index_row)
    vektor_namen.append(namen.get(name))
    for i in range(0, anzahl_jahre+1):
        jahr = str(jahr_beginn+i)
        key_bilanz['jahr'] = jahr
        wert = obil.LeseBilanzCSV(key_bilanz)
        wSpielwindow.tableWidget_GuV.setItem(
            index_row-1, i+1, widgets.QTableWidgetItem(str(wert)))

    # Zeilenüberschriften:
    wSpielwindow.tableWidget_GuV.setVerticalHeaderLabels(vektor_namen)

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


def ZeigeGrafik_Statistik_Anzahl():
    file = files_dict.get('grafik_file_statistik_anzahl')
    ZeigeGrafik(file)

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

    okap = kap.Kapitalanlagen(files_dict)
    oprot.SchreibeInProtokoll('Kapitalanlagen wurden angelegt')

    okap.Init_KA(jahr_beginn)

    jahr = int(jahr_beginn)
    files_dict['jahr_aktuell'] = jahr

    ka_sa_dict.clear()
    #LeseAusFensterMainAlleEingaben()

    wSpielwindow.label_Jahr.setText(str(jahr))

    # die Tabelle im Dialog mit Ergebnissen der Bilanz wird angelegt:
    LegeBilanzTabelleAn(obil)

    # die Tabelle im Dialog mit Ergebnissen der GuV wird angelegt:
    LegeGuVTabelleAn(obil)

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

        obil.ErstelleBilanzAnfang(jahr)

        overtrieb.SchreibeNeugeschaeft(vertrieb_dict)

        okap.Beginn(jahr)
        okap.Fortschreibung(jahr)

        osys.Fortschreibung(von, bis)

        oantrag.LeseVertrieb(jahr)

        osys.Policiere(jahr)
        osys.ErstelleStatistik(von, bis)

        obil.ErstelleBilanzEnde(jahr)

        okap.ZeichneKapitalanlagen(jahr)

        jahr += 1
        files_dict['jahr_aktuell'] = jahr
        LegeBilanzTabelleAn(obil)  # Ergebnisse der Bilanz
        LegeGuVTabelleAn(obil)  # Ergebnisse der GuV

        wSpielwindow.label_Jahr.setText(str(jahr))

        file_grafik = files_dict.get('grafik_file_entwicklung_renten')
        icon = gui.QIcon(file_grafik)
        wSpielwindow.pushButton_Entwicklung_Renten.setIcon(icon)
        hoehe = LeseGroesseEinesButtonsAus(
            wSpielwindow.pushButton_Entwicklung_Renten).get('hoehe')-10
        breite = LeseGroesseEinesButtonsAus(
            wSpielwindow.pushButton_Entwicklung_Renten).get('breite')-10
        wSpielwindow.pushButton_Entwicklung_Renten.setIconSize(
            core.QSize(breite, hoehe))

        file_grafik = files_dict.get('file_grafik_zsk')
        icon = gui.QIcon(file_grafik)
        wSpielwindow.pushButton_ZSK.setIcon(icon)
        hoehe = LeseGroesseEinesButtonsAus(
            wSpielwindow.pushButton_ZSK).get('hoehe')-10
        breite = LeseGroesseEinesButtonsAus(
            wSpielwindow.pushButton_ZSK).get('breite')-10
        wSpielwindow.pushButton_ZSK.setIconSize(core.QSize(breite, hoehe))

        file_grafik = files_dict.get('grafik_file_statistik_anzahl')
        icon = gui.QIcon(file_grafik)
        wSpielwindow.pushButton_statistik_anzahl.setIcon(icon)
        hoehe = LeseGroesseEinesButtonsAus(
            wSpielwindow.pushButton_statistik_anzahl).get('hoehe')-10
        breite = LeseGroesseEinesButtonsAus(
            wSpielwindow.pushButton_statistik_anzahl).get('breite')-10
        wSpielwindow.pushButton_statistik_anzahl.setIconSize(
            core.QSize(breite, hoehe))

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
    wSpielwindow.pushButton_statistik_anzahl.clicked.connect(
        ZeigeGrafik_Statistik_Anzahl)
    wSpielwindow.pushButton_Entwicklung_Renten.clicked.connect(
        ZeigeGrafik_Entwicklung_Renten)
    wSpielwindow.horizontalSlider_Renten.valueChanged.connect(AnteilImSliderRenten)
    
    wSpielwindow.horizontalSlider_ProduktRenteZumMarkt.valueChanged.connect(BeitragProdukteRentenZumMarktmSlider)
    wSpielwindow.horizontalSlider_ProduktBuZumMarkt.valueChanged.connect(BeitragProdukteBuZumMarktmSlider)
    wSpielwindow.horizontalSlider_ProvisionBuZumMarkt.valueChanged.connect(ProvisionBuZumMarktmSlider)
    wSpielwindow.horizontalSlider_ProvisionRenteZumMarkt.valueChanged.connect(ProvisionRenteZumMarktmSlider)
    
    LegeLaufzeitAuswahlBeiRentenFestInKa()
    
    LegeDefoultEinstellungenfest()
    
    oopt = opt.Optionen(files_dict.get('optionen_file_main'))
    
    oprot = prot.Protokoll(files_dict.get('protokoll_file_main'))
    
    Steuerung()
    
    app.exec_()
