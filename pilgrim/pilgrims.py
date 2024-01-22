from main import read_file


PILGRIM_CLASS_PATH = "pilgrim/pilgrims.json"
PILGRIM_WITH_FUNCTION_TEXT = "funkcyjni"


class Pilgrims:
    def __init__(self, file_path_pilgrims):
        self.data_pilgrims = read_file(file_path_pilgrims)
        self.pilgrims_no_accommod = []
        self.pilgrims_other = []

        self.role()
        self.normal_pilgrim()

    # create a list of ppl with functions / used in give-accommodation.html
    def role(self):
        self.list_role_ppl = []
        for id_p, data_p in self.data_pilgrims.items():
            if data_p[3] == PILGRIM_WITH_FUNCTION_TEXT:
                id_pilgrim = id_p
                pilgrim_role = data_p[4]
                sex = data_p[2]
                date_accommod = data_p[5]
                surname = data_p[0]
                name = data_p[1]
                data_role = [id_pilgrim, pilgrim_role, sex, date_accommod, surname, name]
                self.list_role_ppl.append(data_role)

    # create a list of normal ppl (ppl without a function) / used in give-accommodation.html
    def normal_pilgrim(self):
        self.list_other_pilgr = []
        for id_p, data_p in self.data_pilgrims.items():
            if data_p[3] != PILGRIM_WITH_FUNCTION_TEXT:
                id_pilgrim = id_p
                pilgrim_small_group = data_p[3]
                sex = data_p[2]
                date_accommod = data_p[5]
                surname = data_p[0]
                name = data_p[1]
                data_normal_pilgrim = [id_pilgrim, pilgrim_small_group, sex, date_accommod, surname, name]
                self.list_other_pilgr.append(data_normal_pilgrim)


pilg = Pilgrims(PILGRIM_CLASS_PATH)
