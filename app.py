from flask import Flask, request, render_template, redirect, Response
from main import read_file, write_file, ACCOMMODATION_JSON_OBJECT_PATH, PILGRIM_JSON_OBJECT_PATH
from accommodation.accommodation import accommodation_object as ao
from pilgrim.pilgrim import pilgrim_object as po
import pandas as pd
import io


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

LIST_GROUPS = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
LIST_ROLES = ["bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy", "przewodnik",
              "schola", "szef", "techniczny"]
day = "2022-08-04"


@app.route('/')
def main():
    accommodations_summary_for_date = ao.give_number_of_accommodations(day)
    showers_summary_for_date = ao.give_number_of_showers(day)
    list_accommodations_for_date = ao.create_list_accommodations_for_date(day)
    list_showers_for_date = ao.create_list_showers_for_date(day)
    return render_template('index.html', accommodations_summary_for_date=accommodations_summary_for_date, day=day[-1],
                           showers_summary_for_date=showers_summary_for_date, list_accommodations_for_date=
                           list_accommodations_for_date, list_showers_for_date=list_showers_for_date)


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def accommodation():
    data_accommodation = ao.accommodation_base_json
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        town = request.form["town"]
        street = request.form["street"]
        house = request.form["house"]
        apartment = request.form["apartment"]
        phone = request.form["phone"]
        sleep = request.form["sleep"]
        shower = request.form["shower"]
        comment = request.form["comment"]
        accommodation_list = list(data_accommodation.keys())
        accommodation_list = [int(el) for el in accommodation_list]
        accommodation_id = max(accommodation_list) + 1
        data_accommodation[accommodation_id] = last_name, given_name, town, street, house, apartment, phone, sleep,\
                                               shower, comment
        write_file(data_accommodation, ACCOMMODATION_JSON_OBJECT_PATH)
    addresses_data_list = list(data_accommodation.items())
    if request.path == '/noclegi/':
        return render_template("accommodation.html", addresses_data_list=addresses_data_list, day=day[-1])


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edit_accommodation():
    if request.method == "POST":
        data_accommodation = ao.accommodation_base_json
        _id = request.form["id"]
        stay_info = dict(request.form)
        del stay_info["id"]
        stay_info = list(stay_info.values())
        data_accommodation[_id] = stay_info
        write_file(data_accommodation, ACCOMMODATION_JSON_OBJECT_PATH)
        return redirect('/noclegi/')
    accommodation_id = request.args["accommodation-id"]
    accommodation_info = read_file(ACCOMMODATION_JSON_OBJECT_PATH)[accommodation_id]
    return render_template("edit-accommodation.html", accommodation_info=accommodation_info,
                           accommodation_id=accommodation_id)


@app.route('/usun-nocleg/', methods=['GET', 'POST'])
def delete_accommodation():
    if request.method == "POST":
        data_accommodation = ao.accommodation_base_json
        _id = request.form["id"]
        del data_accommodation[_id]
        write_file(data_accommodation, ACCOMMODATION_JSON_OBJECT_PATH)
        return redirect('/noclegi/')
    accommodation_id = request.args["accommodation-id"]
    accommodation_info = read_file(ACCOMMODATION_JSON_OBJECT_PATH)[accommodation_id]
    return render_template("delete-accommodation.html", accommodation_info=accommodation_info,
                           accommodation_id=accommodation_id)


@app.route('/pielgrzymi/', methods=['GET', 'POST'])
def pilgrim():
    data_pilgrims = read_file(PILGRIM_JSON_OBJECT_PATH)
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        small_group = request.form["small_group"]
        role = request.form["role"]
        if role == "":
            role = "-"
        last_stay = request.form["accommodation"]
        gender = request.form["gender"]
        if data_pilgrims.keys():
            pilgrims_list = list(data_pilgrims.keys())
            pilgrims_list = [int(el) for el in pilgrims_list]
            pilgrim_id = max(pilgrims_list) + 1
        else:
            pilgrim_id = 1
        data_pilgrims[pilgrim_id] = last_name, given_name, gender, small_group, role, last_stay
        write_file(data_pilgrims, PILGRIM_JSON_OBJECT_PATH)
        return redirect('/pielgrzymi/')
    data_pilgrims_list = list(data_pilgrims.items())
    return render_template("pilgrims.html", data_pilgrims_list=data_pilgrims_list, list_roles=LIST_ROLES,
                           list_groups=LIST_GROUPS, day=day[-1])


@app.route('/edytuj-pielgrzyma/', methods=['GET', 'POST'])
def edit_pilgrim():
    list_roles = ["-"] + LIST_ROLES
    list_groups = LIST_GROUPS
    if request.method == "POST":
        data_pilgrims = read_file(PILGRIM_JSON_OBJECT_PATH)
        _id = request.form["id"]
        pilgrim_info = dict(request.form)
        del pilgrim_info["id"]
        pilgrim_info = list(pilgrim_info.values())
        data_pilgrims[_id] = pilgrim_info
        write_file(data_pilgrims, PILGRIM_JSON_OBJECT_PATH)
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_single_pilgrim = read_file(PILGRIM_JSON_OBJECT_PATH)[pilgrim_id]
    # small_group = data_single_pilgrim[3]
    # if small_group != "funkcyjni":
    #     small_group = int(small_group)
    # list_groups.remove(small_group)
    role_pilg = data_single_pilgrim[4]
    list_roles.remove(role_pilg)
    return render_template("edit-pilgrim.html", data_single_pilgrim=data_single_pilgrim, pilgrim_id=pilgrim_id,
                           list_roles=list_roles, list_groups=list_groups)


@app.route('/usun-pielgrzyma/', methods=['GET', 'POST'])
def delete_pilgrim():
    if request.method == "POST":
        data_pilgrims = po.data_pilgrims
        _id = request.form["id"]
        del data_pilgrims[_id]
        write_file(data_pilgrims, PILGRIM_JSON_OBJECT_PATH)
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_single_pilgrim = read_file(PILGRIM_JSON_OBJECT_PATH)[pilgrim_id]
    return render_template("delete-pilgrim.html", data_single_pilgrim=data_single_pilgrim, pilgrim_id=pilgrim_id)


@ app.route('/przyporzadkuj-nocleg/', methods=['GET', 'POST'])
def give_accommodation():
    service_pilgrim_list = po.create_service_pilgrim_list()
    normal_pilgrim_list = po.create_normal_pilgrim_list()
    list_accommodations_for_date = ao.create_list_accommodations_for_date(day)
    if request.method == "POST":
        df = pd.DataFrame(list(request.form.items()), columns=['OSOBA', 'NOCLEG'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        filename = f'lista_noclegow_{day}.xlsx'
        headers = {
            'Content-Disposition': f'attachment; filename="{filename}"',
            'Content-type': 'application/vnd.ms-excel'}
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    return render_template("give-accommodation.html", day=day[-1], service_pilgrim_list=service_pilgrim_list,
                           normal_pilgrim_list=normal_pilgrim_list, list_accommodations_for_date=list_accommodations_for_date)
