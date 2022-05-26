from main import read_db


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
        self.funkcyjny()
        self.zwykly_pielgrzym()
        self.funkcja_priorytet()
        self.zwykly_pielg_priorytet()

    def funkcyjny(self):
        # dane funkcyjnego: id, funkcja, płeć, priorytet
        for id_p, dane_p in self.dane.items():
            if dane_p[2] == "funkcyjni":
                self.id_pielgrzyma = id_p
                self.funkcja_pielgrzyma = dane_p[3]
                self.plec = dane_p[5]
                dane_funkcyjnego = [self.id_pielgrzyma, self.funkcja_pielgrzyma, self.plec]
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
        print(f"funkcyjni z grupy 0: {self.funkcyjni_0}")
        print(f"funkcyjni z grupy 1: {self.funkcyjni_1}")
        print(f"funkcyjni z grupy 2: {self.funkcyjni_2}")
        print(f"funkcyjni z grupy do szkoły: {self.funkcyjni_szkola}")

    def zwykly_pielgrzym(self):
        # dane pielgrzyma: id, nr grupki, płeć, priorytet
        for id_p, dane_p in self.dane.items():
            if dane_p[2] != "funkcyjni":
                self.id_pielgrzyma = id_p
                self.grupka_pielgrzyma = dane_p[2]
                self.plec = dane_p[5]
                dane_zwyk_pielgrzyma = [self.id_pielgrzyma, self.grupka_pielgrzyma, self.plec]
                if 0 > 2:                       # TODO: napisać warunek dla: sa_bez_noclegu >= 3 dni
                    self.pielgrzymi_bez_noclegu.append(dane_zwyk_pielgrzyma)
                else:
                    self.pielgrzymi_pozostali.append(dane_zwyk_pielgrzyma)

    def podaj_zwyk_pielg(self):
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
        print(f"Ilość kobiet w grupie <{nazwa}> to: {il_kobiet} | priorytet: {self.priorytet}")
        print(f"Ilość mężczyzn w grupie <{nazwa}> to: {il_mezczyzn} | priorytet: {self.priorytet}")

    def podsum_il_w_grupach(self):
        self.suma_osob_w_grupie(self.funkcyjni_0, "funkcyjni_0")
        self.suma_osob_w_grupie(self.funkcyjni_1, "funkcyjni_1")
        self.suma_osob_w_grupie(self.funkcyjni_2, "funkcyjni_2")
        self.suma_osob_w_grupie(self.funkcyjni_szkola, "funkcyjni_szkola")
        self.suma_osob_w_grupie(self.pielgrzymi_bez_noclegu, "pielgrzymi_bez_noclegu")
        self.suma_osob_w_grupie(self.pielgrzymi_pozostali, "pielgrzymi_pozostali")



# Pielgrzymi("pielgrzymi.json").funkcyjny()
# Pielgrzymi("pielgrzymi.json").funkcja_priorytet()

# Pielgrzymi("pielgrzymi.json")
Pielgrzymi("pielgrzymi.json").podaj_func()
Pielgrzymi("pielgrzymi.json").podaj_zwyk_pielg()
print()
Pielgrzymi("pielgrzymi.json").podsum_il_w_grupach()
