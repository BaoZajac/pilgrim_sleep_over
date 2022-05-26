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
        self.znajdz_funkcje()
        self.funkcja_priorytet()

    def znajdz_funkcje(self):
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

    def funkcja_priorytet(self):
        self.priorytet_plec(self.funkcyjni_0, 0)
        self.priorytet_plec(self.funkcyjni_1, 1)
        self.priorytet_plec(self.funkcyjni_2, 4)
        self.priorytet_plec(self.funkcyjni_szkola, 20)

    def priorytet_plec(self, grupa, priorytet):
        for el in grupa:
            self.priorytet = priorytet
            if el[2] == "mężczyzna":
                self.priorytet *= 1.5
            el.append(self.priorytet)


# Pielgrzymi("pielgrzymi.json").znajdz_funkcje()
# Pielgrzymi("pielgrzymi.json").funkcja_priorytet()

# Pielgrzymi("pielgrzymi.json")
# Pielgrzymi("pielgrzymi.json").podaj_func()
# Pielgrzymi("pielgrzymi.json").funkcja_priorytet()
Pielgrzymi("pielgrzymi.json").podaj_func()
