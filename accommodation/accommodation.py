from main import read_file
import datetime


ACCOMMODATION_CLASS_PATH = "accommodation/accommodation.json"


class Accommodation:
    def __init__(self, file_path_accommodation):
        self.accommodation_base_json = read_file(file_path_accommodation)

    def upload_accommodation_base(self):
        accommodation_base = {}
        for id_a, data_a in self.accommodation_base_json.items():
            town = data_a[2]
            street = data_a[3]
            house = data_a[4]
            apartment = data_a[5]
            surname = data_a[0]
            given_name = data_a[1]
            phone = data_a[6]
            accommodation_amount = self.count_accommodation(id_a, 7)
            shower_amount = self.count_shower(id_a, 8)
            comment = data_a[9]
            date = self.decode_town_to_date(town)
            if not accommodation_base.get(town):
                accommodation_base[(id_a, town, date)] = []
            accommodation_base[(id_a, town, date)] += [[town, street, house, apartment, surname, given_name, phone,
                                                        accommodation_amount, shower_amount, comment, id_a]]
        return accommodation_base

    def count_accommodation(self, accommodation_id, accommodation_index):
        accommodation_amount = self.accommodation_base_json[accommodation_id][accommodation_index]
        accommodation_amount = 0 if not accommodation_amount else int(accommodation_amount)
        return accommodation_amount

    def count_shower(self, accommodation_id, shower_index):
        shower_amount = self.accommodation_base_json[accommodation_id][shower_index]
        shower_amount = 0 if not shower_amount else int(shower_amount)
        return shower_amount

    def decode_town_to_date(self, town):
        if town == "Rudawa" or town == "Radwanowice":
            stay_date = self.assign_date(3)
        elif town == "Olkusz":
            stay_date = self.assign_date(4)
        elif town == "Niegowonice":
            stay_date = self.assign_date(5)
        elif town == "Myszków":
            stay_date = self.assign_date(6)
        elif town == "Poraj":
            stay_date = self.assign_date(7)
        elif town == "Nierada":
            stay_date = self.assign_date(8)
        else:
            stay_date = "x"
        return stay_date

    def assign_date(self, day):
        stay_date = datetime.datetime(2022, 8, day).date()
        return stay_date

    def create_list_date_accommod_shower(self, date):
        list_date_accommod_shower = []
        accommodation_base = self.upload_accommodation_base()
        for k, v in accommodation_base.items():
            if date == str(k[2]):
                list_date_accommod_shower += v
        return list_date_accommod_shower

    def create_list_date_accommod(self, date):
        self.list_date_accommod = []
        for el in self.create_list_date_accommod_shower(date):
            accommodation_quantity = el[7]
            if accommodation_quantity > 0:
                self.list_date_accommod.append(el)
        return self.list_date_accommod

    def give_no_of_accommodation(self, date):
        self.sum_accommod_house = 0
        self.sum_accommod_single_place = 0
        for el in self.create_list_date_accommod_shower(date):
            accommodation_quantity = el[7]
            if accommodation_quantity > 0:
                self.sum_accommod_house += 1
                self.sum_accommod_single_place += accommodation_quantity
        return self.sum_accommod_house, self.sum_accommod_single_place

    def give_no_of_showers(self, date):
        self.sum_showers_house = 0
        self.sum_showers_single_place = 0
        for el in self.create_list_date_accommod_shower(date):
            shower_quantity = el[8]
            if shower_quantity > 0:
                self.sum_showers_house += 1
                self.sum_showers_single_place += shower_quantity
        return self.sum_showers_house, self.sum_showers_single_place

    def create_list_date_showers(self, date):
        self.list_date_showers = []
        for el in self.create_list_date_accommod_shower(date):
            shower_quantity = el[8]
            if shower_quantity > 0:
                self.list_date_showers.append(el)
        return self.list_date_showers


accommodations = Accommodation(ACCOMMODATION_CLASS_PATH)
