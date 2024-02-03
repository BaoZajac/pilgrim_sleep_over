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
            number_accommod = data_a[7]
            number_accommod = 0 if not number_accommod else int(number_accommod)
            number_shower = data_a[8]
            number_shower = 0 if not number_shower else int(number_shower)
            comment = data_a[9]
            date = self.decode_town_to_date(town)
            if not self.accommodation_base.get(town):
                self.accommodation_base[(id_a, town, date)] = []
            self.accommodation_base[(id_a, town, date)] += [[town, street, house, apartment, surname, given_name, phone,
                                                            number_accommod, number_shower, comment, id_a]]

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

    # create a list of data for accommodation and showers for a specific date
    def list_accom_shower_date(self, date):
        list_date = []
        for k, v in self.accommodation_base.items():
            if date == str(k[2]):
                list_date += v
        return list_date

    # return a list of accommodation for a specific date
    def list_accom_date(self, date):
        self.list_accommod_date = []
        for el in self.list_accom_shower_date(date):
            number_accommod = el[7]
            if number_accommod > 0:
                self.list_accommod_date.append(el)
        return self.list_accommod_date

    # return no. of houses with accommodation and no. of accommodation for a specific date
    def sum_accommod_date(self, date):
        self.sum_house_accommod = 0
        self.sum_accommod = 0
        for el in self.list_accom_shower_date(date):
            number_accommod = el[7]
            if number_accommod > 0:
                self.sum_house_accommod += 1
                self.sum_accommod += number_accommod
        return self.sum_house_accommod, self.sum_accommod

    # return no. of houses with additional shower and no. of additional showers for a specific date
    def sum_shower_date(self, date):
        self.sum_house_shower = 0
        self.sum_shower = 0
        for el in self.list_accom_shower_date(date):
            number_shower = el[8]
            if number_shower > 0:
                self.sum_house_shower += 1
                self.sum_shower += number_shower
        return self.sum_house_shower, self.sum_shower

    # return a list of showers for a specific date
    def list_showers_date(self, date):
        self.list_shower_date = []
        for el in self.list_accom_shower_date(date):
            number_shower = el[8]
            if number_shower > 0:
                self.list_shower_date.append(el)
        return self.list_shower_date


accommodations = Accommodation(ACCOMMODATION_CLASS_PATH)
