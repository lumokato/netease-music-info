from sqlio import *
from webapi import *


if __name__ == '__main__':
    create_sql_artist()
    url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='
    req = {"id": 808044884, "offset": 0, "total": True, "limit": 1000, "n": 1000, "csrf_token": ''}
    data = encrypted_request(req)
    json = get_html(url, req)
    tracks = json['playlist']['tracks']
    for track in tracks:
        id_album = track['al']['id']
        urlx = 'http://music.163.com/api/album/' + str(id_album) + '?ext=true&id='\
                + str(id_album) + '&offset=0&total=true&limit=1000'
        data = get_html(urlx)
        id_artist = data['album']['artist']['id']
        name_artist = data['album']['artist']['name']
        insert_sql_artist(id_artist, name_artist)
    del_sql_artist(21138)

