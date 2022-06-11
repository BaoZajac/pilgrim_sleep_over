from flask import Flask, request, render_template, redirect, url_for, Response, make_response
# from flask_sqlalchemy import SQLAlchemy
# from flask_alembic import Alembic
from main import read_file, write_file
from noclegi import noclegi
from uczestnicy import pielg
import pandas as pd
import io


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

# db = SQLAlchemy(app)
dzien = "2022-08-04"        # TODO: zrobić uniwersalne dla każdej daty


# # stworzenie tabeli z adresami
# class Address(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     last_name = db.Column(db.String(120), nullable=False)
#     given_name = db.Column(db.String(120), nullable=True)       #TODO: wypełnione musi być ALBO nazwisko ALBO imię
#     town = db.Column(db.String(120), nullable=False)
#     street = db.Column(db.String(120), nullable=True)
#     house = db.Column(db.String(120), nullable=False)
#     apartment = db.Column(db.String(120), nullable=True)
#     phone = db.Column(db.Integer, nullable=False)


@app.route('/')
def main():
    noclegi_podsum = noclegi.suma_nocl_data(dzien)
    mycie_podsum = noclegi.suma_pryszn_data(dzien)
    lista_nocl = noclegi.lista_nocleg_data(dzien)
    lista_mycie = noclegi.lista_prysznic_data(dzien)
    return render_template('main.html', noclegi_podsum=noclegi_podsum, dzien=dzien[-1], mycie_podsum=mycie_podsum,
                           lista_nocl=lista_nocl, lista_mycie=lista_mycie)


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def nocleg():
    data_noclegi = noclegi.dane_noclegi
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
        nocleg_lista = list(data_noclegi.keys())
        nocleg_lista = [int(el) for el in nocleg_lista]
        nocleg_id = max(nocleg_lista) + 1
        # date = noclegi.miejscowosc_na_data(town)
        # print(date)
        # print(type(date))
        data_noclegi[nocleg_id] = last_name, given_name, town, street, house, apartment, phone, sleep, shower, comment  #, date
        write_file(data_noclegi, "noclegi.json")
    data_address = list(data_noclegi.items())
    if request.path == '/noclegi/':
        return render_template("noclegi.html", data_address=data_address, dzien=dzien[-1])
    elif request.path == '/dodaj-nocleg/':
        return render_template("dodaj-nocleg.html")


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edycja_noclegu():
    if request.method == "POST":
        data_noclegi = noclegi.dane_noclegi
        _id = request.form["id"]
        dane_noc = dict(request.form)
        miejscowosc_przed = data_noclegi[_id][2]
        del dane_noc["id"]
        dane_noc = list(dane_noc.values())
        miejscowosc_po = dane_noc[2]
        if miejscowosc_przed != miejscowosc_po:
            data = noclegi.miejscowosc_na_data(miejscowosc_po)
            # dane_noc.append(data)
        data_noclegi[_id] = dane_noc
        write_file(data_noclegi, "noclegi.json")
        return redirect('/noclegi/')
    nocleg_id = request.args["nocleg-id"]
    data_nocleg = read_file("noclegi.json")[nocleg_id]
    return render_template("edycja-noclegu.html", nocleg=data_nocleg, nocleg_id=nocleg_id)


@app.route('/usun-nocleg/', methods=['GET', 'POST'])
def usun_nocleg():
    if request.method == "POST":
        data_noclegi = noclegi.dane_noclegi
        _id = request.form["id"]
        del data_noclegi[_id]
        write_file(data_noclegi, "noclegi.json")
        return redirect('/noclegi/')
    nocleg_id = request.args["nocleg-id"]
    data_nocleg = read_file("noclegi.json")[nocleg_id]
    return render_template("usun-nocleg.html", nocleg=data_nocleg, nocleg_id=nocleg_id)


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
                           lista_grupek=lista_grupek, dzien=dzien[-1])


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
    return render_template("kto-tu-spi.html", dzien=dzien[-1])


@ app.route('/przyporzadkuj-nocleg/', methods=['GET', 'POST'])
def daj_nocleg():
    lista_funkcyjn = pielg.lista_funkcyjnych
    lista_funkcyjn.sort(key=lambda lista_funkcyjn: lista_funkcyjn[6])
    lista_zwyk_pielg = pielg.lista_pozost_pielg
    lista_zwyk_pielg.sort(key=lambda lista_zwyk_pielg: lista_zwyk_pielg[6])
    lista_noclegow = noclegi.lista_nocleg_data(dzien)
    if request.method == "POST":
        df = pd.DataFrame(list(request.form.items()), columns=['osoba', 'nocleg'])
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        headers = {
            'Content-Disposition': 'attachment; filename=output.xlsx',
            'Content-type': 'application/vnd.ms-excel'}
        return Response(buffer.getvalue(), mimetype='application/vnd.ms-excel', headers=headers)
    return render_template("przyporzadkuj-nocleg.html", dzien=dzien[-1], funkcyjni=lista_funkcyjn,
                           pozostali_pielgrzymi=lista_zwyk_pielg, lista_noclegow=lista_noclegow)
