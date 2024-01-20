from main import read_file
import datetime
from datetime import datetime

from pilgrim.pilgrim_with_function import PilgrimWithFunction


class Pilgrims:
    def __init__(self, file_path_pilgrims):
        self.data_pilgrims = read_file(file_path_pilgrims)
        self.role_0 = []
        self.role_1 = []
        self.role_2 = []
        self.role_school = []
        self.pilgrims_no_accommod = []
        self.pilgrims_other = []
        self.sum_priority = {}

        self.role()
        self.normal_pilgrim()
        self.role_priority()
        self.normal_pilgr_priority()

        self.all_pilgrims = self.role_0 + self.role_1 + self.role_2 + self.role_school + self.pilgrims_no_accommod \
                            + self.pilgrims_other
        self.all_pilgrims_normal = self.pilgrims_no_accommod + self.pilgrims_other

    def role(self):
        # role_person data: id, role, sex, last accommodation, priority
        self.list_role_ppl = []
        for id_p, data_p in self.data_pilgrims.items():
            if data_p[3] == "funkcyjni":
                id_pilgrim = id_p
                pilgrim_role = data_p[4]
                sex = data_p[2]
                date_accommod = data_p[5]
                surname = data_p[0]
                name = data_p[1]
                data_role = [id_pilgrim, pilgrim_role, sex, date_accommod, surname, name]
                self.list_role_ppl.append(data_role)
                if pilgrim_role == PilgrimWithFunction.PORZADKOWY or pilgrim_role == PilgrimWithFunction.CHORAZY:
                    self.role_0.append(data_role)
                elif pilgrim_role == PilgrimWithFunction.SZEF or pilgrim_role == PilgrimWithFunction.PILOT \
                        or pilgrim_role == PilgrimWithFunction.PRZEWODNIK \
                        or pilgrim_role == PilgrimWithFunction.LIDER_KWATERM_JUTRO:
                    self.role_1.append(data_role)
                elif pilgrim_role == PilgrimWithFunction.KWATERMISTRZ_DZIS:
                    self.role_school.append(data_role)
                else:
                    self.role_2.append(data_role)

    def normal_pilgrim(self):
        # pilgrim data: id, no. of a small group, sex, last accommodation, priority
        self.small_groups_division = {}
        self.list_other_pilgr = []
        for id_p, data_p in self.data_pilgrims.items():
            if data_p[3] != "funkcyjni":
                id_pilgrim = id_p
                pilgrim_small_group = data_p[3]
                sex = data_p[2]
                date_accommod = data_p[5]
                surname = data_p[0]
                name = data_p[1]
                data_normal_pilgrim = [id_pilgrim, pilgrim_small_group, sex, date_accommod, surname, name]
                self.list_other_pilgr.append(data_normal_pilgrim)
                if not pilgrim_small_group in self.small_groups_division.keys():
                    self.small_groups_division[pilgrim_small_group] = [data_normal_pilgrim]
                else:
                    self.small_groups_division[pilgrim_small_group].append(data_normal_pilgrim)
                self.from_last_accommod(date_accommod)
                if self.accommod_days >= 3:
                    self.pilgrims_no_accommod.append(data_normal_pilgrim)
                else:
                    self.pilgrims_other.append(data_normal_pilgrim)

    def priority_sex(self, grp, priority):
        for el in grp:
            self.priority = priority
            if el[2] == "mężczyzna":
                # self.priority *= 1.5
                self.priority += 1
            el.append(self.priority)
        return grp

    def role_priority(self):
        self.priority_sex(self.role_0, 0)
        self.priority_sex(self.role_1, 2)
        self.priority_sex(self.role_2, 6)
        self.priority_sex(self.role_school, 20)

    def normal_pilgr_priority(self):
        self.priority_sex(self.pilgrims_no_accommod, 4)
        self.priority_sex(self.pilgrims_other, 8)

    # count no. of days from the last accommodation
    def from_last_accommod(self, date_day):
        today = datetime.now().date()
        last_accommod = datetime.strptime(date_day, "%d-%m-%Y").date()
        accommod_days_count = today - last_accommod
        self.accommod_days = accommod_days_count.days


pilg = Pilgrims("pilgrim/pilgrims.json")

