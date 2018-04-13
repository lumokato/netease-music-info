import csv
from sqlio import *
from webapi import *


# 根据歌手id获取专辑列表
def get_album(id_artist):
    url_artist = 'http://music.163.com/api/artist/albums/' + str(id_artist) + '?id='\
                 + str(id_artist) + '&offset=0&total=true&limit=1000'
    data_artist = get_html_pre(url_artist)
    for dic_album in data_artist['hotAlbums']:
        name_group = dic_album['artist']['name']
        id_group = dic_album['artist']['id']
        name_album = dic_album['name']
        id_album = dic_album['id']
        comment_url_album = dic_album['commentThreadId']
        # 将以上信息存入数据库album
        insert_sql_album(id_album, name_album, id_group, name_group, comment_url_album)


if __name__ == '__main__':
    # create_sql_album()
    # 根据 artist 列表获取 album 信息
    # dic_artist = get_sql_artist()
    # for id_a in dic_artist.keys():
    #     get_album(id_a)
    # 去除无关 album
    reader = csv.reader(open('album_del.csv', encoding='GB18030'))
    # for line in reader:
    #     del_sql_album(line[0])
    list_album = get_sql_album()
    print(len(list_album))




