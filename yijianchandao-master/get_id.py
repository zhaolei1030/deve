import requests
import json
from datetime import datetime

def get_id_title(product):
    """
    登录cd界面，获取cd的id
    :param product:
    :return:
    """
    url = 'http://chandao_url.com'
    account = 'xxxxxx'
    password = 'xxxxxx'
    session = requests.session()
    path = '/pro/user-login.html'
    session.post(url=url + path, data={"account": account, "password": password})
    path = '/pro/index.html'
    session.post(url=url + path, data={"account": account, "password": password})
    path = '/pro/bug-browse-{}.json'.format(product)
    content = session.get(url=url + path)
    content = content.text
    content = json.loads(content)
    content = json.loads(content['data'])
    for i in content['bugs'][0:1]:
        id = i['id']
        title = i['title']
        return id, title
if __name__ == '__main__':
    print(get_id_title(93))
