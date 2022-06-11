from main import read_file
import datetime
from datetime import datetime


class Pielgrzymi:
    def __init__(self, file_path_pielgrzymi):
        self.dane_pielgrzymi = read_file(file_path_pielgrzymi)
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

        # print(self.wszyscy_pielgrzymi)

    def funkcyjny(self):
        # dane funkcyjnego: id, funkcja, płeć, ostatni nocleg, priorytet
        self.lista_funkcyjnych = []
        for id_p, dane_p in self.dane_pielgrzymi.items():
            if dane_p[2] == "funkcyjni":    # TODO: wykasować self?
                id_pielgrzyma = id_p
                funkcja_pielgrzyma = dane_p[3]
                plec = dane_p[5]
                data_nocl = dane_p[4]
                nazwisko = dane_p[0]
                imie = dane_p[1]
                dane_funkcyjnego = [id_pielgrzyma, funkcja_pielgrzyma, plec, data_nocl, nazwisko, imie]
                self.lista_funkcyjnych.append(dane_funkcyjnego)
                if funkcja_pielgrzyma == "porządkowy" or funkcja_pielgrzyma == "chorąży":
                    self.funkcyjni_0.append(dane_funkcyjnego)
                elif funkcja_pielgrzyma == "szef" or funkcja_pielgrzyma == "pilot" \
                        or funkcja_pielgrzyma == "przewodnik" or funkcja_pielgrzyma == "lider_kwaterm_jutro":
                    self.funkcyjni_1.append(dane_funkcyjnego)
                elif funkcja_pielgrzyma == "kwatermistrz_dzis":
                    self.funkcyjni_szkola.append(dane_funkcyjnego)
                else:
                    self.funkcyjni_2.append(dane_funkcyjnego)
        # print("FUNKCYJNI: ", self.lista_funkcyjnych)
        # return self.lista_funkcyjnych

    def podaj_funkc(self):
        print("DANE FUNKCYJNEGO: id, funkcja, płeć, ostatni nocleg, priorytet\n")
        print(f"funkcyjni z grupy 0: {self.funkcyjni_0}")
        print(f"funkcyjni z grupy 1: {self.funkcyjni_1}")
        print(f"funkcyjni z grupy 2: {self.funkcyjni_2}")
        print(f"funkcyjni z grupy do szkoły: {self.funkcyjni_szkola}")

    def zwykly_pielgrzym(self):
        # dane pielgrzyma: id, nr grupki, płeć, ostatni nocleg, priorytet
        self.podzial_grupki = {}
        self.lista_pozost_pielg = []
        for id_p, dane_p in self.dane_pielgrzymi.items():
            if dane_p[3] != "funkcyjni":  # * dane_p[2]
                id_pielgrzyma = id_p
                grupka_pielgrzyma = dane_p[3]  # * dane_p[2]
                plec = dane_p[2]  # * dane_p[5]
                data_nocl = dane_p[5]   # * dane_p[4]
                nazwisko = dane_p[0]
                imie = dane_p[1]
                dane_zwyk_pielgrzyma = [id_pielgrzyma, grupka_pielgrzyma, plec, data_nocl, nazwisko, imie]
                self.lista_pozost_pielg.append(dane_zwyk_pielgrzyma)
                if not grupka_pielgrzyma in self.podzial_grupki.keys():
                    self.podzial_grupki[grupka_pielgrzyma] = [dane_zwyk_pielgrzyma]
                else:
                    self.podzial_grupki[grupka_pielgrzyma].append(dane_zwyk_pielgrzyma)
                self.delta_ostatni_nocleg(data_nocl)
                if self.delta_nocleg >= 3:
                    self.pielgrzymi_bez_noclegu.append(dane_zwyk_pielgrzyma)
                else:
                    self.pielgrzymi_pozostali.append(dane_zwyk_pielgrzyma)
        # print("LISTAPIELG: ", self.lista_pozost_pielg)
        # print("PODZIAŁ GRUPKI: ", self.podzial_grupki)

    def podaj_zwyk_pielg(self):
        print("DANE PIELGRZYMA: id, nr grupki, płeć, ostatni nocleg, priorytet\n")
        print(f"Pielgrzymi, bez noclegu od 3 dni: {self.pielgrzymi_bez_noclegu}")
        print(f"Pozostali pielgrzymi: {self.pielgrzymi_pozostali}")

    def priorytet_plec(self, grupa, priorytet):
        for el in grupa:
            self.priorytet = priorytet
            if el[2] == "mężczyzna":
                # self.priorytet *= 1.5
                self.priorytet += 1
            el.append(self.priorytet)

    def funkcja_priorytet(self):
        self.priorytet_plec(self.funkcyjni_0, 0)
        self.priorytet_plec(self.funkcyjni_1, 2)
        self.priorytet_plec(self.funkcyjni_2, 6)
        self.priorytet_plec(self.funkcyjni_szkola, 20)

    def zwykly_pielg_priorytet(self):
        self.priorytet_plec(self.pielgrzymi_bez_noclegu, 4)
        self.priorytet_plec(self.pielgrzymi_pozostali, 8)

    def suma_osob_w_grupie(self, grupa, nazwa):
        il_kobiet = 0
        il_mezczyzn = 0
        for el in grupa:
            if el[2] == "kobieta":
                il_kobiet += 1
            else:
                il_mezczyzn += 1
        wszyscy = il_kobiet + il_mezczyzn
        # print(f" Grupa '{nazwa}' >>  razem: {wszyscy}, k: {il_kobiet}, m: {il_mezczyzn}")
        return nazwa, wszyscy, il_kobiet, il_mezczyzn

    def podsum_il_w_grupach(self):
        self.suma_osob_w_grupie(self.funkcyjni_0, "funkcyjni_0")
        self.suma_osob_w_grupie(self.funkcyjni_1, "funkcyjni_1")
        self.suma_osob_w_grupie(self.funkcyjni_2, "funkcyjni_2")
        self.suma_osob_w_grupie(self.funkcyjni_szkola, "funkcyjni_szkola")
        self.suma_osob_w_grupie(self.pielgrzymi_bez_noclegu, "pielgrzymi_bez_noclegu")
        self.suma_osob_w_grupie(self.pielgrzymi_pozostali, "pielgrzymi_pozostali")

    def podsum_il_w_grupkach(self):
        print(self.podzial_grupki.items())
        for k, v in self.podzial_grupki.items():
            a = self.suma_osob_w_grupie(v, k)
            # print(a)
        #     print(1, a)
        # print(2, a)
        return a

    def podsum_il_wg_plci(self):
        # self.suma_osob_w_grupie(self.wszyscy_pielgrzymi, "wszyscy_razem")
        return self.suma_osob_w_grupie(self.wszyscy_pielgrzymi, "wszyscy_razem")

    def podsum_il_wg_prioryt(self):
        # zestawienie priorytetów /priorytet: ilość/
        for el in self.wszyscy_pielgrzymi:
            if not self.suma_priorytetow.get(el[4]):
                self.suma_priorytetow[el[4]] = 0
            self.suma_priorytetow[el[4]] += 1
        # print(self.suma_priorytetow)
        # print(sorted(self.suma_priorytetow.items()))
        return self.suma_priorytetow


    # obliczanie ilości dni od ostatniego noclegu
    def delta_ostatni_nocleg(self, data):
        dzis = datetime.now().date()
        ostatni_nocleg = datetime.strptime(data, "%d-%m-%Y").date()
        delta_nocleg_obl = dzis - ostatni_nocleg
        self.delta_nocleg = delta_nocleg_obl.days

    # def borderer(func):             # TODO: jak zrobić dekorator wewnątrz klasy?
    #     print("------------------")
    #     func()


pielg = Pielgrzymi("pielgrzymi.json")
# print("----------------------------------------")
# pielg.podaj_funkc()
# print("----------------------------------------")
# pielg.podaj_zwyk_pielg()
# print("----------------------------------------")
# # print()
# print("PODSUMOWANIE LICZEBNOŚCI GRUP")
# pielg.podsum_il_wg_plci()
# print()
# pielg.podsum_il_w_grupach()
# print()
# print("zestawienie priorytetów [priorytet: ilość]")
# pielg.podsum_il_wg_prioryt()

# pielg.delta_ostatni_nocleg()
# pielg.podsum_il_w_grupkach()


