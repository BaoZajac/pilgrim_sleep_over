from flask import Flask, request, render_template, redirect, Response
from main import read_file, write_file
from accommodation.accommodation import accommodations as accommod
from pilgrim.pilgrim import pilg
import pandas as pd
import io


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

ACCOMMODATION_PATH = "accommodation/accommodation.json"
PILGRIMS_PATH = "pilgrim/pilgrims.json"
LIST_GROUPS = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
LIST_ROLES = ["bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy", "przewodnik",
              "schola", "szef", "techniczny"]
day = "2022-08-04"


@app.route('/')
def main():
    accommod_summary_date = accommod.give_no_of_accommodation(day)
    shower_summary_date = accommod.give_no_of_showers(day)
    list_date_accommod = accommod.create_list_date_accommod(day)
    list_date_showers = accommod.create_list_date_showers(day)
    return render_template('main.html', accommod_summary_date=accommod_summary_date, day=day[-1],
                           shower_summary_date=shower_summary_date, list_date_accommod=list_date_accommod,
                           list_date_showers=list_date_showers)


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def accommodation():
    data_accommodation = accommod.data_accommodation
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
        write_file(data_accommodation, ACCOMMODATION_PATH)
    addresses_data_list = list(data_accommodation.items())
    if request.path == '/noclegi/':
        return render_template("accommodation.html", addresses_data_list=addresses_data_list, day=day[-1])
    elif request.path == '/dodaj-nocleg/':
        return render_template("add-accommodation.html")


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edit_accommodation():
    if request.method == "POST":
        data_accommodation = accommod.data_accommodation
        _id = request.form["id"]
        accommod_info = dict(request.form)
        del accommod_info["id"]
        accommod_info = list(accommod_info.values())
        data_accommodation[_id] = accommod_info
        write_file(data_accommodation, ACCOMMODATION_PATH)
        return redirect('/noclegi/')
    accommodation_id = request.args["accommodation-id"]
    accommodation_info = read_file(ACCOMMODATION_PATH)[accommodation_id]
    return render_template("edit-accommodation.html", accommodation_info=accommodation_info,
                           accommodation_id=accommodation_id)


@app.route('/usun-nocleg/', methods=['GET', 'POST'])
def delete_accommodation():
    if request.method == "POST":
        data_accommodation = accommod.data_accommodation
        _id = request.form["id"]
        del data_accommodation[_id]
        write_file(data_accommodation, ACCOMMODATION_PATH)
        return redirect('/noclegi/')
    accommodation_id = request.args["accommodation-id"]
    accommodation_info = read_file(ACCOMMODATION_PATH)[accommodation_id]
    return render_template("delete-accommodation.html", accommodation_info=accommodation_info,
                           accommodation_id=accommodation_id)


@app.route('/pielgrzymi/', methods=['GET', 'POST'])
def pilgrim():
    data_pilgrims = read_file(PILGRIMS_PATH)
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        small_group = request.form["small_group"]
        role = request.form["role"]
        if role == "":
            role = "-"
        accommodations = request.form["accommodation"]
        sex = request.form["sex"]
        if data_pilgrims.keys():
            pilgrims_list = list(data_pilgrims.keys())
            pilgrims_list = [int(el) for el in pilgrims_list]
            pilgrim_id = max(pilgrims_list) + 1
        else:
            pilgrim_id = 1
        data_pilgrims[pilgrim_id] = last_name, given_name, sex, small_group, role, accommodations
        write_file(data_pilgrims, PILGRIMS_PATH)
        return redirect('/pielgrzymi/')
    data_pilgrims_list = list(data_pilgrims.items())
    return render_template("pilgrims.html", data_pilgrims_list=data_pilgrims_list, list_roles=LIST_ROLES,
                           list_groups=LIST_GROUPS, day=day[-1])


@app.route('/edytuj-pielgrzyma/', methods=['GET', 'POST'])
def edit_pilgrim():
    list_roles = ["-"] + LIST_ROLES
    list_groups = LIST_GROUPS
    if request.method == "POST":
        data_pilgrims = read_file(PILGRIMS_PATH)
        _id = request.form["id"]
        pilgrim_info = dict(request.form)
        del pilgrim_info["id"]
        pilgrim_info = list(pilgrim_info.values())
        data_pilgrims[_id] = pilgrim_info
        write_file(data_pilgrims, PILGRIMS_PATH)
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_single_pilgrim = read_file(PILGRIMS_PATH)[pilgrim_id]
    small_group = data_single_pilgrim[3]
    if small_group != "funkcyjni":
        small_group = int(small_group)
    list_groups.remove(small_group)
    role_pilg = data_single_pilgrim[4]
    list_roles.remove(role_pilg)
    return render_template("edit-pilgrim.html", data_single_pilgrim=data_single_pilgrim, pilgrim_id=pilgrim_id,
                           list_roles=list_roles, list_groups=list_groups)


@app.route('/usun-pielgrzyma/', methods=['GET', 'POST'])
def delete_pilgrim():
    if request.method == "POST":
        data_pilgrims = pilg.data_pilgrims
        _id = request.form["id"]
        del data_pilgrims[_id]
        write_file(data_pilgrims, PILGRIMS_PATH)
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_single_pilgrim = read_file(PILGRIMS_PATH)[pilgrim_id]
    return render_template("delete-pilgrim.html", data_single_pilgrim=data_single_pilgrim, pilgrim_id=pilgrim_id)


@ app.route('/kto-tu-spi/', methods=['GET', 'POST'])
def who_sleeps_here():
    return render_template("who-sleeps-here.html", day=day[-1])


@ app.route('/przyporzadkuj-nocleg/', methods=['GET', 'POST'])
def give_accommodation():
    # list_role = pilg.service_pilgrim_list
    list_role = pilg.create_service_pilgrim_list()
    # list_common_pilg = pilg.normal_pilgrim_list
    list_common_pilg = pilg.create_normal_pilgrim_list()
    list_date_accommod = accommod.create_list_date_accommod(day)
    if request.method == "POST":
        df = pd.DataFrame(list(request.form.items()), columns=['osoba', 'nocleg'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        headers = {
            'Content-Disposition': 'attachment; filename=output.xlsx',
            'Content-type': 'application/vnd.ms-excel'}
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    return render_template("give-accommodation.html", day=day[-1], list_role=list_role,
                           common_pilgrims=list_common_pilg, list_date_accommod=list_date_accommod)
