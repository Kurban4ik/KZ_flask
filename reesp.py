import requests

files = {'file': open("input.jpg", "rb")}

param = {'login': 'kira297@bk.ru', 'password': '123123', 'filter': '3'}
print(requests.post(f'http://127.0.0.1:5000/api/news', data=param, files=files).json(), )
