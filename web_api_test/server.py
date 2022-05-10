import random
import flask
from flask import jsonify, request
import sqlite3

app =flask.Flask(__name__)
app.config["DEBUG"] =True

@app.route('/api/v1/resurces/operazione', methods=['GET'])
def api_id():
    if 'id' in request.args:
        id = request.args['id']
    else:
        return "Error: No id field Provided. Please specify an id "

    con=sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\web_api_test\operation.db')
    cur = con.cursor()
    cur.execute(f"SELECT op_mate,id_op FROM operazioni WHERE client_id='{id}' AND risultato_op is NULL")
    rows = cur.fetchall()
    if len(rows)==0:
        operazione = {'id':'','op':'','state':0}
        return jsonify(operazione)
    r = random.choice(rows)
    id=r[1]
    op=r[0]
    operazione = {'id':id,'op':op,'state':1}
    con.commit()
    con.close
    return jsonify(operazione)

@app.route('/api/v1/resurces/risultato', methods=['GET'])
def api_ris():
    if 'ris' in request.args and 'id' in request.args :
        ris = request.args['ris']
        id_op =request.args['id']
    else:
        return "Error: No id field Provided. Please specify an id "

    con=sqlite3.connect('C:\A1_DATA\ITIS_2021_22\Tpsit\Python\web_api_test\operation.db')
    cur = con.cursor()
    cur.execute(f"UPDATE operazioni SET risultato_op='{ris}' WHERE id_op={id_op}")
    con.commit()
    con.close
    return 'ok'
    
app.run()