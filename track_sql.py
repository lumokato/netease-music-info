import csv
from webapi import *
from sqlio import *


# 根据专辑id获取歌曲页面
def get_track(id_album):
    url_album = 'http://music.163.com/api/album/' + str(id_album) + '?ext=true&id='\
                + str(id_album) + '&offset=0&total=true&limit=1000'
    data_album = get_html_pre(url_album)
    comment_count_album = data_album['album']['info']['commentCount']
    share_count_album = data_album['album']['info']['shareCount']
    size_album = data_album['album']['size']
    # 将以上信息存入数据库album
    upd_sql_album(id_album, comment_count_album, share_count_album, size_album)
    id_artist = data_album['album']['artist']['id']
    name_artist = data_album['album']['artist']['name']
    name_album = data_album['album']['name']
    for dic_track in data_album['album']['songs']:
        popularity_track = dic_track['popularity']
        comment_url_track = dic_track['commentThreadId']
        duration_track = dic_track['duration']
        copyright_track = dic_track['copyrightId']
        artists_track = []
        for dic_artist in dic_track['artists']:
            artists_track.append(dic_artist['name'])
        name_track = dic_track['name']
        id_track = dic_track['id']
        position_track = dic_track['position']
        # 将以上信息存入数据库track(加上歌曲在专辑的次序数）
        insert_sql_track(id_track, name_track, id_album, name_album, id_artist, name_artist, popularity_track,
                         comment_url_track, duration_track, copyright_track, position_track)


if __name__ == '__main__':
    # add_sql_album()
    # create_sql_track()
    # 以下为网站获取内容
    # dic_album = get_sql_album()
    # album_count = 0
    # for ids_album in dic_album.keys():
    #     album_count += 1
    #     if album_count > 7111:
    #         print(album_count, ids_album, dic_album[ids_album])
    #         get_track(ids_album)
    # reader = csv.reader(open('track_th.csv', encoding='UTF-8'))
    list_track = get_sql_track()
    print(len(list_track))
