from http.client import NETWORK_AUTHENTICATION_REQUIRED
from flask import Flask, render_template, request, redirect, url_for, make_response
import sqlite3
from pathlib import Path
import numpy as np

app = Flask(__name__)
         
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
    
    completion = False
    con = sqlite3.connect('C:/A1_DATA/ITIS_2021_22/Tpsit/Python/Giraudo_Federico/stati.db')
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
    
def network():
    con = sqlite3.connect('C:/A1_DATA/ITIS_2021_22/Tpsit/Python/Giraudo_Federico/stati.db')
    cur = con.cursor()
    cur.execute("SELECT COUNT(id) FROM Stato")
    rows = cur.fetchall()
    st_casuale = np.random.randint(0,rows)
    cur.execute(f"SELECT stato FROM Stato WHERE id='{st_casuale[0][0]}'")
    stato = cur.fetchall() 
    print(stato[0])      
    con.commit()
    con.close()
    return stato[0]
    
@app.route("/social", methods=['GET', 'POST'])
def index():
    output = None 
    if request.method == 'POST':
        stato= request.form['stato']
        if len(stato)>80:
            errore= 'Stato troppo lungo'
            return render_template('index.html', errore=errore)
        else:
            utente = request.cookies.get('username')
            con = sqlite3.connect('C:/A1_DATA/ITIS_2021_22/Tpsit/Python/Giraudo_Federico/stati.db')
            cur = con.cursor()
            cur.execute(f"INSERT INTO Stato(utente,stato) VALUES ('{utente}','{stato}')")
            con.commit()
            con.close
            estrazione= network()
        
        return render_template('index.html', output=estrazione)
    return render_template('index.html')

if __name__ == '__main__':   
    app.run(debug=True, host="0.0.0.0")