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
        data_accommod[accommod_id] = last_name, given_name, town, street, house, apartment, phone, sleep, shower, comment  #, date
        write_file(data_accommod, "noclegi.json")
    data_address = list(data_accommod.items())
    if request.path == '/noclegi/':
        return render_template("noclegi.html", data_address=data_address, day=day[-1])
    elif request.path == '/dodaj-nocleg/':
        return render_template("dodaj-nocleg.html")


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edycja_noclegu():
    if request.method == "POST":
        data_accommod = accommod.dane_noclegi
        _id = request.form["id"]
        dane_noc = dict(request.form)
        miejscowosc_przed = data_accommod[_id][2]
        del dane_noc["id"]
        dane_noc = list(dane_noc.values())
        miejscowosc_po = dane_noc[2]
        if miejscowosc_przed != miejscowosc_po:
            data = accommod.miejscowosc_na_data(miejscowosc_po)
            # dane_noc.append(data)
        data_accommod[_id] = dane_noc
        write_file(data_accommod, "noclegi.json")
        return redirect('/noclegi/')
    accommod_id = request.args["nocleg-id"]
    data_nocleg = read_file("noclegi.json")[accommod_id]
    return render_template("edycja-noclegu.html", nocleg=data_nocleg, accommod_id=accommod_id)


@app.route('/usun-nocleg/', methods=['GET', 'POST'])
def usun_nocleg():
    if request.method == "POST":
        data_accommod = accommod.dane_noclegi
        _id = request.form["id"]
        del data_accommod[_id]
        write_file(data_accommod, "noclegi.json")
        return redirect('/noclegi/')
    accommod_id = request.args["nocleg-id"]
    data_nocleg = read_file("noclegi.json")[accommod_id]
    return render_template("usun-nocleg.html", nocleg=data_nocleg, accommod_id=accommod_id)


@app.route('/pielgrzymi/', methods=['GET', 'POST'])
def pielgrzym():
    data_pielgrzymi = read_file("pielgrzymi.json")
    lista_funkcji = ["bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy",
                     "przewodnik", "schola", "szef", "techniczny"]
    lista_grupek = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        small_group = request.form["small_group"]
        function = request.form["function"]
        if function == "":
            function = "-"
        accommodations = request.form["accommodation"]
        sex = request.form["sex"]
        if data_pielgrzymi.keys():
            pielg_lista = list(data_pielgrzymi.keys())
            pielg_lista = [int(el) for el in pielg_lista]
            pielgrzym_id = max(pielg_lista) + 1
        else:
            pielgrzym_id = 1
        data_pielgrzymi[pielgrzym_id] = last_name, given_name, sex, small_group, function, accommodations
        write_file(data_pielgrzymi, "pielgrzymi.json")
        return redirect('/pielgrzymi/')
    data_pielgrzymi_lista = list(data_pielgrzymi.items())
    return render_template("pielgrzymi.html", pielgrzymi=data_pielgrzymi_lista, lista_funkcji=lista_funkcji,
                           lista_grupek=lista_grupek, day=day[-1])


@app.route('/edytuj-pielgrzyma/', methods=['GET', 'POST'])
def edycja_pielgrzyma():
    lista_funkcji = ["-", "bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy",
                     "przewodnik", "schola", "szef", "techniczny"]
    lista_grupek = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
    if request.method == "POST":
        data_pielgrzym = read_file("pielgrzymi.json")
        _id = request.form["id"]
        dane_pielgrz = dict(request.form)
        del dane_pielgrz["id"]
        dane_pielgrz = list(dane_pielgrz.values())
        data_pielgrzym[_id] = dane_pielgrz
        write_file(data_pielgrzym, "pielgrzymi.json")
        return redirect('/pielgrzymi/')
    pielgrzym_id = request.args["pielgrzym-id"]
    data_pielgrzym = read_file("pielgrzymi.json")[pielgrzym_id]
    grupka = data_pielgrzym[3]
    if grupka != "funkcyjni":
        grupka = int(grupka)
    lista_grupek.remove(grupka)
    funkcja = data_pielgrzym[4]
    lista_funkcji.remove(funkcja)
    return render_template("edycja-pielgrzyma.html", pielgrzym=data_pielgrzym, pielgrzym_id=pielgrzym_id,
                           lista_funkcji=lista_funkcji, lista_grupek=lista_grupek)


@app.route('/usun-pielgrzyma/', methods=['GET', 'POST'])
def usun_pielgrzyma():
    if request.method == "POST":
        data_pielgrzymi = pielg.dane_pielgrzymi
        _id = request.form["id"]
        del data_pielgrzymi[_id]
        write_file(data_pielgrzymi, "pielgrzymi.json")
        return redirect('/pielgrzymi/')
    pielgrzym_id = request.args["pielgrzym-id"]
    data_pielg = read_file("pielgrzymi.json")[pielgrzym_id]
    return render_template("usun-pielgrzyma.html", pielgrzym=data_pielg, pielgrzym_id=pielgrzym_id)


@ app.route('/kto-tu-spi/', methods=['GET', 'POST'])
def kto_tu_spi():
    return render_template("kto-tu-spi.html", day=day[-1])


@ app.route('/przyporzadkuj-nocleg/', methods=['GET', 'POST'])
def daj_nocleg():
    lista_funkcyjn = pielg.lista_funkcyjnych
    lista_funkcyjn.sort(key=lambda lista_funkcyjn: lista_funkcyjn[6])
    lista_zwyk_pielg = pielg.lista_pozost_pielg
    lista_zwyk_pielg.sort(key=lambda lista_zwyk_pielg: lista_zwyk_pielg[6])
    lista_noclegow = accommod.lista_nocleg_data(day)
    if request.method == "POST":
        df = pd.DataFrame(list(request.form.items()), columns=['osoba', 'nocleg'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        headers = {
            'Content-Disposition': 'attachment; filename=output.xlsx',
            'Content-type': 'application/vnd.ms-excel'}
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    return render_template("przyporzadkuj-nocleg.html", day=day[-1], funkcyjni=lista_funkcyjn,
                           pozostali_pielgrzymi=lista_zwyk_pielg, lista_noclegow=lista_noclegow)
