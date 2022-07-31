#encoding: utf-8
"""
工具方法
"""
import requests
import logging


def save_html(html: str, file, encoding='utf-8'):
    """
    保存html
    """
    with open(file, 'w', encoding=encoding) as fout:
        fout.write(html)


def get_html(url: str, encoding='utf-8') -> str:
    """
    模拟浏览器打开html
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
    resp = requests.get(url, headers=headers)
    logging.info(f'get {url}, response code is {resp.status_code}.')
    return resp.content.decode(encoding)