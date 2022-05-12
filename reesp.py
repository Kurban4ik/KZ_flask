import requests
date = {
    'login': 'kira297@bk.ru',
    'password': '123123',
    'filter': '3',
    'is_private': '0'
}
files = {
    'file': open('asd.jpg', 'rb')
}
print(requests.post('http://127.0.0.1:5000/api/news', data=date, files=files).json())