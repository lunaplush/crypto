import requests
 
 
url = 'http://news.fvds.ru:5000/news'
params = {
    'keyword': 'btc',
}
headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    
}

response = requests.get(url, headers=headers, params=params)
print(response.content)