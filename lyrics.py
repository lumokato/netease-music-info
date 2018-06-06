import os
import sys
import urllib
import re
import time
import types
import urllib.request
#去除文件名显示错误
def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/\:*?"<>|'
    new_title = re.sub(rstr, "__", title)
    return new_title

#读取指定路径的文件
def getdoclist(docpath):
    docdata = open(docpath)
    doclist = docdata.read( ).splitlines( )
    return doclist

#获取网页信息
def getHtml(url):
    
    hds = {'Cookie' : 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.138 Safari/537.36',
           'Referer' : 'http://music.163.com/' }  
    request = urllib.request.Request(url,headers=hds)
    page = urllib.request.urlopen(request)
    html = page.read()
    return html

def savedoc(filepath,content):
    f = open(filepath,'w')
    f.write(content)
    f.close()

def appenddoc(filepath,content):
    f = open(filepath,'a')
    f.write(content)
    f.close()

def getRegex(regex,data):
    dat = re.compile(regex)
    ret = re.findall(dat,data)
    return ret

def getCited(sen):
    reg = r'"([^\"]+)\"'
    kw = re.compile(reg)
    kword = re.findall(kw,sen)
    if kword:
        return kword

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value/1000)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

#根据社团id获取专辑列表
def getAlbumList(id_Group):
    url_Group = 'http://music.163.com/api/artist/albums/'+ str(id_Group) +'?id=' + str(id_Group) + '&offset=0&total=true&limit=1000'
    page_Group = getHtml(url_Group)
    #反向寻找专辑id
    reg0 = r'"buSsi"(.+?)"eman"'
    abmdata = getRegex(reg0,page_Group.decode()[::-1])
    abmlist = []
    for abms in abmdata:
        abms = abms[::-1]
        abmnm = getRegex('"(.+?)","id',abms)[0]
        abmid = getRegex('"id":(\d+),',abms)[0]
        abmlist.append([abmnm,abmid])
    return abmlist

#根据专辑id获取歌词页面
def getTrackList(id_Album, group_name, album_name):
    url_Album = 'http://music.163.com/api/album/' + str(id_Album) + '?ext=true&id=' + str(id_Album) + '&offset=0&total=true&limit=1000'
    page_album = getHtml(url_Album)
    page_rev = page_album.decode()[::-1]
    reg1 = r'"R_SO_4_(\d+)"'
    songid_total = getRegex(reg1,page_album.decode())
    #writelinez = []
    for songid in songid_total:
        song_name = getRegex(songid[::-1] + r':"di","(.+?)"',page_rev)[0][::-1]
        url_Track = 'http://music.163.com/api/song/lyric?os=pc&id=' + str(songid) + '&lv=-1&kv=-1&tv=-1'
        page_song =  getHtml(url_Track)
        if len(page_song) > 150:
            try:
                print(song_name)
                user_info = lrctotxt(page_song.decode(), group_name, album_name, song_name)
                with open('user_info','a',encoding='utf-8') as file:
                    file.write(user_info)
            except (KeyError,IndexError):
                appenddoc('rubbish',str(songid)+'\n')

#根据歌词页面转化为用户详细信息
def lrctotxt(songpage, group_name, album_name, track_name):
    tlrc = getRegex(r'"tlyric":{(.*?}),"',songpage)[0]
    lyric_user = ''
    lyric_time = ''
    tran_user = ''
    tran_time = ''
    lyric_det = getRegex(r'"lyricUser":{.+?}',songpage)
    if lyric_det:
        lyric_user = getRegex(r'"nickname":"(.+?)"',lyric_det[0])[0]
        lyric_time_str = getRegex(r'"uptime":(.+?)}',lyric_det[0])[0]
        lyric_time = timestamp_datetime(int(lyric_time_str))
    #在有翻译时
    if tlrc != '"version":0,"lyric":null}':
        tran_det = getRegex(r'"transUser":{.+?}',songpage)
        if tran_det:
            tran_user = getRegex(r'"nickname":"(.+?)"',tran_det[0])[0]
            tran_time_str = getRegex(r'"uptime":(.+?)}',tran_det[0])[0]
            tran_time = timestamp_datetime(int(tran_time_str))
    writeline = '"%s","%s","%s","%s","%s","%s","%s"\n'%(group_name, album_name, track_name, tran_user, tran_time, lyric_user, lyric_time)
    return writeline

#进行文本输出
def saveAll(groupnum):
    group = open('GroupId','rb').readlines()[groupnum]
    groupname = getCited(group.decode())[0]
    print(groupname)
    groupid = getCited(group.decode())[1]
    albumlist = getAlbumList(groupid)
    for albums in albumlist:
        albumname = albums[0]
        albumid = albums[1]
        getTrackList(albumid, groupname, albumname)

#getTrackList(82840,"test")
#print(getAlbumList(19783)[1][0])
if __name__ == '__main__':
    for i in range(126):
        saveAll(i)

