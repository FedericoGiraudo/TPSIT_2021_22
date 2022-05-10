import flask
import requests
import sqlite3
while True:
    id=input("inserisci il client id(client_1,client_2): ")
    r=requests.get(f'http://127.0.0.1:5000/api/v1/resurces/operazione?id={id}')
    data=r.json()
    if data['state']==0:
        break
    risultato=eval(data['op'])
    id_op=data['id']
    requests.get(f'http://127.0.0.1:5000/api/v1/resurces/risultato?id={id_op}&ris={risultato}')