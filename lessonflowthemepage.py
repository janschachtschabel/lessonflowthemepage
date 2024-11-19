import os
import json
import re
from openai import OpenAI, OpenAIError
from pydantic import BaseModel, ValidationError
from enum import Enum
from typing import List

# OpenAI-Client mit API-Key aus Umgebungsvariablen einrichten
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Deutsche Enums für Bildungsstufe, Fach und Inhaltstyp
class Bildungsstufe(str, Enum):
    ELEMENTARBEREICH = "Elementarbereich"
    PRIMARSTUFE = "Primarstufe"
    SEKUNDARSTUFE_I = "Sekundarstufe I"
    SEKUNDARSTUFE_II = "Sekundarstufe II"
    SEKUNDARSTUFE = "Sekundarstufe"
    HOCHSCHULE = "Hochschule"
    BERUFLICHE_BILDUNG = "Berufliche Bildung"
    FORTBILDUNG = "Fortbildung"
    ERWACHSENENBILDUNG = "Erwachsenenbildung"
    FOERDERSCHULE = "Förderschule"
    FERNUNTERRICHT = "Fernunterricht"

class Fach(str, Enum):
    ALLGEMEIN = "Allgemein"
    ALT_GRIECHISCH = "Alt-Griechisch"
    AGRARWIRTSCHAFT = "Agrarwirtschaft"
    ARBEIT_ERNAEHRUNG_SOZIALES = "Arbeit, Ernährung, Soziales"
    ARBEITSLEHRE = "Arbeitslehre"
    ARBEITSSICHERHEIT = "Arbeitssicherheit"
    ASTRONOMIE = "Astronomie"
    BAUTECHNIK = "Bautechnik"
    BERUFLICHE_BILDUNG = "Berufliche Bildung"
    BIOLOGIE = "Biologie"
    CHEMIE = "Chemie"
    CHINESISCH = "Chinesisch"
    DARSTELLENDES_SPIEL = "Darstellendes Spiel"
    DEUTSCH = "Deutsch"
    DEUTSCH_ALS_ZWEITSPRACHE = "Deutsch als Zweitsprache"
    ELEKTROTECHNIK = "Elektrotechnik"
    ERNAEHRUNG_UND_HAUSWIRTSCHAFT = "Ernährung und Hauswirtschaft"
    ENGLISCH = "Englisch"
    PAEDAGOGIK = "Pädagogik"
    ESPERANTO = "Esperanto"
    ETHIK = "Ethik"
    FARBTECHNIK_UND_RAUMGESTALTUNG = "Farbtechnik und Raumgestaltung"
    FRANZOESISCH = "Französisch"
    GEOGRAFIE = "Geografie"
    GESCHICHTE = "Geschichte"
    GESELLSCHAFTSKUNDE = "Gesellschaftskunde"
    GESUNDHEIT = "Gesundheit"
    HAUSWIRTSCHAFT = "Hauswirtschaft"
    HOLZTECHNIK = "Holztechnik"
    INFORMATIK = "Informatik"
    INTERKULTURELLE_BILDUNG = "Interkulturelle Bildung"
    ITALIENISCH = "Italienisch"
    KUNST = "Kunst"
    KOERPERPFLEGE = "Körperpflege"
    LATEIN = "Latein"
    MATHEMATIK = "Mathematik"
    MECHATRONIK = "Mechatronik"
    MEDIENBILDUNG = "Medienbildung"
    MEDIENDIDAKTIK = "Mediendidaktik"
    METALLTECHNIK = "Metalltechnik"
    MINT = "MINT"
    MUSIK = "Musik"
    NACHHALTIGKEIT = "Nachhaltigkeit"
    NIEDERDEUTSCH = "Niederdeutsch"
    OPEN_EDUCATIONAL_RESOURCES = "Open Educational Resources"
    PHILOSOPHIE = "Philosophie"
    PHYSIK = "Physik"
    POLITIK = "Politik"
    PSYCHOLOGIE = "Psychologie"
    RELIGION = "Religion"
    RUSSISCH = "Russisch"
    SACHUNTERRICHT = "Sachunterricht"
    SEXUALERZIEHUNG = "Sexualerziehung"
    SONDERPAEDAGOGIK = "Sonderpädagogik"
    SORBISCH = "Sorbisch"
    SOZIALPAEDAGOGIK = "Sozialpädagogik"
    SPANISCH = "Spanisch"
    SPORT = "Sport"
    TEXTILTECHNIK_UND_BEKLEIDUNG = "Textiltechnik und Bekleidung"
    TUERKISCH = "Türkisch"
    WIRTSCHAFT_UND_VERWALTUNG = "Wirtschaft und Verwaltung"
    WIRTSCHAFTSKUNDE = "Wirtschaftskunde"
    UMWELTGEFAEHRDUNG_UMWELTSCHUTZ = "Umweltgefährdung, Umweltschutz"
    VERKEHRSERZIEHUNG = "Verkehrserziehung"
    WEITERBILDUNG = "Weiterbildung"
    WERKEN = "Werken"
    ZEITGEMAESSE_BILDUNG = "Zeitgemäße Bildung"
    SONSTIGES = "Sonstiges"

class Inhaltstyp(str, Enum):
    BILD = "Bild"
    VIDEO = "Video"
    AUDIO = "Audio"
    INTERAKTIVES_MEDIUM = "Interaktives Medium"
    UNTERRICHTSIDEE = "Unterrichtsidee"
    UNTERRICHTSPLAN = "Unterrichtsplan"
    UNTERRICHTSBAUSTEIN_REIHE = "Unterrichtsbaustein/-reihe"
    METHODEN = "Methoden"
    TESTS_FRAGEBOGENE = "Tests / Fragebögen"
    KURS = "Kurs"
    LERNOBJEKT_PFAD = "Lernobjekt / -pfad"
    PRAESENTATION = "Präsentation"
    LERNSPIEL = "Lernspiel"
    ARBEITSBLATT = "Arbeitsblatt"
    UEBUNGSMATERIAL = "Übungsmaterial"
    RECHERCHE_LERN_AUFTRAG = "Recherche, Lernauftrag"
    EXPERIMENT = "Experiment"
    PROJEKT_MATERIAL = "Projekt-Material"
    KREATIVE_OFFENE_AKTIVITAET = "Kreative, offene Aktivität"
    ENTDECKENDES_LERNEN = "Entdeckendes Lernen"
    ROLLENSPIEL = "Rollenspiel"
    FALLSTUDIE = "Fallstudie"
    ARTIKEL = "Artikel"
    LEHR_BUCH = "(Lehr-)Buch"
    HANDOUT = "Handout"
    SCHUELERARBEIT = "Schülerarbeit"
    NOTEN = "Noten"
    CHECKLISTE = "Checkliste"
    REGULARIEN_HANDBUCH = "Regularien, Handbuch"
    WEBSEITE = "Webseite"
    WEBBLOG = "Webblog"
    WIKI = "Wiki"
    WORT_VOKABELLISTE = "Wort-/Vokabelliste"
    NACHSCHLAGEWERK = "Nachschlagewerk"
    PRIMAERMATERIAL = "Primärmaterial"
    TEXTBAUSTEINE = "Textbausteine"
    PERSOEENLICHKEIT = "Persönlichkeit"
    DATEN = "Daten"
    FORMEL = "Formel"
    MODELL_3D = "Modell / 3D"
    TABELLEN = "Tabellen"
    NEWS = "News"
    QUELLE = "Quelle"
    TOOL = "Tool"
    BILDUNGSANGEBOT = "Bildungsangebot"
    EVENT_WETTBEWERB = "Event, Wettbewerb"

# Mapping-Dictionaries
BILDUNGSSTUFE_MAPPING = {
    "Elementarbereich": "http://w3id.org/openeduhub/vocabs/educationalContext/elementarbereich",
    "Primarstufe": "http://w3id.org/openeduhub/vocabs/educationalContext/grundschule",
    "Sekundarstufe I": "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_1",
    "Sekundarstufe II": "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe_2",
    "Sekundarstufe": "http://w3id.org/openeduhub/vocabs/educationalContext/sekundarstufe",
    "Hochschule": "http://w3id.org/openeduhub/vocabs/educationalContext/hochschule",
    "Berufliche Bildung": "http://w3id.org/openeduhub/vocabs/educationalContext/berufliche_bildung",
    "Fortbildung": "http://w3id.org/openeduhub/vocabs/educationalContext/fortbildung",
    "Erwachsenenbildung": "http://w3id.org/openeduhub/vocabs/educationalContext/erwachsenenbildung",
    "Förderschule": "http://w3id.org/openeduhub/vocabs/educationalContext/foerderschule",
    "Fernunterricht": "http://w3id.org/openeduhub/vocabs/educationalContext/fernunterricht"
}

FACH_MAPPING = {
    "Allgemein": "http://w3id.org/openeduhub/vocabs/discipline/720",
    "Alt-Griechisch": "http://w3id.org/openeduhub/vocabs/discipline/20003",
    "Agrarwirtschaft": "http://w3id.org/openeduhub/vocabs/discipline/04001",
    "Arbeit, Ernährung, Soziales": "http://w3id.org/openeduhub/vocabs/discipline/oeh01",
    "Arbeitslehre": "http://w3id.org/openeduhub/vocabs/discipline/020",
    "Arbeitssicherheit": "http://w3id.org/openeduhub/vocabs/discipline/04014",
    "Astronomie": "http://w3id.org/openeduhub/vocabs/discipline/46014",
    "Bautechnik": "http://w3id.org/openeduhub/vocabs/discipline/04002",
    "Berufliche Bildung": "http://w3id.org/openeduhub/vocabs/discipline/040",
    "Biologie": "http://w3id.org/openeduhub/vocabs/discipline/080",
    "Chemie": "http://w3id.org/openeduhub/vocabs/discipline/100",
    "Chinesisch": "http://w3id.org/openeduhub/vocabs/discipline/20041",
    "Darstellendes Spiel": "http://w3id.org/openeduhub/vocabs/discipline/12002",
    "Deutsch": "http://w3id.org/openeduhub/vocabs/discipline/120",
    "Deutsch als Zweitsprache": "http://w3id.org/openeduhub/vocabs/discipline/28002",
    "Elektrotechnik": "http://w3id.org/openeduhub/vocabs/discipline/04005",
    "Ernährung und Hauswirtschaft": "http://w3id.org/openeduhub/vocabs/discipline/04006",
    "Englisch": "http://w3id.org/openeduhub/vocabs/discipline/20001",
    "Pädagogik": "http://w3id.org/openeduhub/vocabs/discipline/440",
    "Esperanto": "http://w3id.org/openeduhub/vocabs/discipline/20090",
    "Ethik": "http://w3id.org/openeduhub/vocabs/discipline/160",
    "Farbtechnik und Raumgestaltung": "http://w3id.org/openeduhub/vocabs/discipline/04007",
    "Französisch": "http://w3id.org/openeduhub/vocabs/discipline/20002",
    "Geografie": "http://w3id.org/openeduhub/vocabs/discipline/220",
    "Geschichte": "http://w3id.org/openeduhub/vocabs/discipline/240",
    "Gesellschaftskunde": "http://w3id.org/openeduhub/vocabs/discipline/48005",
    "Gesundheit": "http://w3id.org/openeduhub/vocabs/discipline/260",
    "Hauswirtschaft": "http://w3id.org/openeduhub/vocabs/discipline/50001",
    "Holztechnik": "http://w3id.org/openeduhub/vocabs/discipline/04009",
    "Informatik": "http://w3id.org/openeduhub/vocabs/discipline/320",
    "Interkulturelle Bildung": "http://w3id.org/openeduhub/vocabs/discipline/340",
    "Italienisch": "http://w3id.org/openeduhub/vocabs/discipline/20004",
    "Kunst": "http://w3id.org/openeduhub/vocabs/discipline/060",
    "Körperpflege": "http://w3id.org/openeduhub/vocabs/discipline/04010",
    "Latein": "http://w3id.org/openeduhub/vocabs/discipline/20005",
    "Mathematik": "http://w3id.org/openeduhub/vocabs/discipline/380",
    "Mechatronik": "http://w3id.org/openeduhub/vocabs/discipline/oeh04010",
    "Medienbildung": "http://w3id.org/openeduhub/vocabs/discipline/900",
    "Mediendidaktik": "http://w3id.org/openeduhub/vocabs/discipline/400",
    "Metalltechnik": "http://w3id.org/openeduhub/vocabs/discipline/04011",
    "MINT": "http://w3id.org/openeduhub/vocabs/discipline/04003",
    "Musik": "http://w3id.org/openeduhub/vocabs/discipline/420",
    "Nachhaltigkeit": "http://w3id.org/openeduhub/vocabs/discipline/64018",
    "Niederdeutsch": "http://w3id.org/openeduhub/vocabs/discipline/niederdeutsch",
    "Open Educational Resources": "http://w3id.org/openeduhub/vocabs/discipline/44099",
    "Philosophie": "http://w3id.org/openeduhub/vocabs/discipline/450",
    "Physik": "http://w3id.org/openeduhub/vocabs/discipline/460",
    "Politik": "http://w3id.org/openeduhub/vocabs/discipline/480",
    "Psychologie": "http://w3id.org/openeduhub/vocabs/discipline/510",
    "Religion": "http://w3id.org/openeduhub/vocabs/discipline/520",
    "Russisch": "http://w3id.org/openeduhub/vocabs/discipline/20006",
    "Sachunterricht": "http://w3id.org/openeduhub/vocabs/discipline/28010",
    "Sexualerziehung": "http://w3id.org/openeduhub/vocabs/discipline/560",
    "Sonderpädagogik": "http://w3id.org/openeduhub/vocabs/discipline/44006",
    "Sorbisch": "http://w3id.org/openeduhub/vocabs/discipline/20009",
    "Sozialpädagogik": "http://w3id.org/openeduhub/vocabs/discipline/44007",
    "Spanisch": "http://w3id.org/openeduhub/vocabs/discipline/20007",
    "Sport": "http://w3id.org/openeduhub/vocabs/discipline/600",
    "Textiltechnik und Bekleidung": "http://w3id.org/openeduhub/vocabs/discipline/04012",
    "Türkisch": "http://w3id.org/openeduhub/vocabs/discipline/20008",
    "Wirtschaft und Verwaltung": "http://w3id.org/openeduhub/vocabs/discipline/04013",
    "Wirtschaftskunde": "http://w3id.org/openeduhub/vocabs/discipline/700",
    "Umweltgefährdung, Umweltschutz": "http://w3id.org/openeduhub/vocabs/discipline/640",
    "Verkehrserziehung": "http://w3id.org/openeduhub/vocabs/discipline/660",
    "Weiterbildung": "http://w3id.org/openeduhub/vocabs/discipline/680",
    "Werken": "http://w3id.org/openeduhub/vocabs/discipline/50005",
    "Zeitgemäße Bildung": "http://w3id.org/openeduhub/vocabs/discipline/72001",
    "Sonstiges": "http://w3id.org/openeduhub/vocabs/discipline/999"
}

INHALTSTYP_MAPPING = {
    "Bild": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/b8fb5fb2-d8bf-4bbe-ab68-358b65a26bed",
    "Video": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/38774279-af36-4ec2-8e70-811d5a51a6a1",
    "Audio": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/39197d6f-dfb1-4e82-92e5-79f906e9d2a9",
    "Interaktives Medium": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/05aa0f49-7e1b-498b-a7d5-c5fc8e73b2e2",
    "Unterrichtsidee": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/11f438d7-cb11-49c2-8e67-2dd7df677092",
    "Unterrichtsplan": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/8526273b-2b21-46f2-ac8d-bbf362c8a690",
    "Unterrichtsbaustein/-reihe": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/f1341358-3f91-449b-b6eb-f58636f756a0",
    "Methoden": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/101c0c66-5202-4eba-9ebf-79f4903752b9",
    "Tests / Fragebögen": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/02bfd0fe-96ab-4dd6-a306-ec362ec25ea0",
    "Kurs": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/e10e9add-700e-4b57-a9c5-8f1088bb0545",
    "Lernobjekt / -pfad": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/3469a5e7-86d1-4376-bd3d-1f2b183ed94a",
    "Präsentation": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/1e300ea3-a687-45a3-b215-9c240c1666dc",
    "Lernspiel": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/ded96854-280a-45ac-ad3a-f5b9b8dd0a03",
    "Arbeitsblatt": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/c8e52242-361b-4a2a-b95d-25e516b28b45",
    "Übungsmaterial": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/0b2d7dec-8eb1-4a28-9cf2-4f3a4f5a511b",
    "Recherche, Lernauftrag": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/90a082d8-ee5f-4b33-bd5c-f1738262c47d",
    "Experiment": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/ffe4d8e8-3cfd-4e9a-b025-83f129eb5c9d",
    "Projekt-Material": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/71c71f72-fc8d-4263-902f-abf1366a73ca",
    "Kreative, offene Aktivität": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/57bfc743-4c94-4bdd-bdfa-c638a062d151",
    "Entdeckendes Lernen": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/ec402e87-c623-47e2-8d2e-1c4ea6923409",
    "Rollenspiel": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/d0c115e4-848d-4aea-8e31-23869e9add3e",
    "Fallstudie": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/41eaccae-899b-4209-8a54-c793a3cdf538",
    "Artikel": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/c77df53a-2611-4029-9712-f9c0eeb032a3",
    "(Lehr-)Buch": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/3927fdb6-0477-422c-9f5a-6285948aeaf4",
    "Handout": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/9abf6ace-85bc-44e2-af4f-93a6bd255a21",
    "Schülerarbeit": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/fece0442-c686-4496-b97e-06d87782009b",
    "Noten": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/854e5bcf-d898-43ca-bc70-caf2a7e33673",
    "Checkliste": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/99f3bb30-22c0-4b46-871c-43ab4b6baf6f",
    "Regularien, Handbuch": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/ac925aae-1f3c-4817-a9dd-b9b24c336b0d",
    "Webseite": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/55761ec6-0cd4-4677-86ee-6f395934dae7",
    "Webblog": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/ac4987d7-5d09-4a21-82c6-268ed6cdc7eb",
    "Wiki": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/6f669beb-273a-4153-bdb6-4c6d59b2366d",
    "Wort-/Vokabelliste": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/9337a93e-777d-4d76-99a5-51f5e9935e63",
    "Nachschlagewerk": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/cf8929a7-d521-4f17-bbe3-96748c862486",
    "Primärmaterial": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/1c610f61-9bf0-4d77-8536-b713a3733510",
    "Textbausteine": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/2c151a4e-556e-42db-9e44-3a581deb5834",
    "Persönlichkeit": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/b1e25325-d403-44f0-814a-ff2f5d866931",
    "Daten": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/620a3fee-ac87-40e6-8408-20b48b430eca",
    "Formel": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/c2fc554c-a7ae-4af7-a785-d727c5a8d0db",
    "Modell / 3D": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/25957b6b-338e-4379-ba4f-67fc7654ef34",
    "Tabellen": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/a0b83e5a-eaa4-4df8-9eec-3678abd60c25",
    "News": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/9bbb50a2-10c5-4a8b-9e0e-6a5fc86c40fe",
    "Quelle": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/2e678af3-1026-4171-b88e-3b3a915d1673",
    "Tool": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/37a3ad9c-727f-4b74-bbab-27d59015c695",
    "Bildungsangebot": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/6b6786df-9ce9-44bf-8a04-caebd4456fcf",
    "Event, Wettbewerb": "http://w3id.org/openeduhub/vocabs/new_lrt_aggregated/b06c5816-60c7-4f1b-bcd7-95d70aaa4740"
}

# Pydantic-Modelle für Unterrichtsphasen und den gesamten Ablauf
class Unterrichtsphase(BaseModel):
    titel: str
    kurzbeschreibung: str

class Unterrichtsablauf(BaseModel):
    titel: str
    beschreibung: str
    unterrichtsphasen: List[Unterrichtsphase]
    anzahl_phasen: int

class PhaseFilter(BaseModel):
    phase_titel: str
    suchbegriff_thema: str
    bildungstufe_uri: str
    fachbereich_uri: str
    inhaltstyp_uri: str

class GesamtOutput(BaseModel):
    unterrichtsablauf_text: str
    anzahl_phasen: int
    phase_filter: List[PhaseFilter]

# ---------------------------
# Funktionen zur Generierung des Unterrichtsablaufs und der Filter
# ---------------------------

def normalize_inhaltstyp(inhaltstyp: str) -> str:
    """
    Normalisiert den Inhaltstyp, um sicherzustellen, dass er mit den Enum-Werten übereinstimmt.
    """
    mapping = {
        "Interaktive Übung": "Interaktives Medium",
        "Präsentation": "Präsentation",
        "Modell_3D": "Modell / 3D",
        # Fügen Sie weitere Synonyme oder ähnliche Begriffe hinzu, falls notwendig
    }
    return mapping.get(inhaltstyp, inhaltstyp)  # Rückgabe des Originals, falls keine Übereinstimmung

def generate_unterrichtsablauf(breadcrumb: str, beschreibung: str, bildungsstufe: str, fach: str, sprache: str) -> Unterrichtsablauf:
    system_prompt = (
        "Du bist ein hilfreicher KI-Assistent für Lehr- und Lernsituationen, der sachlich korrekte und verständliche Antworten gibt, um Lernenden und Lehrenden komplexe Themen näherzubringen. "
        "Deine Antworten sind relevant, aktuell und fachlich fundiert, basieren auf vertrauenswürdigen Quellen und enthalten keine falschen oder spekulativen Aussagen. "
        "Du passt deine Sprache an die Zielgruppe an, bleibst klar und fachlich präzise, um den Lernerfolg zu fördern.\n\n"
        "Du achtest darauf, dass deine Antworten rechtlich unbedenklich sind, insbesondere in Bezug auf Urheberrecht, Datenschutz, Persönlichkeitsrechte und Jugendschutz. "
        "Die Herkunft der Informationen wird bei Bedarf transparent gemacht. Du orientierst dich an anerkannten didaktischen Prinzipien, lieferst praxisorientierte Erklärungen und vermeidest unnötige Komplexität.\n\n"
        "Neutralität und Objektivität stehen im Fokus. Persönliche Meinungen oder parteiische Bewertungen sind ausgeschlossen. Deine Inhalte werden regelmäßig überprüft, um den höchsten Qualitätsstandards zu genügen, unter anderem durch den Einsatz von LLM-gestützter Analyse. "
        "Dein Ziel ist es, sachliche, aktuelle und rechtlich wie didaktisch einwandfreie Informationen bereitzustellen.\n\n"
        "Basierend auf den folgenden Informationen erstelle einen strukturierten Unterrichtsablauf für eine Unterrichtseinheit.\n\n"
        f"Breadcrumb-Menü: {breadcrumb}\n"
        f"Beschreibungstext: {beschreibung}\n"
        f"Bildungsstufe: {bildungsstufe}\n"
        f"Fachgebiet: {fach}\n"
        f"Sprache: {sprache}\n\n"
        "Bitte geben Sie ausschließlich gültiges JSON zurück, ohne zusätzliche Erklärungen oder Kommentare.\n\n"
        "{\n"
        '  "titel": "Titel für den Ablauf",\n'
        '  "beschreibung": "Beschreibung des Unterrichtsablaufs (ca. 500 Zeichen)",\n'
        '  "unterrichtsphasen": [\n'
        '    {\n'
        '      "titel": "Titel der Phase",\n'
        '      "kurzbeschreibung": "Kurzbeschreibung der Phase (2 Sätze)"\n'
        '    }\n'
        '    # Weitere Phasen können hinzugefügt werden\n'
        '  ],\n'
        '  "anzahl_phasen": Anzahl_der_Phase\n'
        "}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modellname korrigiert
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )

        content = response.choices[0].message.content.strip()

        # Debug-Ausgabe
        print("Rohe Antwort vom Modell (Unterrichtsablauf):")
        print(content)

        # Entfernen von Kommentaren und Parsing des JSON-Inhalts
        json_content = re.sub(r'#.*', '', content, flags=re.MULTILINE).strip()
        parsed_content = json.loads(json_content)

        # Validierung mit Pydantic
        ablauf = Unterrichtsablauf.parse_obj(parsed_content)

        return ablauf

    except OpenAIError as e:
        print(f"OpenAI API-Fehler: {e}")
        raise
    except json.JSONDecodeError:
        print("Fehler beim Parsen der JSON-Antwort für den Unterrichtsablauf.")
        print(f"Antwortinhalt: {content}")
        raise
    except ValidationError as ve:
        print("Validierungsfehler bei der Pydantic-Modellierung des Unterrichtsablaufs:")
        for error in ve.errors():
            print(f"Fehlerfeld: {error['loc']}, Fehler: {error['msg']}, Typ: {error['type']}")
        raise
    except Exception as ex:
        print(f"Ein unerwarteter Fehler ist aufgetreten beim Generieren des Unterrichtsablaufs: {ex}")
        raise

def generate_phase_filter(unterrichtsablauf: Unterrichtsablauf, phase: Unterrichtsphase, bildungsstufe: str, fach: str) -> PhaseFilter:
    system_prompt = (
        "Du bist ein hilfreicher KI-Assistent für Lehr- und Lernsituationen, der sachlich korrekte und verständliche Antworten gibt, um Lernenden und Lehrenden komplexe Themen näherzubringen. "
        "Deine Antworten sind relevant, aktuell und fachlich fundiert, basieren auf vertrauenswürdigen Quellen und enthalten keine falschen oder spekulativen Aussagen. "
        "Du passt deine Sprache an die Zielgruppe an, bleibst klar und fachlich präzise, um den Lernerfolg zu fördern.\n\n"
        "Du achtest darauf, dass deine Antworten rechtlich unbedenklich sind, insbesondere in Bezug auf Urheberrecht, Datenschutz, Persönlichkeitsrechte und Jugendschutz. "
        "Die Herkunft der Informationen wird bei Bedarf transparent gemacht. Du orientierst dich an anerkannten didaktischen Prinzipien, lieferst praxisorientierte Erklärungen und vermeidest unnötige Komplexität.\n\n"
        "Neutralität und Objektivität stehen im Fokus. Persönliche Meinungen oder parteiische Bewertungen sind ausgeschlossen. Deine Inhalte werden regelmäßig überprüft, um den höchsten Qualitätsstandards zu genügen. "
        "Dein Ziel ist es, sachliche, aktuelle und didaktisch einwandfreie Informationen bereitzustellen.\n\n"
        "Basierend auf der folgenden Unterrichtsphase sollst du einen Filter erstellen, der passende Bildungsinhalte aus einer Datenbank abruft. "
        "Der Filter soll Bildungsstufe, Fach, Inhaltstyp (aus den vorgegebenen Optionen) und Thema umfassen. "
        "Die abgerufenen Inhalte sollen methodisch und didaktisch für die jeweilige Phase passend sein und den Lehr- und Lernprozess bestmöglich unterstützen.\n\n"
        "Hier sind die Informationen zur aktuellen Phase:\n"
        f"Phase Titel: {phase.titel}\n"
        f"Kurzbeschreibung: {phase.kurzbeschreibung}\n\n"
        "Hintergrundinformationen:\n"
        f"Bildungsstufe: {bildungsstufe}\n"
        f"Fach: {fach}\n\n"
        "Berücksichtige dabei die folgenden Kriterien:\n"
        "- Thematisch fokussiert sich auf Inhalte und das spezifische Thema der Unterrichtseinheit (z.B. Informationsvermittlung, Erarbeitung).\n"
        "- Methodisch bezieht sich auf die Art und Weise, wie der Unterricht durchgeführt und gestaltet wird, einschließlich der Interaktionsformen und didaktischen Ansätze (z.B. Motivation, Organisation der Gruppe, Reflexion, Differenzierung).\n"
        "- Falls Elemente von beidem vorhanden sind, identifiziere, ob ein Aspekt überwiegt oder ob eine gleichwertige Mischung aus beiden vorliegt.\n\n"
        "Schlage basierend auf dem Schwerpunkt des Abschnitts der Lehr- und Lernsituation (thematisch oder methodisch) den am besten geeigneten Inhaltstyp aus den vorgegebenen Optionen vor. "
        "Verwende dabei unterschiedliche Inhaltstypen für verschiedene Phasen, um den spezifischen Anforderungen jeder Phase gerecht zu werden.\n\n"
        "Beachte dabei, dass der 'inhaltstyp' immer eines der folgenden sein muss:\n"
        "- Bild\n"
        "- Video\n"
        "- Audio\n"
        "- Interaktives Medium\n"
        "- Unterrichtsidee\n"
        "- Unterrichtsplan\n"
        "- Unterrichtsbaustein/-reihe\n"
        "- Methoden\n"
        "- Tests / Fragebögen\n"
        "- Kurs\n"
        "- Lernobjekt / -pfad\n"
        "- Präsentation\n"
        "- Lernspiel\n"
        "- Arbeitsblatt\n"
        "- Übungsmaterial\n"
        "- Recherche, Lernauftrag\n"
        "- Experiment\n"
        "- Projekt-Material\n"
        "- Kreative, offene Aktivität\n"
        "- Entdeckendes Lernen\n"
        "- Rollenspiel\n"
        "- Fallstudie\n"
        "- Artikel\n"
        "- (Lehr-)Buch\n"
        "- Handout\n"
        "- Schülerarbeit\n"
        "- Noten\n"
        "- Checkliste\n"
        "- Regularien, Handbuch\n"
        "- Webseite\n"
        "- Webblog\n"
        "- Wiki\n"
        "- Wort-/Vokabelliste\n"
        "- Nachschlagewerk\n"
        "- Primärmaterial\n"
        "- Textbausteine\n"
        "- Persönlichkeit\n"
        "- Daten\n"
        "- Formel\n"
        "- Modell / 3D\n"
        "- Tabellen\n"
        "- News\n"
        "- Quelle\n"
        "- Tool\n"
        "- Bildungsangebot\n"
        "- Event, Wettbewerb\n\n"
        "Stelle sicher, dass der 'inhaltstyp' immer in der Antwort enthalten ist und exakt einem der vorgegebenen Enum-Werte entspricht.\n\n"
        "Beispiele zur Unterstützung:\n"
        "- Einführung: Video eignet sich gut, um das Interesse zu wecken und das Thema vorzustellen.\n"
        "- Erarbeitung: Arbeitsblatt hilft dabei, das erlernte Wissen zu vertiefen.\n"
        "- Wissenskontrolle: Tests / Fragebögen sind ideal, um das Verständnis zu überprüfen.\n"
        "- Experimentelle Phase: Experiment eignet sich, um praktische Anwendungen zu demonstrieren.\n"
        "- Reflexion: Methoden sind geeignet, um die Schülerinnen und Schüler zur Reflexion anzuregen.\n"
        "- Interaktive Übung: Lernspiel fördert das aktive Lernen und die Anwendung des Gelernten.\n"
        "- Gruppenarbeit: Rollenspiel unterstützt die Zusammenarbeit und das Verständnis komplexer Konzepte.\n\n"
        "Bitte geben Sie ausschließlich gültiges JSON zurück, ohne zusätzliche Erklärungen oder Kommentare:\n"
        "{\n"
        '  "thema": "Suchbegriff/Thema",\n'
        '  "bildungsstufe": "Wert aus Bildungsstufe Enum",\n'
        '  "fach": "Wert aus Fach Enum",\n'
        '  "inhaltstyp": "Wert aus Inhaltstyp Enum"\n'
        "}"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Modellname korrigiert
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        content = response.choices[0].message.content.strip()

        # Debug-Ausgabe
        print(f"Rohe Antwort vom Modell für Phase '{phase.titel}':")
        print(content)

        # Verwenden Sie Regex, um den JSON-Teil der Antwort zu extrahieren
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_match:
            raise ValueError("Die Antwort enthält kein gültiges JSON-Objekt.")

        json_str = json_match.group()

        # Parsen des JSON-Inhalts
        parsed_content = json.loads(json_str)

        # Normalisierung des Inhaltstyps
        parsed_content['inhaltstyp'] = normalize_inhaltstyp(parsed_content.get('inhaltstyp', ''))

        # Validierung und Parsing des Inhalts mit Pydantic
        class KlassifikationErgebnisPhase(BaseModel):
            thema: str
            bildungsstufe: Bildungsstufe
            fach: Fach
            inhaltstyp: Inhaltstyp

        try:
            ergebnis = KlassifikationErgebnisPhase.parse_obj(parsed_content)
        except ValidationError as ve:
            print("Validierungsfehler bei der Pydantic-Modellierung:")
            for error in ve.errors():
                print(f"Fehlerfeld: {error['loc']}, Fehler: {error['msg']}, Typ: {error['type']}")
            # Falls ein Fehler auftritt, entfernen wir die fehlerhaften Felder und versuchen erneut zu parsen
            if any(err['loc'] == ('inhaltstyp',) for err in ve.errors()):
                del parsed_content['inhaltstyp']
            if any(err['loc'] == ('fach',) for err in ve.errors()):
                del parsed_content['fach']
            if any(err['loc'] == ('bildungsstufe',) for err in ve.errors()):
                del parsed_content['bildungsstufe']
            # Parst erneut
            ergebnis = KlassifikationErgebnisPhase.parse_obj(parsed_content)

        # Mappen der Bildungsstufe, Fachbereich und Inhaltstyp auf ihre entsprechenden URIs
        bildungstufe_uri = BILDUNGSSTUFE_MAPPING.get(ergebnis.bildungsstufe)
        fachbereich_uri = FACH_MAPPING.get(ergebnis.fach)
        inhaltstyp_uri = INHALTSTYP_MAPPING.get(ergebnis.inhaltstyp)

        # Sicherstellen, dass alle URIs gefunden wurden
        if not bildungstufe_uri:
            raise ValueError(f"Keine URI für Bildungsstufe '{ergebnis.bildungsstufe}' gefunden.")
        if not fachbereich_uri:
            raise ValueError(f"Keine URI für Fach '{ergebnis.fach}' gefunden.")
        if not inhaltstyp_uri:
            raise ValueError(f"Keine URI für Inhaltstyp '{ergebnis.inhaltstyp}' gefunden.")

        # Erstellen des PhaseFilter-Objekts
        filter_obj = PhaseFilter(
            phase_titel=phase.titel,
            suchbegriff_thema=ergebnis.thema,
            bildungstufe_uri=bildungstufe_uri,
            fachbereich_uri=fachbereich_uri,
            inhaltstyp_uri=inhaltstyp_uri
        )

        return filter_obj

    except OpenAIError as e:
        print(f"OpenAI API-Fehler bei der Generierung der Filter für Phase '{phase.titel}': {e}")
        raise
    except json.JSONDecodeError:
        print(f"Fehler beim Parsen der JSON-Antwort für die Phase '{phase.titel}'.")
        print(f"Antwortinhalt: {content}")
        raise
    except ValidationError as ve:
        print(f"Validierungsfehler bei der Pydantic-Modellierung des Phase-Filters für Phase '{phase.titel}':")
        for error in ve.errors():
            print(f"Fehlerfeld: {error['loc']}, Fehler: {error['msg']}, Typ: {error['type']}")
        raise
    except Exception as ex:
        print(f"Ein unerwarteter Fehler ist aufgetreten beim Generieren der Filter für Phase '{phase.titel}': {ex}")
        raise

# ---------------------------
# Hauptfunktion zur Generierung des gesamten Outputs
# ---------------------------

def main():
    # Demo-Daten
    breadcrumb = "Physik - Optik - Menschliches Auge"
    beschreibung = (
        "Das menschliche Auge ist unser wahrscheinlich wichtigstes Sinnesorgan: "
        "Über das Auge nehmen wir die Welt wahr, erkennen Formen und Farben. "
        "Das Auge erfüllt also wichtige biologische Funktionen. "
        "Unter physikalischen Gesichtspunkten betrachtet besteht das Auge im Wesentlichen aus einer Sammellinse, "
        "die einen entfernten Gegenstand auf die Netzhaut abbildet. "
        "Mit diesem Wissen lässt sich der Prozess des Sehens physikalisch erklären."
    )
    bildungsstufe = "Sekundarstufe I"
    fach = "Physik"
    sprache = "deutsch"

    try:
        # Schritt 1: Generierung des Unterrichtsablaufs
        unterrichtsablauf = generate_unterrichtsablauf(breadcrumb, beschreibung, bildungsstufe, fach, sprache)

        # Schritt 2: Generierung der Filter für jede Phase
        phase_filters = []
        for phase in unterrichtsablauf.unterrichtsphasen:
            filter_obj = generate_phase_filter(unterrichtsablauf, phase, bildungsstufe, fach)
            phase_filters.append(filter_obj)

        # Zusammenführung der Ergebnisse
        unterrichtsablauf_text = (
            f"Titel: {unterrichtsablauf.titel}\n\n"
            f"Beschreibung: {unterrichtsablauf.beschreibung}\n\n"
            "Unterrichtsphasen:\n" +
            "\n".join([f"- {phase.titel}: {phase.kurzbeschreibung}" for phase in unterrichtsablauf.unterrichtsphasen])
        )

        gesamt_output = GesamtOutput(
            unterrichtsablauf_text=unterrichtsablauf_text,
            anzahl_phasen=unterrichtsablauf.anzahl_phasen,
            phase_filter=phase_filters
        )

        # Ausgabe
        print("\n\nGesamtausgabe (JSON):")
        # Für Pydantic v2 verwenden wir model_dump_json() ohne 'ensure_ascii'
        print(gesamt_output.model_dump_json(indent=2))

        # Optional: Formatierte Ausgabe
        print("\n\nFormatierte Gesamtausgabe:")
        print(f"Titel: {unterrichtsablauf.titel}\n")
        print(f"Beschreibung:\n{unterrichtsablauf.beschreibung}\n")
        print("Unterrichtsphasen:")
        for idx, phase in enumerate(unterrichtsablauf.unterrichtsphasen, 1):
            print(f"  Phase {idx}: {phase.titel}")
            print(f"    {phase.kurzbeschreibung}")
        print(f"\nAnzahl der Phasen: {unterrichtsablauf.anzahl_phasen}\n")

        print("Phase Filter:")
        for filter_obj in phase_filters:
            print(f"- Phase Titel: {filter_obj.phase_titel}")
            print(f"  Suchbegriff/Thema: {filter_obj.suchbegriff_thema}")
            print(f"  Bildungsstufe URI: {filter_obj.bildungstufe_uri}")
            print(f"  Fachbereich URI: {filter_obj.fachbereich_uri}")
            print(f"  Inhaltstyp URI: {filter_obj.inhaltstyp_uri}\n")

    except Exception as e:
        print(f"Die Klassifikation konnte nicht durchgeführt werden: {e}")

if __name__ == "__main__":
    main()
