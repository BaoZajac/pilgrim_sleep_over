from main import read_file
from uczestnicy import Pielgrzymi
import datetime
# from datetime import datetime


class Noclegi(Pielgrzymi):
    def __init__(self, file_path_noclegi):
        super().__init__("pielgrzymi.json")         # TODO: zrobić możliwość wyboru pliku z klasy Pielgrzymi
        self.dane_noclegi = read_file(file_path_noclegi)
        self.noclegi_wszystkie = {}
        self.lista_data = []
        self.wczytaj_dane()


        self.noclegi_rudawa = []
        self.noclegi_olkusz = []
        self.noclegi_niegowonice = []
        self.noclegi_myszkow = []
        self.noclegi_poraj = []
        self.noclegi_nierada = []
        # self.miejscowosc_na_data()

        self.il_domow_z_noclegiem = 0
        self.il_domow_z_prysznicem = 0
        self.il_noclegow = 0
        self.il_prysznicow = 0
        # self.dane_o_noclegach = self.dane_noclegi.values()

    # wczytaj dane z pliku do słownika
    def wczytaj_dane(self):
        for id_n, dane_n in self.dane_noclegi.items():
            miejscowosc = dane_n[2]
            ulica = dane_n[3]
            dom = dane_n[4]
            mieszkanie = dane_n[5]
            nazwisko = dane_n[0]
            imie = dane_n[1]
            tel = dane_n[6]
            il_noclegow = dane_n[7]
            il_pryszn = dane_n[8]
            komentarz = dane_n[9]
            data = self.miejscowosc_na_data(miejscowosc)
            if not self.noclegi_wszystkie.get(miejscowosc):
                self.noclegi_wszystkie[(id_n, miejscowosc, data)] = []
            self.noclegi_wszystkie[(id_n, miejscowosc, data)] += [[miejscowosc, ulica, dom, mieszkanie, nazwisko, imie,
                                                                   tel, il_noclegow, il_pryszn, komentarz]]
        # print(self.noclegi_wszystkie)

    # odkodowanie daty noclegu z nazwy miejscowości
    def miejscowosc_na_data(self, miejscowosc):
        if miejscowosc == "Rudawa" or miejscowosc == "Radwanowice":
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
        # self.data_noclegu = datetime.strptime(self.data_noclegu, "%d-%m-%Y").date()
        else:
            self.data_noclegu = "x"
        return self.data_noclegu

    # tworzy listę noclegów dla danej daty
    def lista_nocl_data(self, data):
        self.lista_data = []
        for k, v in self.noclegi_wszystkie.items():
            if data == str(k[2]):
                self.lista_data += v
        # print(self.lista_data)
        return self.lista_data

    # podaje il. domów z noclegiem i il. noclegów
    def suma_nocl_data(self, data):
        self.suma_dom_nocleg = 0
        self.suma_nocleg = 0
        for el in self.lista_nocl_data(data):
            il_noclegow = el[7]
            self.suma_dom_nocleg += 1
            self.suma_nocleg += int(il_noclegow)
        print(self.lista_nocl_data(data))
        print(self.suma_dom_nocleg)
        print(self.suma_nocleg)




    # tworzy listę noclegów dla danej miejscowości
    def lista_nocl_miejscow(self):
        for id_n, dane_n in self.dane_noclegi.items():
            # print(dane_n)
            miejscowosc = dane_n[2]
            id_nocleg = id_n
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
        # print("Olkusz", self.noclegi_olkusz)
        # print("Niegowonice", self.noclegi_niegowonice)
        # print("Myszków", self.noclegi_myszkow)
        # print("Poraj", self.noclegi_poraj)
        # print("Nierada", self.noclegi_nierada)

    def lista_wszystk_nocl(self):
        print(self.dane_noclegi)

    # def suma_noclegow_miejscowosc(self, town):
    #     for el in self.noclegi_rudawa






    # def il_noclegow_na_dany_dzien(self, date):
    #     for el in self.dane_o_noclegach:
    #         self.il_noclegow += int(el[7])
    #         self.il_domow_z_noclegiem += 1
    #     return self.il_noclegow, self.il_domow_z_noclegiem


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
# noclegi.lista_nocl_miejscow()
# noclegi.lista_wszystk_nocl()
# noclegi.wczytaj_dane()
# noclegi.miejscowosc_na_data()
# noclegi.lista_nocl_data("2022-08-03")
# noclegi.lista_nocl_data("2022-08-04")
noclegi.suma_nocl_data("2022-08-04")
