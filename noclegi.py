from main import read_file
import datetime


class Noclegi:
    def __init__(self, file_path_accommodation):
        self.data_accommodation = read_file(file_path_accommodation)
        self.all_accommodation = {}
        self.wczytaj_dane()

    # upload data from a file to a dictionary
    def wczytaj_dane(self):
        for id_a, data_a in self.data_accommodation.items():
            town = data_a[2]
            street = data_a[3]
            house = data_a[4]
            apartment = data_a[5]
            surname = data_a[0]
            given_name = data_a[1]
            phone = data_a[6]
            number_accommod = data_a[7]
            number_accommod = 0 if not number_accommod else int(number_accommod)
            number_shower = data_a[8]
            number_shower = 0 if not number_shower else int(number_shower)
            comment = data_a[9]
            date = self.miejscowosc_na_data(town)
            if not self.all_accommodation.get(town):
                self.all_accommodation[(id_a, town, date)] = []
            self.all_accommodation[(id_a, town, date)] += [[town, street, house, apartment, surname, given_name, phone,
                                                            number_accommod, number_shower, comment, id_a]]

    # decode an accommodation date from a town name
    def miejscowosc_na_data(self, town):
        if town == "Rudawa" or town == "Radwanowice":
            self.date_accommod = datetime.datetime(2022, 8, 3).date()
        elif town == "Olkusz":
            self.date_accommod = datetime.datetime(2022, 8, 4).date()
        elif town == "Niegowonice":
            self.date_accommod = datetime.datetime(2022, 8, 5).date()
        elif town == "Myszków":
            self.date_accommod = datetime.datetime(2022, 8, 6).date()
        elif town == "Poraj":
            self.date_accommod = datetime.datetime(2022, 8, 7).date()
        elif town == "Nierada":
            self.date_accommod = datetime.datetime(2022, 8, 8).date()
        else:
            self.date_accommod = "x"
        return self.date_accommod

    # create a list of data for accommodation and showers for a specific date
    def lista_n_p_data(self, date):
        list_date = []
        for k, v in self.all_accommodation.items():
            if date == str(k[2]):
                list_date += v
        return list_date

    # return a list of accommodation for a specific date
    def lista_nocleg_data(self, date):
        self.list_accommod_date = []
        for el in self.lista_n_p_data(date):
            number_accommod = el[7]
            if number_accommod > 0:
                self.list_accommod_date.append(el)
        return self.list_accommod_date

    # return no. of houses with accommodation and no. of accommodation for a specific date
    def suma_nocl_data(self, date):
        self.sum_house_accommod = 0
        self.sum_accommod = 0
        for el in self.lista_n_p_data(date):
            number_accommod = el[7]
            if number_accommod > 0:
                self.sum_house_accommod += 1
                self.sum_accommod += number_accommod
        # print(f"Lista na {date}: {self.lista_n_p_data(date)}")
        # print(f"{self.sum_house_accommod} - suma domów z noclegiem ({date})")
        # print(f"{self.sum_accommod} - suma noclegów jednostkowych ({date})")
        return self.sum_house_accommod, self.sum_accommod

    # return a list of all all accommodation
    def lista_wszystk_nocl(self):
        return self.data_accommodation

    # return no. of houses with additional shower and no. of additional showers for a specific date
    def suma_pryszn_data(self, date):
        self.suma_dom_prysznic = 0
        self.suma_prysznic = 0
        for el in self.lista_n_p_data(date):
            number_shower = el[8]
            if number_shower > 0:
                self.suma_dom_prysznic += 1
                self.suma_prysznic += number_shower
        # print(f"Lista na {date}: {self.lista_n_p_data(date)}")
        # print(f"{self.suma_dom_prysznic} - suma domów z myciem się ({date})")
        # print(f"{self.suma_prysznic} - suma myć jednostkowych ({date})")
        return self.suma_dom_prysznic, self.suma_prysznic

    # return a list of showers for a specific date
    def lista_prysznic_data(self, date):
        self.lista_pryszn_data = []
        for el in self.lista_n_p_data(date):
            number_shower = el[8]
            if number_shower > 0:
                self.lista_pryszn_data.append(el)
        return self.lista_pryszn_data

    """ return a list of 'small houses' (houses where there are max 4 places to sleep and shower in total) 
    and no. of accommodation in 'small houses' """
    def zestawienie_malych_domow(self, date):
        male_domy = {}
        il_nocl_mal_dom = 0
        for el in self.lista_n_p_data(date):
            number_accommod = el[7]
            number_shower = el[8]
            if 0 < number_accommod <= 4 and number_accommod + number_shower <= 4:
                male_domy[(tuple(el))] = []
                il_nocl_mal_dom += number_accommod
        return male_domy, il_nocl_mal_dom


noclegi = Noclegi("accommodation.json")
# noclegi.suma_nocl_data("2022-08-03")
