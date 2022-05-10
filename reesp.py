import requests
files = {
    'file': open('unknown.png', 'rb')
}
data = {
    'login': 'kira297@bk.ru',
    'password': '123123'
}
print(requests.post('http://127.0.0.1:5000/api/news', data=data, files=files).json())