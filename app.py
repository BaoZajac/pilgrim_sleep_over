from flask import Flask, request, render_template, redirect, Response
from main import read_file, write_file
from accommodation.accommodation import accommodations as accommod
from pilgrim.pilgrim import pilg
import pandas as pd
import io


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

day = "2022-08-04"        # TODO: make universal for any date


@app.route('/')
def main():
    accommod_summary = accommod.sum_accommod_date(day)
    shower_summary = accommod.sum_shower_date(day)
    list_accommod = accommod.create_list_date_accommod(day)
    list_shower = accommod.list_showers_date(day)
    return render_template('main.html', accommod_summary=accommod_summary, day=day[-1], shower_summary=shower_summary,
                           list_accommod=list_accommod, list_shower=list_shower)


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def accommodation():
    data_accommod = accommod.data_accommodation
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
        accom_list = list(data_accommod.keys())
        accom_list = [int(el) for el in accom_list]
        accommod_id = max(accom_list) + 1
        data_accommod[accommod_id] = last_name, given_name, town, street, house, apartment, phone, sleep, shower,\
                                     comment
        write_file(data_accommod, "accommodation/accommodation.json")
    data_address = list(data_accommod.items())
    if request.path == '/noclegi/':
        return render_template("accommodation.html", data_address=data_address, day=day[-1])
    elif request.path == '/dodaj-nocleg/':
        return render_template("add-accommodation.html")


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edit_accommodation():
    if request.method == "POST":
        data_accommod = accommod.data_accommodation
        _id = request.form["id"]
        accommod_info = dict(request.form)
        del accommod_info["id"]
        accommod_info = list(accommod_info.values())
        data_accommod[_id] = accommod_info
        write_file(data_accommod, "accommodation/accommodation.json")
        return redirect('/noclegi/')
    accommod_id = request.args["accom-id"]
    accom_info = read_file("accommodation/accommodation.json")[accommod_id]
    return render_template("edit-accommodation.html", accommod=accom_info, accommod_id=accommod_id)


@app.route('/usun-nocleg/', methods=['GET', 'POST'])
def delete_accommodation():
    if request.method == "POST":
        data_accommod = accommod.data_accommodation
        _id = request.form["id"]
        del data_accommod[_id]
        write_file(data_accommod, "accommodation/accommodation.json")
        return redirect('/noclegi/')
    accommod_id = request.args["accom-id"]
    accom_info = read_file("accommodation/accommodation.json")[accommod_id]
    return render_template("delete-accommodation.html", accommod=accom_info, accommod_id=accommod_id)


@app.route('/pielgrzymi/', methods=['GET', 'POST'])
def pilgrim():
    data_pilgrims = read_file("pilgrim/pilgrims.json")
    list_roles = ["bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy",
                     "przewodnik", "schola", "szef", "techniczny"]
    list_groups = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        small_group = request.form["small_group"]
        function = request.form["function"]
        if function == "":
            function = "-"
        accommodations = request.form["accommodation"]
        sex = request.form["sex"]
        if data_pilgrims.keys():
            pilgrims_list = list(data_pilgrims.keys())
            pilgrims_list = [int(el) for el in pilgrims_list]
            pilgrim_id = max(pilgrims_list) + 1
        else:
            pilgrim_id = 1
        data_pilgrims[pilgrim_id] = last_name, given_name, sex, small_group, function, accommodations
        write_file(data_pilgrims, "pilgrim/pilgrims.json")
        return redirect('/pielgrzymi/')
    data_pilgrims_list = list(data_pilgrims.items())
    return render_template("pilgrims.html", pilgrims=data_pilgrims_list, list_roles=list_roles,
                           list_groups=list_groups, day=day[-1])


@app.route('/edytuj-pielgrzyma/', methods=['GET', 'POST'])
def edit_pilgrim():
    list_roles = ["-", "bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy",
                     "przewodnik", "schola", "szef", "techniczny"]
    list_groups = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
    if request.method == "POST":
        data_pilgrims = read_file("pilgrim/pilgrims.json")
        _id = request.form["id"]
        data_pilgr = dict(request.form)
        del data_pilgr["id"]
        data_pilgr = list(data_pilgr.values())
        data_pilgrims[_id] = data_pilgr
        write_file(data_pilgrims, "pilgrim/pilgrims.json")
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_pilgrim = read_file("pilgrim/pilgrims.json")[pilgrim_id]
    group = data_pilgrim[3]
    if group != "funkcyjni":
        group = int(group)
    list_groups.remove(group)
    role_pilg = data_pilgrim[4]
    list_roles.remove(role_pilg)
    return render_template("edit-pilgrim.html", data_pilgrim=data_pilgrim, pilgrim_id=pilgrim_id,
                           list_roles=list_roles, list_groups=list_groups)


@app.route('/usun-pielgrzyma/', methods=['GET', 'POST'])
def delete_pilgrim():
    if request.method == "POST":
        data_pilgrims = pilg.data_pilgrims
        _id = request.form["id"]
        del data_pilgrims[_id]
        write_file(data_pilgrims, "pilgrim/pilgrims.json")
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_pilgrim = read_file("pilgrim/pilgrims.json")[pilgrim_id]
    return render_template("delete-pilgrim.html", data_pilgrim=data_pilgrim, pilgrim_id=pilgrim_id)


@ app.route('/kto-tu-spi/', methods=['GET', 'POST'])
def who_sleeps_here():
    return render_template("who-sleeps-here.html", day=day[-1])


@ app.route('/przyporzadkuj-nocleg/', methods=['GET', 'POST'])
def give_accommodation():
    # list_role = pilg.service_pilgrim_list
    list_role = pilg.create_service_pilgrim_list()
    # list_common_pilg = pilg.normal_pilgrim_list
    list_common_pilg = pilg.create_normal_pilgrim_list()
    list_accommod = accommod.create_list_date_accommod(day)
    if request.method == "POST":
        df = pd.DataFrame(list(request.form.items()), columns=['osoba', 'nocleg'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        headers = {
            'Content-Disposition': 'attachment; filename=output.xlsx',
            'Content-type': 'application/vnd.ms-excel'}
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    return render_template("give-accommodation.html", day=day[-1], list_role=list_role,
                           common_pilgrims=list_common_pilg, list_accommod=list_accommod)
