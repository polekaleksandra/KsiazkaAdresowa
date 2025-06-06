import sys
import json
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLineEdit, QLabel, QTextEdit, QMessageBox, QComboBox
)

dane = "adresy.json"

class ksiazka_adresowa(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Książka Adresowa")
        self.lista_kontaktow = []
        self.utworz_interfejs()
        self.wczytaj_dane_z_pliku()

    def utworz_interfejs(self):
        uklad_glowny = QVBoxLayout()
        self.pola_kontaktowe = {
            'Imię': QLineEdit(),
            'Nazwisko': QLineEdit(),
            'Telefon': QLineEdit(),
            'Ulica': QLineEdit(),
            'Miasto': QLineEdit()
        }
        for etykieta, pole in self.pola_kontaktowe.items():
            wiersz = QHBoxLayout()
            wiersz.addWidget(QLabel(etykieta))
            wiersz.addWidget(pole)
            uklad_glowny.addLayout(wiersz)

        self.przycisk_dodaj = QPushButton("dodaj adres")
        self.przycisk_dodaj.clicked.connect(self.dodaj_adres)
        uklad_glowny.addWidget(self.przycisk_dodaj)
        self.przycisk_usun = QPushButton("usun kontakt")
        self.przycisk_usun.clicked.connect(self.usun_kontakt)
        uklad_glowny.addWidget(self.przycisk_usun)
        self.przycisk_wszystkie = QPushButton("wszystkie twoje kontakty")
        self.przycisk_wszystkie.clicked.connect(self.pokaz_wszystkie)
        uklad_glowny.addWidget(self.przycisk_wszystkie)
        uklad_wyszukiwania = QHBoxLayout()
        self.pole_tekstowe_wyszukiwania = QLineEdit()
        self.lista_kryteriow_wyszukiwania = QComboBox()

        for etykieta in self.pola_kontaktowe:
            self.lista_kryteriow_wyszukiwania.addItem(etykieta)

        przycisk_szukaj = QPushButton("szukaj")
        przycisk_szukaj.clicked.connect(self.szukaj_adres)
        uklad_wyszukiwania.addWidget(QLabel("wyszukaj:"))
        uklad_wyszukiwania.addWidget(self.pole_tekstowe_wyszukiwania)
        uklad_wyszukiwania.addWidget(self.lista_kryteriow_wyszukiwania)
        uklad_wyszukiwania.addWidget(przycisk_szukaj)
        uklad_glowny.addLayout(uklad_wyszukiwania)
        self.przycisk_statystyki = QPushButton("pokaz statystyki miast")
        self.przycisk_statystyki.clicked.connect(self.pokaz_statystyki_miast)
        uklad_glowny.addWidget(self.przycisk_statystyki)
        self.pole_wynikowe = QTextEdit()
        self.pole_wynikowe.setReadOnly(True)
        uklad_glowny.addWidget(self.pole_wynikowe)
        self.setLayout(uklad_glowny)

    def dodaj_adres(self):
        nowy_kontakt = {}
        for nazwa_pola, pole in self.pola_kontaktowe.items():
            wartosc = pole.text().strip()
            if not wartosc:
                QMessageBox.warning(self, "błąd", f"pole '{nazwa_pola}' nie moze zostac puste")
                return
            nowy_kontakt[nazwa_pola] = wartosc
        for istniejacy_kontakt in self.lista_kontaktow:
            if (istniejacy_kontakt['Imię'].lower() == nowy_kontakt['Imię'].lower() and
                    istniejacy_kontakt['Nazwisko'].lower() == nowy_kontakt['Nazwisko'].lower()):
                QMessageBox.warning(self, "błąd", "taki kontakt juz istnieje")
                return
        self.lista_kontaktow.append(nowy_kontakt)
        self.zapisz_dane_do_pliku()
        self.wyczysc_pola()
        self.pole_wynikowe.setText("dodano kontakt:\n" + json.dumps(nowy_kontakt, indent=2, ensure_ascii=False))

    def usun_kontakt(self):
        imie = self.pola_kontaktowe["Imię"].text().strip().lower()
        nazwisko = self.pola_kontaktowe["Nazwisko"].text().strip().lower()
        if not imie or not nazwisko:
            QMessageBox.warning(self, "błąd", "wpisz dane aby usunąć kontakt.")
            return
        for kontakt in self.lista_kontaktow:
            if kontakt["Imię"].lower() == imie and kontakt["Nazwisko"].lower() == nazwisko:
                self.lista_kontaktow.remove(kontakt)
                self.zapisz_dane_do_pliku()
                self.wyczysc_pola()
                self.pole_wynikowe.setText(f"usunięto kontakt:\n{json.dumps(kontakt, indent=2, ensure_ascii=False)}")
                return
        QMessageBox.information(self, "informacja", "nie znaleziono tego kontaktu do usunięcia.")

    def pokaz_wszystkie(self):
        if not self.lista_kontaktow:
            self.pole_wynikowe.setText("brak kontaktów.")
            return
        tekst = "wszystkie kontakty:\n" + json.dumps(self.lista_kontaktow, indent=2, ensure_ascii=False)
        self.pole_wynikowe.setText(tekst)

    def szukaj_adres(self):
        tekst_wyszukiwania = self.pole_tekstowe_wyszukiwania.text().strip().lower()

        if not tekst_wyszukiwania:
            QMessageBox.warning(self, "błąd", "Wpisz coś w polu wyszukiwania, aby rozpocząć szukanie.")
            return
        pole_wyszukiwania = self.lista_kryteriow_wyszukiwania.currentText()
        znalezione_kontakty = []
        for kontakt in self.lista_kontaktow:
            if tekst_wyszukiwania in kontakt[pole_wyszukiwania].lower():
                znalezione_kontakty.append(kontakt)
        if znalezione_kontakty:
            self.pole_wynikowe.setText(
                "Wyniki wyszukiwania:\n" + json.dumps(znalezione_kontakty, indent=2, ensure_ascii=False))
        else:
            self.pole_wynikowe.setText("Brak wyników.")

    def pokaz_statystyki_miast(self):
        lista_miast = []
        for kontakt in self.lista_kontaktow:
            miasto = kontakt["Miasto"]
            lista_miast.append(miasto)
        statystyki = {}
        for miasto in lista_miast:
            if miasto in statystyki:
                statystyki[miasto] = statystyki[miasto] + 1
            else:
                statystyki[miasto] = 1
        tekst_statystyk = ""
        for miasto, liczba in statystyki.items():
            tekst_statystyk = tekst_statystyk + f"{miasto}: {liczba}\n"
        self.pole_wynikowe.setText("Statystyka miast:\n" + tekst_statystyk)
    def wyczysc_pola(self):
        for pole in self.pola_kontaktowe.values():
            pole.clear()

    def zapisz_dane_do_pliku(self):
        with open(dane, "w", encoding="utf-8") as plik_json:
            json.dump(self.lista_kontaktow, plik_json, indent=2, ensure_ascii=False)

    def wczytaj_dane_z_pliku(self):
        if os.path.exists(dane):
            with open(dane, "r", encoding="utf-8") as plik_json:
                self.lista_kontaktow = json.load(plik_json)

if __name__ == "__main__":
    aplikacja_qt = QApplication(sys.argv)
    okno_programu = ksiazka_adresowa()
    okno_programu.resize(650, 500)
    okno_programu.show()
    sys.exit(aplikacja_qt.exec_())
