from main import read_file, ACCOMMODATION_JSON_OBJECT_PATH
import datetime


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

    def create_list_accommodation_shower_for_date(self, date):
        list_accommodation_shower_for_date = []
        accommodation_base = self.upload_accommodation_base()
        for k, v in accommodation_base.items():
            if date == str(k[2]):
                list_accommodation_shower_for_date += v
        return list_accommodation_shower_for_date

    def create_list_accommodations_for_date(self, date):
        list_accommodations_for_date = []
        for el in self.create_list_accommodation_shower_for_date(date):
            accommodation_quantity = el[7]
            if accommodation_quantity > 0:
                list_accommodations_for_date.append(el)
        return list_accommodations_for_date

    def give_number_of_accommodations(self, date):
        sum_of_houses_with_accommodations = 0
        sum_of_single_accommodation_places = 0
        for el in self.create_list_accommodation_shower_for_date(date):
            accommodation_quantity = el[7]
            if accommodation_quantity > 0:
                sum_of_houses_with_accommodations += 1
                sum_of_single_accommodation_places += accommodation_quantity
        return sum_of_houses_with_accommodations, sum_of_single_accommodation_places

    def give_number_of_showers(self, date):
        sum_of_houses_with_showers = 0
        sum_of_single_shower_places = 0
        for el in self.create_list_accommodation_shower_for_date(date):
            shower_quantity = el[8]
            if shower_quantity > 0:
                sum_of_houses_with_showers += 1
                sum_of_single_shower_places += shower_quantity
        return sum_of_houses_with_showers, sum_of_single_shower_places

    def create_list_showers_for_date(self, date):
        list_showers_for_date = []
        for el in self.create_list_accommodation_shower_for_date(date):
            shower_quantity = el[8]
            if shower_quantity > 0:
                list_showers_for_date.append(el)
        return list_showers_for_date


accommodation_object = Accommodation(ACCOMMODATION_JSON_OBJECT_PATH)

