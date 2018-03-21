import os
import sys
import re
import time
import types
import requests

id_artist = '22033'


# 获取网页信息
def get_html(url):
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    content = requests.get(url, headers=hds)
    html_data = content.json()
    return html_data


def get_album(id_artist):
    url_artist = 'http://music.163.com/api/artist/albums/' + str(id_artist) + '?id='\
                 + str(id_artist) + '&offset=0&total=true&limit=1000'
    data_artist = get_html(url_artist)
    for dic_album in data_artist['hotAlbums']:
        name_group = dic_album['artist']['name']
        id_group = dic_album['artist']['id']
        name_album = dic_album['name']
        id_album = dic_album['id']
        comment_url = dic_album['commentThreadId']
        print(name_album)
get_album(id_artist)

def getAlbumList(id_Group):
    url_Group = 'http://music.163.com/api/artist/albums/' + str(id_Group) + '?id=' + str(
        id_Group) + '&offset=0&total=true&limit=1000'
    page_Group = get_html(url_Group)
    # 反向寻找专辑id
    reg0 = r'"buSsi"(.+?)"eman"'
    abmdata = getRegex(reg0, page_Group.decode()[::-1])
    abmlist = []
    for abms in abmdata:
        abms = abms[::-1]
        abmnm = getRegex('"(.+?)","id', abms)[0]
        abmid = getRegex('"id":(\d+),', abms)[0]
        abmlist.append([abmnm, abmid])
    return abmlist


# 根据专辑id获取歌词页面
def getTrackList(id_Album, savetxt):
    url_Album = 'http://music.163.com/api/album/' + str(id_Album) + '?ext=true&id=' + str(
        id_Album) + '&offset=0&total=true&limit=1000'
    page_album = getHtml(url_Album)
    page_rev = page_album.decode()[::-1]
    reg1 = r'"R_SO_4_(\d+)"'
    songid_total = getRegex(reg1, page_album.decode())
    # writelinez = []
    for songid in songid_total:
        song_name = getRegex(songid[::-1] + r':"di","(.+?)"', page_rev)[0][::-1]


def songpage(sid, sname, savetxt):
    writelinez = ['\n\n################################\n\n', sname,
                  '\n\n#####################################\n\n']
    url_Track = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(sid) + '&lv=-1&kv=-1&tv=-1'
    page_song = getHtml(url_Track)
    if len(page_song) > 150:
        try:
            print(sname)
            writelinez.extend(lrctotxt(page_song.decode()))
            with open(savetxt, 'a', encoding='utf-8') as file:
                for writex in writelinez:
                    file.write('%s' % (writex))
        except (KeyError, IndexError):
            appenddoc('rubbish', str(sid) + '\n')