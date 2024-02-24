from main import read_file
import datetime


ACCOMMODATION_CLASS_PATH = "accommodation/accommodation.json"


class Accommodation:
    def __init__(self, file_path_accommodation):
        self.data_accommodation = read_file(file_path_accommodation)
        self.accommodation_base = {}
        
        self.upload_accommodation_base()

    def upload_accommodation_base(self):
        for id_a, data_a in self.data_accommodation.items():
            town = data_a[2]
            street = data_a[3]
            house = data_a[4]
            apartment = data_a[5]
            surname = data_a[0]
            given_name = data_a[1]
            phone = data_a[6]
            accommod_amount = data_a[7]
            accommod_amount = 0 if not accommod_amount else int(accommod_amount)
            number_shower = data_a[8]
            number_shower = 0 if not number_shower else int(number_shower)
            comment = data_a[9]
            date = self.decode_town_to_date(town)
            if not self.accommodation_base.get(town):
                self.accommodation_base[(id_a, town, date)] = []
            self.accommodation_base[(id_a, town, date)] += [[town, street, house, apartment, surname, given_name, phone,
                                                            accommod_amount, number_shower, comment, id_a]]

    def decode_town_to_date(self, town):
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

    def create_list_date_accommod_shower(self, date):
        list_date_accommod_shower = []
        for k, v in self.accommodation_base.items():
            if date == str(k[2]):
                list_date_accommod_shower += v
        return list_date_accommod_shower

    def create_list_date_accommod(self, date):
        self.list_date_accommod = []
        for el in self.create_list_date_accommod_shower(date):
            accommod_amount = el[7]
            if accommod_amount > 0:
                self.list_date_accommod.append(el)
        return self.list_date_accommod

    def give_no_of_accommodation(self, date):
        self.sum_accommod_house = 0
        self.sum_accommod_single_place = 0
        for el in self.create_list_date_accommod_shower(date):
            accommod_amount = el[7]
            if accommod_amount > 0:
                self.sum_accommod_house += 1
                self.sum_accommod_single_place += accommod_amount
        return self.sum_accommod_house, self.sum_accommod_single_place

    def give_no_of_showers(self, date):
        self.sum_showers_house = 0
        self.sum_showers_single_place = 0
        for el in self.create_list_date_accommod_shower(date):
            shower_amount = el[8]
            if shower_amount > 0:
                self.sum_showers_house += 1
                self.sum_showers_single_place += shower_amount
        return self.sum_showers_house, self.sum_showers_single_place

    def create_list_date_showers(self, date):
        self.list_date_showers = []
        for el in self.create_list_date_accommod_shower(date):
            shower_amount = el[8]
            if shower_amount > 0:
                self.list_date_showers.append(el)
        return self.list_date_showers


accommodations = Accommodation(ACCOMMODATION_CLASS_PATH)
