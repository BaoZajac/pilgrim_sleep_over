from main import read_file
import datetime
from datetime import datetime


class Pilgrims:
    def __init__(self, file_path_pilgrims):
        self.data_pilgrims = read_file(file_path_pilgrims)
        self.role_0 = []
        self.role_1 = []
        self.role_2 = []
        self.role_school = []
        self.pilgrims_no_accommod = []
        self.pilgrims_other = []
        self.sum_priority = {}

        self.role()
        self.normal_pilgrim()
        self.role_priority()
        self.normal_pilgr_priority()

        self.all_pilgrims = self.role_0 + self.role_1 + self.role_2 + self.role_school + self.pilgrims_no_accommod \
                            + self.pilgrims_other
        self.all_pilgrims_normal = self.pilgrims_no_accommod + self.pilgrims_other

    def role(self):
        # role_person data: id, role, sex, last accommodation, priority
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

    def give_role(self):
        print("DANE FUNKCYJNEGO: id, funkcja, płeć, ostatni nocleg, priorytet\n")
        print(f"funkcyjni z grupy 0: {self.role_0}")
        print(f"funkcyjni z grupy 1: {self.role_1}")
        print(f"funkcyjni z grupy 2: {self.role_2}")
        print(f"funkcyjni z grupy do szkoły: {self.role_school}")

    def normal_pilgrim(self):
        # pilgrim data: id, no. of a small group, sex, last accommodation, priority
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
                self.from_last_accommod(data_nocl)
                if self.delta_nocleg >= 3:
                    self.pilgrims_no_accommod.append(dane_zwyk_pielgrzyma)
                else:
                    self.pilgrims_other.append(dane_zwyk_pielgrzyma)

    def give_normal_pilgr(self):
        print("DANE PIELGRZYMA: id, nr grupki, płeć, ostatni nocleg, priorytet\n")
        print(f"Pielgrzymi, bez noclegu od 3 dni: {self.pilgrims_no_accommod}")
        print(f"Pozostali pielgrzymi: {self.pilgrims_other}")

    def priority_sex(self, grupa, priorytet):
        for el in grupa:
            self.priorytet = priorytet
            if el[2] == "mężczyzna":
                # self.priorytet *= 1.5
                self.priorytet += 1
            el.append(self.priorytet)
        return grupa

    def role_priority(self):
        self.priority_sex(self.role_0, 0)
        self.priority_sex(self.role_1, 2)
        self.priority_sex(self.role_2, 6)
        self.priority_sex(self.role_school, 20)

    def normal_pilgr_priority(self):
        self.priority_sex(self.pilgrims_no_accommod, 4)
        self.priority_sex(self.pilgrims_other, 8)

    def sum_ppl_in_group(self, grupa, nazwa):
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

    def summary_number_in_groups(self):
        self.sum_ppl_in_group(self.role_0, "funkcyjni_0")
        self.sum_ppl_in_group(self.role_1, "funkcyjni_1")
        self.sum_ppl_in_group(self.role_2, "funkcyjni_2")
        self.sum_ppl_in_group(self.role_school, "funkcyjni_szkola")
        self.sum_ppl_in_group(self.pilgrims_no_accommod, "pielgrzymi_bez_noclegu")
        self.sum_ppl_in_group(self.pilgrims_other, "pielgrzymi_pozostali")

    def summary_number_in_small_groups(self):
        print(self.podzial_grupki.items())
        for k, v in self.podzial_grupki.items():
            a = self.sum_ppl_in_group(v, k)
        return a

    def summary_number_sex(self):
        # self.sum_ppl_in_group(self.all_pilgrims, "wszyscy_razem")
        return self.sum_ppl_in_group(self.all_pilgrims, "wszyscy_razem")

    def summary_number_priority(self):
        # catalog of priorities /priority: amount/
        for el in self.all_pilgrims:
            if not self.sum_priority.get(el[4]):
                self.sum_priority[el[4]] = 0
            self.sum_priority[el[4]] += 1
        return self.sum_priority

    # count no. of days from the last accommodation
    def from_last_accommod(self, data):
        dzis = datetime.now().date()
        ostatni_nocleg = datetime.strptime(data, "%d-%m-%Y").date()
        delta_nocleg_obl = dzis - ostatni_nocleg
        self.delta_nocleg = delta_nocleg_obl.days


pilg = Pilgrims("pilgrims.json")


