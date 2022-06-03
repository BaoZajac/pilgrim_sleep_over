from flask import Flask, request, render_template, redirect, url_for
# from flask_sqlalchemy import SQLAlchemy
# from flask_alembic import Alembic
from main import read_file, write_file
from noclegi import noclegi


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

# db = SQLAlchemy(app)
dzien = "2022-08-03"        # TODO: zrobić uniwersalne dla każdej daty


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
    # print(lista_nocl)
    return render_template('main.html', noclegi_podsum=noclegi_podsum, dzien=dzien, mycie_podsum=mycie_podsum,
                           lista_nocl=lista_nocl, lista_mycie=lista_mycie)


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def nocleg():
    data_noclegi = read_file("noclegi.json")
    # data_address = list(data_noclegi.items())
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
        data_noclegi[nocleg_id] = last_name, given_name, town, street, house, apartment, phone, sleep, shower, comment
        write_file(data_noclegi, "noclegi.json")
    data_address = list(data_noclegi.items())
    if request.path == '/noclegi/':
        # return redirect(url_for('/noclegi/', data_address=data_address))
        return render_template("noclegi.html", data_address=data_address)
    elif request.path == '/dodaj-nocleg/':
        return render_template("dodaj-nocleg.html")


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
        data_pielgrzymi[pielgrzym_id] = last_name, given_name, small_group, function, accommodations, sex
        write_file(data_pielgrzymi, "pielgrzymi.json")
    data_pielgrzymi_lista = list(data_pielgrzymi.items())
    return render_template("pielgrzymi.html", pielgrzymi=data_pielgrzymi_lista, lista_funkcji=lista_funkcji,
                           lista_grupek=lista_grupek)


@app.route('/edytuj-pielgrzyma/', methods=['GET', 'POST'])
def edycja_pielgrzyma():
    if request.method == "POST":
        # write_file(data_pielgrzymi, "pielgrzymi.json")    # TODO: zrobić zapisywanie edytowanych danych
        return redirect('/pielgrzymi/')
    lista_funkcji = ["-", "bagażowy", "chorąży", "ekologiczny", "kwatermistrz", "medyczny", "pilot", "porządkowy",
                     "przewodnik", "schola", "szef", "techniczny"]
    lista_grupek = ["funkcyjni", 1, 2, 3, 4, 5, 6, 7, 8]
    pielgrzym_id = request.args["pielgrzym-id"]
    data_pielgrzym = read_file("pielgrzymi.json")[pielgrzym_id]
    grupka = data_pielgrzym[2]
    if grupka != "funkcyjni":
        grupka = int(grupka)
    lista_grupek.remove(grupka)
    funkcja = data_pielgrzym[3]
    lista_funkcji.remove(funkcja)
    return render_template("edycja-pielgrzyma.html", pielgrzym=data_pielgrzym, pielgrzym_id=pielgrzym_id,
                           lista_funkcji=lista_funkcji, lista_grupek=lista_grupek)


@app.route('/edytuj-nocleg/', methods=['GET', 'POST'])
def edycja_noclegu():
    if request.method == "POST":        # TODO: zrobić zapisywanie edytowanych danych
        return redirect('/noclegi/')
    nocleg_id = request.args["nocleg-id"]
    data_nocleg = read_file("noclegi.json")[nocleg_id]
    return render_template("edycja-noclegu.html", nocleg=data_nocleg, nocleg_id=nocleg_id)

