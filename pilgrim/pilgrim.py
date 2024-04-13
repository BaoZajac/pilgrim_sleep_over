from main import read_file, PILGRIM_JSON_OBJECT_PATH


# PILGRIM_JSON_OBJECT_PATH = "pilgrim/pilgrims.json"
PILGRIM_WITH_FUNCTION_TEXT = "funkcyjni"


class Pilgrim:
    def __init__(self, file_path_pilgrims):
        self.data_pilgrims = read_file(file_path_pilgrims)

    def create_service_pilgrim_list(self):
        service_pilgrim_list = []
        for id_p, data_p in self.data_pilgrims.items():
            if data_p[3] == PILGRIM_WITH_FUNCTION_TEXT:
                id_pilgrim = id_p
                pilgrim_role = data_p[4]
                gender = data_p[2]
                date_accommodation = data_p[5]
                surname = data_p[0]
                name = data_p[1]
                data_service_pilgrim = [id_pilgrim, pilgrim_role, gender, date_accommodation, surname, name]
                service_pilgrim_list.append(data_service_pilgrim)
        return service_pilgrim_list

    def create_normal_pilgrim_list(self):
        normal_pilgrim_list = []
        for id_p, data_p in self.data_pilgrims.items():
            if data_p[3] != PILGRIM_WITH_FUNCTION_TEXT:
                id_pilgrim = id_p
                pilgrim_small_group = data_p[3]
                gender = data_p[2]
                date_accommodation = data_p[5]
                surname = data_p[0]
                name = data_p[1]
                data_normal_pilgrim = [id_pilgrim, pilgrim_small_group, gender, date_accommodation, surname, name]
                normal_pilgrim_list.append(data_normal_pilgrim)
        return normal_pilgrim_list


pilgrim_object = Pilgrim(PILGRIM_JSON_OBJECT_PATH)
