from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic
from main import read_db, write_db


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_accountant.db"

db = SQLAlchemy(app)

adresy = []


# stworzenie tabeli z adresami
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(120), nullable=False)
    given_name = db.Column(db.String(120), nullable=True)       #TODO: wypełnione musi być ALBO nazwisko ALBO imię
    town = db.Column(db.String(120), nullable=False)
    street = db.Column(db.String(120), nullable=True)
    house = db.Column(db.String(120), nullable=False)
    apartment = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.Integer, nullable=False)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/dodaj-nocleg/', methods=['POST', 'GET'])
@app.route('/noclegi/', methods=['POST', 'GET'])
def nocleg():
    data = read_db()
    data_address = list(data.items())
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        town = request.form["town"]
        street = request.form["street"]
        house = request.form["house"]
        apartment = request.form["apartment"]
        phone = request.form["phone"]
        # lista = (last_name, given_name, town, street, house, apartment, phone)
        # adresy.append(lista)
        nocleg_id = int(max(list(data.keys()))) + 1
        data[nocleg_id] = last_name, given_name, town, street, house, apartment, phone
        write_db(data)
    if request.path == '/noclegi/':
        # return redirect(url_for('/noclegi/', data_address=data_address))
        return render_template("noclegi.html", data_address=data_address)
    elif request.path == '/dodaj-nocleg/':
        return render_template("dodaj-nocleg.html")


@app.route('/pielgrzymi/', methods=['GET', 'POST'])
def pielgrzym():
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        small_group = request.form["small_group"]
        function = request.form["function"]
    return render_template("pielgrzymi.html")




