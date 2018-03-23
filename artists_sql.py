import requests
from webapi import *






if __name__ == '__main__':
    # headers = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
    #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
    #                          ' Chrome/35.0.1916.138 Safari/537.36',
    #            'Referer': 'http://music.163.com/'}
    # url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='
    # req = {"id": 808044884, "offset": 0, "total": True, "limit": 1000, "n": 1000, "csrf_token": ''}
    # data = encrypted_request(req)
    # response = requests.post(url, headers=headers, data=data)
    # json = response.json()
    # tracks = json['playlist']['tracks']
    # create_sql_album()
    # for track in tracks:
    #     id_album = track['al']['id']
    #     urlx = 'http://music.163.com/api/album/' + str(id_album) + '?ext=true&id='\
    #             + str(id_album) + '&offset=0&total=true&limit=1000'
    #     data = get_html(urlx)
    #     id = data['album']['artist']['id']
    #     name = data['album']['artist']['name']
    #     insert_album(id, name)
    datda = get_album_id_mysql()
    print('0')
