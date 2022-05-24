import json


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

    def funkcyjni(self):
        if ...:
            ...


class Noclegi(Pielgrzymi):
    def __init__(self, file_path_noclegi):
        super().__init__("pielgrzymi.json")      # TODO: czy to tak ma być?
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


a = Noclegi("noclegi.json").il_noclegow_na_dany_dzien(1)
print(a)
