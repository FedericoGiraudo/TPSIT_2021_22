import requests
r = requests.get('https://www.ralphlauren.it/it/wishlist')
print(r.text)
print(r.text) # contenuto della risposta HTTP
print(r.json) # oggetto JSON
print(r.status_code) # codice di status
print(r.headers) # informazione contenuta negli headers della risposta
print(r.history) # informazioni sui reindirizzamenti