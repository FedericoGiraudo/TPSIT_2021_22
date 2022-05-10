import requests

r=requests.get('http://localhost:5000/get_image')
file=open("./downloaded.jpg", "wb")
file.write(r.content)
file.close()