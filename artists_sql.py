import requests
from webapi import *
import pymysql


config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'db': 'test0',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}


def create_sql_album():
    db = pymysql.connect(**config)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS album_artist")
    cursor.execute('SET NAMES UTF8')
    cursor.execute("SET CHARACTER_SET_CLIENT=utf8")
    cursor.execute("SET CHARACTER_SET_RESULTS=utf8")
    # 使用预处理语句创建表
    sql = """CREATE TABLE album_artist ( 
             id  INT(20) NOT NULL, 
             name  CHAR(200) NOT NULL
             )"""
    cursor.execute(sql)
    print("CREATE TABLE OK")
    # 关闭数据库连接
    db.close()


# 将用户（id,name,comment）添加到user_comment数据中
def insert_album(id, nam):
    # Connect to the database
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO album_artist (id, name) VALUES (%s, %s)"
    try:
        # 执行sql语句
        cursor.execute(sql, (id, nam))
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        print('Error', e)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


# 从user_comment数据库中获取用户的个人（id，name）,并返回user_data列表
def get_album_id_mysql():
    user_data = []
    # Connect to the database
    db = pymysql.connect(**config)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = 'SELECT * FROM album_artist WHERE 1'
    try:
        # 执行sql语句
        cursor.execute(sql)
        for user in cursor:
            user_id_name = {'id': '0', 'name': '0'}
            id = user['id']
            name = user['name']
            user_id_name['id'] = id
            user_id_name['name'] = name
            if user_id_name not in user_data:
                user_data.append(user_id_name)
        # 提交到数据库执行
        db.commit()
        return user_data
    except Exception as e:
        print('Error', e)
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


def get_html(url):
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    proxy = {
        'http': '221.0.232.13:61202'
    }
    content = requests.get(url, headers=hds, timeout=20)
    html_data = content.json()
    return html_data


if __name__ == '__main__':
    headers = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/35.0.1916.138 Safari/537.36',
               'Referer': 'http://music.163.com/'}
    url = 'http://music.163.com/weapi/v3/playlist/detail?csrf_token='
    req = {"id": 808044884, "offset": 0, "total": True, "limit": 1000, "n": 1000, "csrf_token": ''}
    data = encrypted_request(req)
    response = requests.post(url, headers=headers, data=data)
    json = response.json()
    tracks = json['playlist']['tracks']
    create_sql_album()
    for track in tracks:
        id_album = track['al']['id']
        urlx = 'http://music.163.com/api/album/' + str(id_album) + '?ext=true&id='\
                + str(id_album) + '&offset=0&total=true&limit=1000'
        data = get_html(urlx)
        id = data['album']['artist']['id']
        name = data['album']['artist']['name']
        insert_album(id, name)
