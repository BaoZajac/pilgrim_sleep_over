from flask import Flask, request, render_template, redirect, url_for, Response, make_response
# from flask_sqlalchemy import SQLAlchemy
# from flask_alembic import Alembic
from main import read_file, write_file
from noclegi import noclegi as accommod
from uczestnicy import pielg
import pandas as pd
import io


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

# db = SQLAlchemy(app)
day = "2022-08-04"        # TODO: make universal for any date


# # creating a table with addresses
# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     last_name = db.Column(db.String(120), nullable=False)
#     given_name = db.Column(db.String(120), nullable=True)       #TODO: OR first name OR surname must be completed
#     town = db.Column(db.String(120), nullable=False)
#     street = db.Column(db.String(120), nullable=True)
#     house = db.Column(db.String(120), nullable=False)
#     apartment = db.Column(db.String(120), nullable=True)
#     phone = db.Column(db.Integer, nullable=False)


@app.route('/')
def main():
    accommod_summary = accommod.suma_nocl_data(day)
    shower_summary = accommod.suma_pryszn_data(day)
    list_accommod = accommod.lista_nocleg_data(day)
    list_shower = accommod.lista_prysznic_data(day)
    return render_template('main.html', accommod_summary=accommod_summary, day=day[-1], shower_summary=shower_summary,
                           list_accommod=list_accommod, list_shower=list_shower)


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def nocleg():
    data_accommod = accommod.dane_noclegi
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
        # date = accommod.miejscowosc_na_data(town)
        # print(date)
        # print(type(date))
        data_accommod[accommod_id] = last_name, given_name, town, street, house, apartment, phone, sleep, shower,\
                                     comment  #, date
        write_file(data_accommod, "noclegi.json")
    data_address = list(data_accommod.items())
    if request.path == '/noclegi/':
        return render_template("accommodation.html", data_address=data_address, day=day[-1])
    elif request.path == '/dodaj-nocleg/':
        return render_template("add_accommodation.html")


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edycja_noclegu():
    if request.method == "POST":
        data_accommod = accommod.dane_noclegi
        _id = request.form["id"]
        accommod_info = dict(request.form)
        town_before = data_accommod[_id][2]
        del accommod_info["id"]
        accommod_info = list(accommod_info.values())
        town_after = accommod_info[2]
        if town_before != town_after:
            data = accommod.miejscowosc_na_data(town_after)
            # accommod_info.append(data)
        data_accommod[_id] = accommod_info
        write_file(data_accommod, "noclegi.json")
        return redirect('/noclegi/')
    accommod_id = request.args["accom-id"]
    accom_info = read_file("noclegi.json")[accommod_id]
    return render_template("edit_accommodation.html", accommod=accom_info, accommod_id=accommod_id)


@app.route('/usun-nocleg/', methods=['GET', 'POST'])
def usun_nocleg():
    if request.method == "POST":
        data_accommod = accommod.dane_noclegi
        _id = request.form["id"]
        del data_accommod[_id]
        write_file(data_accommod, "noclegi.json")
        return redirect('/noclegi/')
    accommod_id = request.args["accom-id"]
    accom_info = read_file("noclegi.json")[accommod_id]
    return render_template("delete_accommodation.html", accommod=accom_info, accommod_id=accommod_id)


@app.route('/pielgrzymi/', methods=['GET', 'POST'])
def pielgrzym():
    data_pilgrims = read_file("pielgrzymi.json")
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
        write_file(data_pilgrims, "pielgrzymi.json")
        return redirect('/pielgrzymi/')
    data_pilgrims_list = list(data_pilgrims.items())
    return render_template("pilgrims.html", pilgrims=data_pilgrims_list, list_roles=list_roles,
                           list_groups=list_groups, day=day[-1])


@app.route('/edytuj-pielgrzyma/', methods=['GET', 'POST'])
def edycja_pielgrzyma():
    list_roles = ["-", "bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy",
                     "przewodnik", "schola", "szef", "techniczny"]
    list_groups = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
    if request.method == "POST":
        data_pilgrims = read_file("pielgrzymi.json")
        _id = request.form["id"]
        data_pilgr = dict(request.form)
        del data_pilgr["id"]
        data_pilgr = list(data_pilgr.values())
        data_pilgrims[_id] = data_pilgr
        write_file(data_pilgrims, "pielgrzymi.json")
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_pilgrim = read_file("pielgrzymi.json")[pilgrim_id]
    group = data_pilgrim[3]
    if group != "funkcyjni":
        group = int(group)
    list_groups.remove(group)
    role = data_pilgrim[4]
    list_roles.remove(role)
    return render_template("edycja-pielgrzyma.html", pilgrim=data_pilgrim, pilgrim_id=pilgrim_id,
                           list_roles=list_roles, list_groups=list_groups)


@app.route('/usun-pielgrzyma/', methods=['GET', 'POST'])
def usun_pielgrzyma():
    if request.method == "POST":
        data_pilgrims = pielg.dane_pielgrzymi
        _id = request.form["id"]
        del data_pilgrims[_id]
        write_file(data_pilgrims, "pielgrzymi.json")
        return redirect('/pielgrzymi/')
    pilgrim_id = request.args["pilgrim-id"]
    data_pilgrim = read_file("pielgrzymi.json")[pilgrim_id]
    return render_template("usun-pielgrzyma.html", pilgrim=data_pilgrim, pilgrim_id=pilgrim_id)


@ app.route('/kto-tu-spi/', methods=['GET', 'POST'])
def kto_tu_spi():
    return render_template("kto-tu-spi.html", day=day[-1])


@ app.route('/przyporzadkuj-nocleg/', methods=['GET', 'POST'])
def daj_nocleg():
    list_role = pielg.lista_funkcyjnych
    list_role.sort(key=lambda list_role: list_role[6])
    list_common_pilg = pielg.lista_pozost_pielg
    list_common_pilg.sort(key=lambda list_common_pilg: list_common_pilg[6])
    list_accommod = accommod.lista_nocleg_data(day)
    if request.method == "POST":
        df = pd.DataFrame(list(request.form.items()), columns=['osoba', 'nocleg'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        headers = {
            'Content-Disposition': 'attachment; filename=output.xlsx',
            'Content-type': 'application/vnd.ms-excel'}
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    return render_template("give_accommodation.html", day=day[-1], list_role=list_role,
                           common_pilgrims=list_common_pilg, list_accommod=list_accommod)
