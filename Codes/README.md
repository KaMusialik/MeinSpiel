Hier werden die Codes *.py zu meine Spiel abgelegt. Es sind viele ...
Es muss parall ein Verzeichnis mit den Daten zum Spiel und Fenster.ui geben. Dies wird in der steuerung.py als Workdir oben eingetragen.

z.B.: files_dict['work_dir'] = '/home/karol/Projekte/csv_fuer_mein_Spiel/'

Wenn das Spiel auf einen neuen Rechner installiert wird, müssen folgende Schritte durchgeführt werden:
- installiere mini Conda
- installiere zusätzliche packeges:
  - conda install pyqt pandas pypdf2 matplotlib
- hole vom Github die zip-datei und extrahiere sie auf dem Rechner:
  - es werden zwei Verzeichnisse extrahiert: Codes und Dateien
- öffne die Datei steuerung.py. Dort muss man ggf. das Word-Dir ausrichten/eintragen:
  - files_dict['work_dir'] = '/home/karol/Projekte/MeinSpiel/Dateien/'
  
In dem Projekt befindet sich mySpiel.bat. Diese Batch-Datei müsste ggf. auch angepasst werden, falls eine Verknüpfung sie ausfruft 