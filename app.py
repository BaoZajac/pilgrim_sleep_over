from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method == "POST":
        last_name = request.form["last_name"]
        given_name = request.form["given_name"]
        town = request.form["town"]
        street = request.form["street"]
        house = request.form["house"]
        apartment = request.form["apartment"]
        phone = request.form["phone"]
    return render_template("form-noclegi.html")