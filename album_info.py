import os
import sys
import re
import time
import types
import requests
from webapi import *


# 根据歌手id获取专辑列表
def get_album(id_artist):
    url_artist = 'http://music.163.com/api/artist/albums/' + str(id_artist) + '?id='\
                 + str(id_artist) + '&offset=0&total=true&limit=1000'
    data_artist = get_html_pre(url_artist)
    id_list_album = []
    for dic_album in data_artist['hotAlbums']:
        name_group = dic_album['artist']['name']
        id_group = dic_album['artist']['id']
        name_album = dic_album['name']
        id_album = dic_album['id']
        comment_url_album = dic_album['commentThreadId']
        # 将以上信息存入数据库album
        id_list_album.append(id_album)
    return id_list_album


# 根据专辑id获取歌曲页面
def get_track(id_album):
    url_album = 'http://music.163.com/api/album/' + str(id_album) + '?ext=true&id='\
                + str(id_album) + '&offset=0&total=true&limit=1000'
    data_album = get_html_pre(url_album)
    comment_count_album = data_album['album']['info']['commentCount']
    share_count_album = data_album['album']['info']['shareCount']
    size_album = data_album['album']['size']
    # 将以上信息存入数据库album
    id_list_track = []
    for dic_track in data_album['album']['songs']:
        popularity_track = dic_track['popularity']
        comment_count_track = dic_track['commentThreadId']
        duration_track = dic_track['duration']
        copyright_track = dic_track['copyrightId']
        artists_track = []
        for dic_artist in dic_track['artists']:
            artists_track.append(dic_artist['name'])
        name_track = dic_track['name']
        id_track = dic_track['id']
        position_track = dic_track['position']
        # 将以上信息存入数据库track(加上歌曲在专辑的次序数）
        id_list_track.append(id_track)
    return id_list_track


# 根据歌曲id获取评论
def get_comment(id_track):
    pages = 0
    url_comment = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' \
                  + str(id_track) + '?limit=20&offset=' + str(pages)
    # url_comment = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(id_track)
    # url = "http://music.163.com/weapi/v1/resource/comments/R_SO_4_30251507/?csrf_token="
    # first_param = {"uid": "30251508", "offset": "0", "csrf_token": "", "limit": "20"}
    # url_lyric = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(sid) + '&lv=-1&kv=-1&tv=-1'
    page_track = get_html_pre(url_comment)
    total_track_comment = page_track['total']
    return total_track_comment


if __name__ == '__main__':
    id_test = '30251507'
    # get_track(id_test)
    # get_album(id_test)
    get_comment(id_test)


