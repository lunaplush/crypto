"""
функции модуля обеспечивают работу с FastApi
"""
import requests

def git_list_news(keyword, date_begin, date_end):
    """
    Функция возвращает списко новостей за период по ключевому слову
    :param keyword: ключевое слово
    :param date_begin: начала периода
    :param date_end: конец периода
    :return:
    """
    url = 'http://news.fvds.ru:5000/news'
    params = {
        'keyword': keyword,
        'date_start': date_begin,
        'date_end': date_end,
        'limit': 0
    }
    headers = {
        'accept': 'application/json',
        'content-type': 'application/json',
    }
    return requests.get(url, headers=headers, params=params)