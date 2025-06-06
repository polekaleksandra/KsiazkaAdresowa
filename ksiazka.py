import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTextEdit, QMessageBox, QComboBox
)
from collections import Counter
dane = "adresy.json"
class KsiazkaAdresowa(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Książka Adresowa")
        self.kontakty = []
        self.inicjalizuj_interfejs()
        self.wczytaj_dane()
    def inicjalizuj_interfejs(self):
        uklad_glowny = QVBoxLayout()
        self.pola = {
            'Imię': QLineEdit(),
            'Nazwisko': QLineEdit(),
            'Telefon': QLineEdit(),
            'Ulica': QLineEdit(),
            'Miasto': QLineEdit()
        }
        for i in self.pola:
            wiersz = QHBoxLayout()
            wiersz.addWidget(QLabel(i))
            wiersz.addWidget(self.pola[i])
            uklad_glowny.addLayout(wiersz)
        self.przycisk_dodaj = QPushButton("Dodaj adres")
        self.przycisk_dodaj.clicked.connect(self.dodaj_adres)
        uklad_glowny.addWidget(self.przycisk_dodaj)
        uklad_wyszukiwania = QHBoxLayout()
        self.pole_wyszukiwania = QLineEdit()
        self.kryterium_wyszukiwania = QComboBox()
        for j in self.pola:
            self.kryterium_wyszukiwania.addItem(j)
        przycisk_szukaj = QPushButton("Szukaj")
        przycisk_szukaj.clicked.connect(self.szukaj_adres)
        uklad_wyszukiwania.addWidget(QLabel("Szukaj:"))
        uklad_wyszukiwania.addWidget(self.pole_wyszukiwania)
        uklad_wyszukiwania.addWidget(self.kryterium_wyszukiwania)
        uklad_wyszukiwania.addWidget(przycisk_szukaj)
        uklad_glowny.addLayout(uklad_wyszukiwania)
        self.przycisk_statystyki = QPushButton("Pokaż statystyki miast")
        self.przycisk_statystyki.clicked.connect(self.pokaz_statystyki)
        uklad_glowny.addWidget(self.przycisk_statystyki)
        self.wynik = QTextEdit()
        self.wynik.setReadOnly(True)
        uklad_glowny.addWidget(self.wynik)
        self.setLayout(uklad_glowny)
    def dodaj_adres(self):
        nowy_kontakt = {}
        for k in self.pola:
            nowy_kontakt[k] = self.pola[k].text().strip()
        for i in self.kontakty:
            if i['Imię'].lower() == nowy_kontakt['Imię'].lower() and i['Nazwisko'].lower() == nowy_kontakt['Nazwisko'].lower():
                QMessageBox.warning(self, "Błąd", "Taki użytkownik już istnieje!")
                return
        self.kontakty.append(nowy_kontakt)
        self.zapisz_dane()
        self.wyczysc_pola()
        self.wynik.setText("Dodano kontakt:\n" + json.dumps(nowy_kontakt, indent=2, ensure_ascii=False))
    def szukaj_adres(self):
        zapytanie = self.pole_wyszukiwania.text().lower().strip()
        pole = self.kryterium_wyszukiwania.currentText()
        wyniki = []
        for j in self.kontakty:
            if zapytanie in j[pole].lower():
                wyniki.append(j)
        if len(wyniki) > 0:
            self.wynik.setText("Wyniki wyszukiwania:\n" + json.dumps(wyniki, indent=2, ensure_ascii=False))
        else:
            self.wynik.setText("Brak wyników.")
    def pokaz_statystyki(self):
        miasta = []
        for i in self.kontakty:
            miasta.append(i["Miasto"])
        statystyki = Counter(miasta)
        tekst_statystyki = ""
        for miasto in statystyki:
            tekst_statystyki += f"{miasto}: {statystyki[miasto]}\n"
        self.wynik.setText("Statystyka miast:\n" + tekst_statystyki)
    def wyczysc_pola(self):
        for pole in self.pola.values():
            pole.clear()
    def zapisz_dane(self):
        with open(dane, "w", encoding="utf-8") as plik:
            json.dump(self.kontakty, plik, indent=2, ensure_ascii=False)
    def wczytaj_dane(self):
        if os.path.exists(dane):
            with open(dane, "r", encoding="utf-8") as plik:
                self.kontakty = json.load(plik)
if __name__ == "__main__":
    aplikacja = QApplication(sys.argv)
    okno = KsiazkaAdresowa()
    okno.resize(650, 500)
    okno.show()
    sys.exit(aplikacja.exec_())
