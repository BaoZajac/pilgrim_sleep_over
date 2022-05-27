from main import read_db
from uczestnicy import Pielgrzymi
import datetime


class Noclegi(Pielgrzymi):
    def __init__(self, file_path_noclegi):
        super().__init__("pielgrzymi.json")         # TODO: zrobić możliwość wyboru pliku z klasy Pielgrzymi
        self.dane_noclegi = read_db(file_path_noclegi)
        self.noclegi_rudawa = []
        self.noclegi_olkusz = []
        self.noclegi_niegowonice = []
        self.noclegi_myszkow = []
        self.noclegi_poraj = []
        self.noclegi_nierada = []

        self.il_domow_z_noclegiem = 0
        self.il_domow_z_prysznicem = 0
        self.il_noclegow = 0
        self.il_prysznicow = 0
        self.dane_o_noclegach = self.dane_noclegi.values()

    def miejscowosc_na_data(self):
        for id_n, dane_n in self.dane_noclegi.items():
            miejscowosc = dane_n[2]
            if miejscowosc == "Rudawa":
                self.data_noclegu = datetime.datetime(2022, 8, 3).date()
            elif miejscowosc == "Olkusz":
                self.data_noclegu = datetime.datetime(2022, 8, 4).date()
            elif miejscowosc == "Niegowonice":
                self.data_noclegu = datetime.datetime(2022, 8, 5).date()
            elif miejscowosc == "Myszków":
                self.data_noclegu = datetime.datetime(2022, 8, 6).date()
            elif miejscowosc == "Poraj":
                self.data_noclegu = datetime.datetime(2022, 8, 7).date()
            elif miejscowosc == "Nierada":
                self.data_noclegu = datetime.datetime(2022, 8, 8).date()
            # print(miejscowosc, self.data_noclegu)

    def lista_nocl_miejscow(self):
        for id_n, dane_n in self.dane_noclegi.items():
            # print(dane_n)
            miejscowosc = dane_n[2]
            id_nocleg = id_n
            # nazwisko = dane_n[0]
            # imie = dane_n[1]
            # dane_n = nazwisko, imie, miejscowosc, ulica, dom, mieszkanie, tel, nocleg, prysznic, komentarz
            # TODO: czy da się zrobić uniwersalne jak poniżej, tylko jak przekazać to town w nazwie zmiennej
            """ [town przekazane w atrybucie(?) metody]    albo ta sama idea co poniżej, ale wykorzystana w for
                if miejscowosc == town:
                self.noclegi_{{town}}.append("tekst")
                print(self.noclegi_rudawa)"""
            if miejscowosc == "Rudawa":
                self.noclegi_rudawa.append(list(id_nocleg) + dane_n)
            elif miejscowosc == "Olkusz":
                self.noclegi_olkusz.append(list(id_nocleg) + dane_n)
            elif miejscowosc == "Niegowonice":
                self.noclegi_niegowonice.append(list(id_nocleg) + dane_n)
            elif miejscowosc == "Myszków":
                self.noclegi_myszkow.append(list(id_nocleg) + dane_n)
            elif miejscowosc == "Poraj":
                self.noclegi_poraj.append(list(id_nocleg) + dane_n)
            elif miejscowosc == "Nierada":
                self.noclegi_nierada.append(list(id_nocleg) + dane_n)
        print("Rudawa", self.noclegi_rudawa)
        print("Olkusz", self.noclegi_olkusz)
        print("Niegowonice", self.noclegi_niegowonice)
        print("Myszków", self.noclegi_myszkow)
        print("Poraj", self.noclegi_poraj)
        print("Nierada", self.noclegi_nierada)





    # def il_noclegow_na_dany_dzien(self, date):
    #     for el in self.dane_o_noclegach:
    #         self.il_noclegow += int(el[7])
    #         self.il_domow_z_noclegiem += 1
    #     return self.il_noclegow, self.il_domow_z_noclegiem
    #
    # def il_prysznicow_na_dany_dzien(self, date):
    #     for el in self.dane_o_noclegach:
    #         self.il_prysznicow += int(el[8])
    #         self.il_domow_z_prysznicem += 1
    #     return self.il_prysznicow, self.il_domow_z_prysznicem
    #
    # def przyznawanie_noclegow(self):
    #     if self.il_noclegow < self.grupaA:
    #         ...
    #
    # def zapisz_noclegi(self):
    #     ...


noclegi = Noclegi("noclegi.json")
# noclegi.miejscowosc_na_data()
noclegi.lista_nocl_miejscow()
