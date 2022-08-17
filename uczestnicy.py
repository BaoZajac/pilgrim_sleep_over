from main import read_file
import datetime
from datetime import datetime


class Pielgrzymi:
    def __init__(self, file_path_pilgrims):
        self.data_pilgrims = read_file(file_path_pilgrims)
        self.role_0 = []
        self.role_1 = []
        self.role_2 = []
        self.role_school = []
        self.pilgrims_no_accommod = []
        self.pilgrims_other = []
        self.sum_priority = {}

        self.funkcyjny()
        self.zwykly_pielgrzym()
        self.funkcja_priorytet()
        self.zwykly_pielg_priorytet()

        self.all_pilgrims = self.role_0 + self.role_1 + self.role_2 + self.role_school + self.pilgrims_no_accommod \
                            + self.pilgrims_other
        self.all_pilgrims_normal = self.pilgrims_no_accommod + self.pilgrims_other


    def funkcyjny(self):
        # dane funkcyjnego: id, funkcja, płeć, ostatni nocleg, priorytet
        self.lista_funkcyjnych = []
        for id_p, dane_p in self.data_pilgrims.items():
            if dane_p[3] == "funkcyjni":
                id_pielgrzyma = id_p
                funkcja_pielgrzyma = dane_p[4]
                plec = dane_p[2]
                data_nocl = dane_p[5]
                nazwisko = dane_p[0]
                imie = dane_p[1]
                dane_funkcyjnego = [id_pielgrzyma, funkcja_pielgrzyma, plec, data_nocl, nazwisko, imie]
                self.lista_funkcyjnych.append(dane_funkcyjnego)
                if funkcja_pielgrzyma == "porządkowy" or funkcja_pielgrzyma == "chorąży":
                    self.role_0.append(dane_funkcyjnego)
                elif funkcja_pielgrzyma == "szef" or funkcja_pielgrzyma == "pilot" \
                        or funkcja_pielgrzyma == "przewodnik" or funkcja_pielgrzyma == "lider_kwaterm_jutro":
                    self.role_1.append(dane_funkcyjnego)
                elif funkcja_pielgrzyma == "kwatermistrz_dzis":
                    self.role_school.append(dane_funkcyjnego)
                else:
                    self.role_2.append(dane_funkcyjnego)

    def podaj_funkc(self):
        print("DANE FUNKCYJNEGO: id, funkcja, płeć, ostatni nocleg, priorytet\n")
        print(f"funkcyjni z grupy 0: {self.role_0}")
        print(f"funkcyjni z grupy 1: {self.role_1}")
        print(f"funkcyjni z grupy 2: {self.role_2}")
        print(f"funkcyjni z grupy do szkoły: {self.role_school}")

    def zwykly_pielgrzym(self):
        # dane pielgrzyma: id, nr grupki, płeć, ostatni nocleg, priorytet
        self.podzial_grupki = {}
        self.lista_pozost_pielg = []
        for id_p, dane_p in self.data_pilgrims.items():
            if dane_p[3] != "funkcyjni":
                id_pielgrzyma = id_p
                grupka_pielgrzyma = dane_p[3]
                plec = dane_p[2]
                data_nocl = dane_p[5]
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
                    self.pilgrims_no_accommod.append(dane_zwyk_pielgrzyma)
                else:
                    self.pilgrims_other.append(dane_zwyk_pielgrzyma)

    def podaj_zwyk_pielg(self):
        print("DANE PIELGRZYMA: id, nr grupki, płeć, ostatni nocleg, priorytet\n")
        print(f"Pielgrzymi, bez noclegu od 3 dni: {self.pilgrims_no_accommod}")
        print(f"Pozostali pielgrzymi: {self.pilgrims_other}")

    def priorytet_plec(self, grupa, priorytet):
        for el in grupa:
            self.priorytet = priorytet
            if el[2] == "mężczyzna":
                # self.priorytet *= 1.5
                self.priorytet += 1
            el.append(self.priorytet)
        return grupa

    def funkcja_priorytet(self):
        self.priorytet_plec(self.role_0, 0)
        self.priorytet_plec(self.role_1, 2)
        self.priorytet_plec(self.role_2, 6)
        self.priorytet_plec(self.role_school, 20)

    def zwykly_pielg_priorytet(self):
        self.priorytet_plec(self.pilgrims_no_accommod, 4)
        self.priorytet_plec(self.pilgrims_other, 8)

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
        self.suma_osob_w_grupie(self.role_0, "funkcyjni_0")
        self.suma_osob_w_grupie(self.role_1, "funkcyjni_1")
        self.suma_osob_w_grupie(self.role_2, "funkcyjni_2")
        self.suma_osob_w_grupie(self.role_school, "funkcyjni_szkola")
        self.suma_osob_w_grupie(self.pilgrims_no_accommod, "pielgrzymi_bez_noclegu")
        self.suma_osob_w_grupie(self.pilgrims_other, "pielgrzymi_pozostali")

    def podsum_il_w_grupkach(self):
        print(self.podzial_grupki.items())
        for k, v in self.podzial_grupki.items():
            a = self.suma_osob_w_grupie(v, k)
        return a

    def podsum_il_wg_plci(self):
        # self.suma_osob_w_grupie(self.all_pilgrims, "wszyscy_razem")
        return self.suma_osob_w_grupie(self.all_pilgrims, "wszyscy_razem")

    def podsum_il_wg_prioryt(self):
        # zestawienie priorytetów /priorytet: ilość/
        for el in self.all_pilgrims:
            if not self.sum_priority.get(el[4]):
                self.sum_priority[el[4]] = 0
            self.sum_priority[el[4]] += 1
        return self.sum_priority

    # obliczanie ilości dni od ostatniego noclegu
    def delta_ostatni_nocleg(self, data):
        dzis = datetime.now().date()
        ostatni_nocleg = datetime.strptime(data, "%d-%m-%Y").date()
        delta_nocleg_obl = dzis - ostatni_nocleg
        self.delta_nocleg = delta_nocleg_obl.days


pielg = Pielgrzymi("pilgrims.json")


