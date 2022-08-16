from main import read_file
import datetime


class Noclegi:
    def __init__(self, file_path_accommodation):
        self.data_accommodation = read_file(file_path_accommodation)
        self.all_accommodation = {}
        self.wczytaj_dane()

    # wczytaj dane z pliku do słownika
    def wczytaj_dane(self):
        for id_n, dane_n in self.data_accommodation.items():
            town = dane_n[2]
            street = dane_n[3]
            dom = dane_n[4]
            apartment = dane_n[5]
            surname = dane_n[0]
            given_name = dane_n[1]
            phone = dane_n[6]
            il_noclegow = dane_n[7]
            il_noclegow = 0 if not il_noclegow else int(il_noclegow)
            il_pryszn = dane_n[8]
            il_pryszn = 0 if not il_pryszn else int(il_pryszn)
            komentarz = dane_n[9]
            data = self.miejscowosc_na_data(town)
            if not self.all_accommodation.get(town):
                self.all_accommodation[(id_n, town, data)] = []
            self.all_accommodation[(id_n, town, data)] += [[town, street, dom, apartment, surname, given_name,
                                                                   phone, il_noclegow, il_pryszn, komentarz, id_n]]

    # odkodowanie daty noclegu z nazwy miejscowości
    def miejscowosc_na_data(self, town):
        if town == "Rudawa" or town == "Radwanowice":
            self.data_noclegu = datetime.datetime(2022, 8, 3).date()
        elif town == "Olkusz":
            self.data_noclegu = datetime.datetime(2022, 8, 4).date()
        elif town == "Niegowonice":
            self.data_noclegu = datetime.datetime(2022, 8, 5).date()
        elif town == "Myszków":
            self.data_noclegu = datetime.datetime(2022, 8, 6).date()
        elif town == "Poraj":
            self.data_noclegu = datetime.datetime(2022, 8, 7).date()
        elif town == "Nierada":
            self.data_noclegu = datetime.datetime(2022, 8, 8).date()
        else:
            self.data_noclegu = "x"
        return self.data_noclegu

    # tworzy listę danych dla noclegów i pryszniców dla danej daty
    def lista_n_p_data(self, data):
        lista_data = []
        for k, v in self.all_accommodation.items():
            if data == str(k[2]):
                lista_data += v
        return lista_data

    # zwraca listę noclegów na dany dzień
    def lista_nocleg_data(self, data):
        self.lista_nocl_data = []
        for el in self.lista_n_p_data(data):
            il_noclegow = el[7]
            if il_noclegow > 0:
                self.lista_nocl_data.append(el)
        return self.lista_nocl_data

    # podaje il. domów z noclegiem i il. noclegów dla danej daty
    def suma_nocl_data(self, data):
        self.suma_dom_nocleg = 0
        self.suma_nocleg = 0
        for el in self.lista_n_p_data(data):
            il_noclegow = el[7]
            if il_noclegow > 0:
                self.suma_dom_nocleg += 1
                self.suma_nocleg += il_noclegow
        # print(f"Lista na {data}: {self.lista_n_p_data(data)}")
        # print(f"{self.suma_dom_nocleg} - suma domów z noclegiem ({data})")
        # print(f"{self.suma_nocleg} - suma noclegów jednostkowych ({data})")
        return self.suma_dom_nocleg, self.suma_nocleg

    # zwraca listę wszystkich wszystkich noclegów
    def lista_wszystk_nocl(self):
        return self.data_accommodation

    # podaje il. domów z myciem się i il. myć jednostkowych dla danej daty
    def suma_pryszn_data(self, data):
        self.suma_dom_prysznic = 0
        self.suma_prysznic = 0
        for el in self.lista_n_p_data(data):
            il_prysznicow = el[8]
            if il_prysznicow > 0:
                self.suma_dom_prysznic += 1
                self.suma_prysznic += il_prysznicow
        # print(f"Lista na {data}: {self.lista_n_p_data(data)}")
        # print(f"{self.suma_dom_prysznic} - suma domów z myciem się ({data})")
        # print(f"{self.suma_prysznic} - suma myć jednostkowych ({data})")
        return self.suma_dom_prysznic, self.suma_prysznic

    # zwraca listę pryszniców na dany dzień
    def lista_prysznic_data(self, data):
        self.lista_pryszn_data = []
        for el in self.lista_n_p_data(data):
            il_pryszn = el[8]
            if il_pryszn > 0:
                self.lista_pryszn_data.append(el)
        return self.lista_pryszn_data

    """zwraca listę "małych domów" (domów, w których jest maks 4 miejsca do noclegu i mycia się łącznie) 
    oraz il noclegów w małych domach"""
    def zestawienie_malych_domow(self, data):
        male_domy = {}
        il_nocl_mal_dom = 0
        for el in self.lista_n_p_data(data):
            il_noclegow = el[7]
            il_pryszn = el[8]
            if 0 < il_noclegow <= 4 and il_noclegow + il_pryszn <= 4:
                male_domy[(tuple(el))] = []
                il_nocl_mal_dom += il_noclegow
        return male_domy, il_nocl_mal_dom


noclegi = Noclegi("accommodation.json")
# noclegi.suma_nocl_data("2022-08-03")
