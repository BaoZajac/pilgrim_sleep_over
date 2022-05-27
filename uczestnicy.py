from main import read_db
import datetime
from datetime import datetime


class Pielgrzymi:
    def __init__(self, file_path_pielgrzymi):
        self.dane = read_db(file_path_pielgrzymi)
        # self.id_pielgrzyma = None             # TODO: czy to jest potrzebne?
        # self.funkcja_pielgrzyma = None
        self.funkcyjni_0 = []
        self.funkcyjni_1 = []
        self.funkcyjni_2 = []
        self.funkcyjni_szkola = []
        self.pielgrzymi_bez_noclegu = []
        self.pielgrzymi_pozostali = []
        self.suma_priorytetow = {}

        self.funkcyjny()
        self.zwykly_pielgrzym()
        self.funkcja_priorytet()
        self.zwykly_pielg_priorytet()

        self.wszyscy_pielgrzymi = self.funkcyjni_0 + self.funkcyjni_1 + self.funkcyjni_2 + self.funkcyjni_szkola \
                                  + self.pielgrzymi_bez_noclegu + self.pielgrzymi_pozostali
        self.wszyscy_pielg_zwykli = self.pielgrzymi_bez_noclegu + self.pielgrzymi_pozostali


    def funkcyjny(self):
        # dane funkcyjnego: id, funkcja, płeć, ostatni nocleg, priorytet
        for id_p, dane_p in self.dane.items():
            if dane_p[2] == "funkcyjni":
                self.id_pielgrzyma = id_p
                self.funkcja_pielgrzyma = dane_p[3]
                self.plec = dane_p[5]
                self.data_nocl = dane_p[4]
                dane_funkcyjnego = [self.id_pielgrzyma, self.funkcja_pielgrzyma, self.plec, self.data_nocl]
                if self.funkcja_pielgrzyma == "porządkowy" or self.funkcja_pielgrzyma == "chorąży":
                    self.funkcyjni_0.append(dane_funkcyjnego)
                elif self.funkcja_pielgrzyma == "szef" or self.funkcja_pielgrzyma == "pilot" \
                        or self.funkcja_pielgrzyma == "przewodnik" or self.funkcja_pielgrzyma == "lider_kwaterm_jutro":
                    self.funkcyjni_1.append(dane_funkcyjnego)
                elif self.funkcja_pielgrzyma == "kwatermistrz_dzis":
                    self.funkcyjni_szkola.append(dane_funkcyjnego)
                else:
                    self.funkcyjni_2.append(dane_funkcyjnego)

    def podaj_func(self):
        print("DANE FUNKCYJNEGO: id, funkcja, płeć, ostatni nocleg, priorytet\n")
        print(f"funkcyjni z grupy 0: {self.funkcyjni_0}")
        print(f"funkcyjni z grupy 1: {self.funkcyjni_1}")
        print(f"funkcyjni z grupy 2: {self.funkcyjni_2}")
        print(f"funkcyjni z grupy do szkoły: {self.funkcyjni_szkola}")

    def zwykly_pielgrzym(self):
        # dane pielgrzyma: id, nr grupki, płeć, ostatni nocleg, priorytet
        for id_p, dane_p in self.dane.items():
            if dane_p[2] != "funkcyjni":
                self.id_pielgrzyma = id_p
                self.grupka_pielgrzyma = dane_p[2]
                self.plec = dane_p[5]
                self.data_nocl = dane_p[4]
                dane_zwyk_pielgrzyma = [self.id_pielgrzyma, self.grupka_pielgrzyma, self.plec, self.data_nocl]
                if 0 > 2:                       # TODO: napisać warunek dla: sa_bez_noclegu >= 3 dni
                    self.pielgrzymi_bez_noclegu.append(dane_zwyk_pielgrzyma)
                else:
                    self.pielgrzymi_pozostali.append(dane_zwyk_pielgrzyma)

    def podaj_zwyk_pielg(self):
        print("DANE PIELGRZYMA: id, nr grupki, płeć, ostatni nocleg, priorytet\n")
        print(f"Pielgrzymi, bez noclegu od 3 dni: {self.pielgrzymi_bez_noclegu}")
        print(f"Pozostali pielgrzymi: {self.pielgrzymi_pozostali}")

    def priorytet_plec(self, grupa, priorytet):
        for el in grupa:
            self.priorytet = priorytet
            if el[2] == "mężczyzna":
                self.priorytet *= 1.5
            el.append(self.priorytet)

    def funkcja_priorytet(self):
        self.priorytet_plec(self.funkcyjni_0, 0)
        self.priorytet_plec(self.funkcyjni_1, 1)
        self.priorytet_plec(self.funkcyjni_2, 4)
        self.priorytet_plec(self.funkcyjni_szkola, 20)

    def zwykly_pielg_priorytet(self):
        # if self.nocleg_jak_dawno >= 3:
        #     self.priorytet_plec(self.pielgrzymi_bez_noclegu, 2)
        #     # self.priorytet = 2
        # else:
            self.priorytet_plec(self.pielgrzymi_pozostali, 7)
            # self.priorytet = 7

    def suma_osob_w_grupie(self, grupa, nazwa):
        il_kobiet = 0
        il_mezczyzn = 0
        for el in grupa:
            if el[2] == "kobieta":
                il_kobiet += 1
            else:
                il_mezczyzn += 1
        # if grupa[2] == "kobieta":
        #     il_kobiet += 1
        # else:
        #     il_mezczyzn += 1
        print(f" Grupa '{nazwa}' >>  k: {il_kobiet}, m: {il_mezczyzn}")

    def podsum_wszyst_plcie(self):
        self.suma_osob_w_grupie(self.wszyscy_pielgrzymi, "wszyscy_razem")

    def podsum_il_w_grupach(self):
        self.suma_osob_w_grupie(self.funkcyjni_0, "funkcyjni_0")
        self.suma_osob_w_grupie(self.funkcyjni_1, "funkcyjni_1")
        self.suma_osob_w_grupie(self.funkcyjni_2, "funkcyjni_2")
        self.suma_osob_w_grupie(self.funkcyjni_szkola, "funkcyjni_szkola")
        self.suma_osob_w_grupie(self.pielgrzymi_bez_noclegu, "pielgrzymi_bez_noclegu")
        self.suma_osob_w_grupie(self.pielgrzymi_pozostali, "pielgrzymi_pozostali")
        # for grupa_os in self.wszyscy_pielgrzymi:
        #     self.suma_osob_w_grupie(grupa_os, f'{grupa_os=}'.split('=')[0])
        #   print(f'{grupa_os=}'.split('=')[0])
        #     print(grupa_os)
        # print(self.wszyscy_pielgrzymi)
        # print(self.funkcyjni_0)

    def podsum_il_wg_prioryt(self):
        # zestawienie priorytetów /priorytet: ilość/
        for el in self.wszyscy_pielgrzymi:
            if not self.suma_priorytetow.get(el[4]):
                self.suma_priorytetow[el[4]] = 0
            self.suma_priorytetow[el[4]] += 1
        print(self.suma_priorytetow)
        print(sorted(self.suma_priorytetow.items()))

    # obliczanie ilości dni od ostatniego noclegu dla wszystkich z danej grupy na raz
    def delta_ostatni_nocleg(self):
        today = datetime.now().date()
        for el in self.wszyscy_pielg_zwykli:
            last_accommodation = datetime.strptime(el[3], "%d-%m-%Y").date()
            delta_nocleg_obl = today - last_accommodation
            self.delta_nocleg = delta_nocleg_obl.days
            print(self.delta_nocleg)


    def borderer(func):             # TODO: jak zrobić dekorator wewnątrz klasy?
        print("------------------")
        func()


pielg = Pielgrzymi("pielgrzymi.json")
# print("----------------------------------------")
# pielg.podaj_func()
# print("----------------------------------------")
# pielg.podaj_zwyk_pielg()
# print("----------------------------------------")
# # print()
# print("PODSUMOWANIE LICZEBNOŚCI GRUP")
# pielg.podsum_wszyst_plcie()
# print()
# pielg.podsum_il_w_grupach()
# print()
# print("zestawienie priorytetów [priorytet: ilość]")
# pielg.podsum_il_wg_prioryt()

pielg.delta_ostatni_nocleg()


