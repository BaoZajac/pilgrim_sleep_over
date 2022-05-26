from main import read_db


class Pielgrzymi:
    def __init__(self, file_path_pielgrzymi):
        self.dane = read_db(file_path_pielgrzymi)
        self.id_pielgrzyma = None
        self.funkcja_pielgrzyma = None
        self.funkcyjni_0 = []
        self.funkcyjni_1 = []
        self.funkcyjni_2 = []
        self.funkcyjni_szkola = []
        self.znajdz_funkcje()

    def znajdz_funkcje(self):
        for id_p, dane_p in self.dane.items():
            self.id_pielgrzyma = id_p
            if dane_p[2] == "funkcyjni":
                self.funkcja_pielgrzyma = dane_p[3]
                if self.funkcja_pielgrzyma == "porządkowy" or self.funkcja_pielgrzyma == "chorąży":
                    self.funkcyjni_0.append((self.id_pielgrzyma, self.funkcja_pielgrzyma))
                elif self.funkcja_pielgrzyma == "szef" or self.funkcja_pielgrzyma == "pilot" \
                        or self.funkcja_pielgrzyma == "przewodnik" or self.funkcja_pielgrzyma == "lider_kwaterm_jutro":
                    self.funkcyjni_1.append((self.id_pielgrzyma, self.funkcja_pielgrzyma))
                elif self.funkcja_pielgrzyma == "kwatermistrz_dzis":
                    self.funkcyjni_szkola.append((self.id_pielgrzyma, self.funkcja_pielgrzyma))
                else:
                    self.funkcyjni_2.append((self.id_pielgrzyma, self.funkcja_pielgrzyma))

    def podaj_func(self):
        print(f"funkcyjni z grupy 0: {self.funkcyjni_0}")
        print(f"funkcyjni z grupy 1: {self.funkcyjni_1}")
        print(f"funkcyjni z grupy 2: {self.funkcyjni_2}")
        print(f"funkcyjni z grupy do szkoły: {self.funkcyjni_szkola}")

    def funkcja_priorytet(self):
        # print(self.funkcja_pielgrzyma)
        self.znajdz_funkcje()
        print(self.funkcja_pielgrzyma)
        # if self.funkcja_pielgrzyma == "chorąży":
        #     print("yes")


# Pielgrzymi("pielgrzymi.json").znajdz_funkcje()
# Pielgrzymi("pielgrzymi.json").funkcja_priorytet()

Pielgrzymi("pielgrzymi.json").podaj_func()
# Pielgrzymi("pielgrzymi.json")