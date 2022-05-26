import json
import datetime
from datetime import datetime


def read_db(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def write_db(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)


class Pielgrzymi:
    def __init__(self, file_path_pielgrzymi):
        self.data_pielgrzymi = read_db(file_path_pielgrzymi)
        self.lista_funkcji = ["bagażowy", "chorąży", "ekologiczny", "kwatermistrz_dzis", "kwatermistrz_jutro",
                              "lider_kwaterm_jutro", "medyczny", "pilot", "porządkowy", "przewodnik", "schola", "szef",
                              "techniczny"]
        self.dane_o_pielgrzymie = self.data_pielgrzymi.values()

    def priorytet_funkcyjni(self):
        for funkcja in self.lista_funkcji:
            if funkcja == "porządkowy":
                priorytet = 0
            elif funkcja == "szef" or funkcja == "pilot" or funkcja == "przewodnik" or funkcja == "chorąży" \
                    or funkcja == "lider_kwaterm_jutro":
                priorytet = 1
            elif funkcja == "kwatermistrz_dzis":
                priorytet = 20
            else:
                priorytet = 4

    def priorytet_pielgrzym(self):
        if self.ostatni_nocleg >= 3:
            priorytet = 2
        else:
            priorytet = 7

    def ostatni_nocleg(self):
        today = datetime.now().date()
        for el in self.dane_o_pielgrzymie:
            last_accommodation = datetime.strptime(el[4], "%d-%m-%Y").date()
            self.nocleg_jak_dawno = today - last_accommodation
            print(self.nocleg_jak_dawno)
            # d1 = date(2022, 8, 3)
            # roznica = d1 - self.last_accommodation
            # print(roznica)
        return self.nocleg_jak_dawno


class Noclegi(Pielgrzymi):
    def __init__(self, file_path_noclegi):
        super().__init__("pielgrzymi.json")
        self.data_noclegi = read_db(file_path_noclegi)
        self.il_domow_z_noclegiem = 0
        self.il_domow_z_prysznicem = 0
        self.il_noclegow = 0
        self.il_prysznicow = 0
        self.dane_o_noclegach = self.data_noclegi.values()

    def il_noclegow_na_dany_dzien(self, date):
        for el in self.dane_o_noclegach:
            self.il_noclegow += int(el[7])
            self.il_domow_z_noclegiem += 1
        return self.il_noclegow, self.il_domow_z_noclegiem

    def il_prysznicow_na_dany_dzien(self, date):
        for el in self.dane_o_noclegach:
            self.il_prysznicow += int(el[8])
            self.il_domow_z_prysznicem += 1
        return self.il_prysznicow, self.il_domow_z_prysznicem

    def przyznawanie_noclegow(self):

        if self.il_noclegow < self.grupaA:
            ...


# a = Noclegi("noclegi.json").il_noclegow_na_dany_dzien(1)
# print(a)

# Pielgrzymi("pielgrzymi.json").ostatni_nocleg()



