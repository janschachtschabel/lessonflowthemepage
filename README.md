# lessonflowthemepage
Dieses Python-Skript erstellt automatisch strukturierte Unterrichtsabläufe basierend auf Angaben einer Themenseite.

# Funktionsweise
Das Skript arbeitet in zwei Hauptschritten:

Generierung des Unterrichtsablaufs: Anhand von Eingaben wie Thema, Bildungsstufe und Fachgebiet wird ein detaillierter Unterrichtsplan mit Titel, Beschreibung und Phasen erstellt.

Erstellung von Metadatenfiltern: Für jede Phase des Unterrichtsablaufs werden spezifische Metadatenfilter generiert, um passende Inhalte zuzuordnen.

# Eingabeparameter
Breadcrumb: Hierarchische Themenstruktur (z.B. "Physik > Optik > Menschliches Auge")

Beschreibung: Detaillierte Beschreibung des Themas

Bildungsstufe: Zielgruppe (z.B. "Sekundarstufe II")

Fach: Fachgebiet (z.B. "Physik")

Sprache: Unterrichtssprache (z.B. "Deutsch")


# Ausgabe
Das Skript liefert einen JSON-formatierten Unterrichtsablauf mit folgenden Informationen:

Titel: Titel des Unterrichtsablaufs

Beschreibung: Kurzbeschreibung des Ablaufs

Unterrichtsphasen: Liste der Phasen mit Titeln und Kurzbeschreibungen

Anzahl_phasen: Gesamtzahl der Phasen

# Voraussetzungen
Python 3.x

Installierte Abhängigkeiten (siehe requirements.txt)

# Installation
Klonen Sie das Repository:

bash
Code kopieren

git clone https://github.com/janschachtschabel/lessonflowthemepage.git

Wechseln Sie ins Projektverzeichnis:

bash
Code kopieren

cd lessonflowthemepage

Installieren Sie die erforderlichen Pakete:

bash
Code kopieren

pip install -r requirements.txt

# Nutzung
Führen Sie das Skript mit den gewünschten Eingabeparametern aus:

bash
Code kopieren
python lessonflowthemepage.py

# Lizenz
Dieses Projekt steht unter der Apache 2 Lizenz.

# Kontakt
Bei Fragen oder Anregungen wenden Sie sich bitte an mich.
