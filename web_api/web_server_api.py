import flask
from flask import jsonify, request
import sqlite3

app =flask.Flask(__name__)
app.config["DEBUG"] =True

@app.route('/api/v1/resurces/books/all', methods=['GET'])
def api_all():
   return jsonify()


@app.route('/', methods=['GET'])
def home():
    return "<h1>Biblioteca online</h1><p>Prototipo di web API.</p>"


@app.route('/api/v1/resurces/books', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field Provided. Please specify an id "
    results = []

    con=sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\libri.db')
    cur = con.cursor()
    results = cur.execute(f"SELECT title FROM books WHERE id={id}")
    con.commit()
    con.close
    print(results[0])
    #return jsonify(results[0])

app.run()