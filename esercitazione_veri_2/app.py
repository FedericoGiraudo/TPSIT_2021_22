from lib2to3.pygram import Symbols
from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
import socket as sck
from sympy import *
app = Flask(__name__)

def calc(utente,funzione,incognita,estremo_min,estremo_max):  
    if(estremo_max != ""):
        risultato = integrate(funzione,(incognita,estremo_min,estremo_max))
    else:
        risultato = integrate(funzione,incognita)
       
    con = sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\esercitazione_veri_2\movimenti.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Calcoli(utente,funzione,incognita,estremo_min,estremo_max,risultato) VALUES ('{utente}','{funzione}','{incognita}','{estremo_min}','{estremo_max}','{risultato}')")
    con.commit()
    con.close
    return risultato
           
@app.route("/", methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        username_c = request.cookies.get('username')
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion ==False:
            error = 'Invalid Credentials. Please try again.'
        else:  
            if username_c==None:
                resp = make_response(render_template('index.html'))
                resp.set_cookie('username', username)
                return resp  
            return redirect(url_for('index')) 
    return render_template('login.html', error=error)

def validate(username, password):
    print("dddddd")
    completion = False
    con = sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\esercitazione_veri_2\movimenti.db')
    #with sqlite3.connect('static/db.db') as con:
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route("/calcolo", methods=['GET', 'POST'])
def index():
    output = None
    
    if request.method == 'POST':
        funzione= request.form['funzione']
        incognita = request.form['incognita']
        estremo_min = request.form['estremo_min']
        estremo_max = request.form['estremo_max']

        incognita =symbols(incognita)
        init_printing(use_unicode = True)

        utente = request.cookies.get('username')
        risultato = calc(utente,funzione,incognita,estremo_min,estremo_max)

        return render_template('index.html', output=risultato)
    return render_template('index.html')

if __name__ == '__main__':   
    app.run(debug=True, host="0.0.0.0")