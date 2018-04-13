import datetime
import pymysql
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'password',
    'db': 'netease_music',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


# 创建 TABLE artist
def create_sql_artist():
    # 连接 database
    db = pymysql.connect(**config)
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS `artist`")
    # 使用预处理语句创建表
    sql = """CREATE TABLE `artist` ( 
             id_artist  INT(10) NOT NULL, 
             name_artist  VARCHAR(40) NOT NULL,
             PRIMARY KEY (id_artist)
             )"""
    cursor.execute(sql)
    print("CREATE TABLE artist OK")
    # 关闭数据库连接
    db.close()


# 将 artist 信息添加到TABLE中
def insert_sql_artist(id_artist_insert, name_artist_insert):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO `artist` (id_artist, name_artist) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (id_artist_insert, name_artist_insert))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 从数据库中获取 artist 信息, 并返回字典
def get_sql_artist():
    artist_data = {}
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = 'SELECT * FROM `artist` WHERE 1=1'
    try:
        cursor.execute(sql)
        for user in cursor:
            artist_data[user['id_artist']] = user['name_artist']
        db.commit()
        return artist_data
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 删除 artist 中数据
def del_sql_artist(id_del):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "DELETE FROM `artist` WHERE id_artist = %s" % id_del
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 创建 TABLE album
def create_sql_album():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `album`")
    sql = """CREATE TABLE `album` ( 
             id_album  INT(10) NOT NULL, 
             name_album  VARCHAR(80) NOT NULL,
             id_artist  INT(10) NOT NULL, 
             name_artist  VARCHAR(40) NOT NULL,
             comment_url_album  VARCHAR(20),
             PRIMARY KEY (id_album)
             )"""
    cursor.execute(sql)
    print("CREATE TABLE album OK")
    db.close()


# 将 album 信息添加到TABLE中
def insert_sql_album(id_album, name_album, id_group, name_group, comment_url_album):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO `album` (id_album, name_album, id_artist, " \
          "name_artist, comment_url_album) VALUES (%s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (id_album, name_album, id_group, name_group, comment_url_album))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 从数据库中获取 album 的 id 与 name 信息, 并返回字典
def get_sql_album():
    album_data = {}
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = 'SELECT * FROM `album` WHERE 1=1'
    try:
        cursor.execute(sql)
        for user in cursor:
            album_data[user['id_album']] = user['name_album']
        db.commit()
        return album_data
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 删除 album 中数据
def del_sql_album(id_del):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "DELETE FROM `album` WHERE id_album = %s" % id_del
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 增加 album 表的新列
def add_sql_album():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "ALTER TABLE `album` ADD COLUMN size_album INT(5) NOT NULL"
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 更新 album 表的信息
def upd_sql_album(id_album, comment_count_album, share_count_album, size_album):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "UPDATE `album` SET comment_count_album = %s, share_count_album = %s, size_album = %s WHERE id_album = %s"
    try:
        cursor.execute(sql, (comment_count_album, share_count_album, size_album, id_album))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 创建 TABLE track
def create_sql_track():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `track`")
    sql = """CREATE TABLE `track` ( 
             id_track  INT(10) NOT NULL, 
             name_track  VARCHAR(80) NOT NULL,
             id_album  INT(10) NOT NULL, 
             name_album  VARCHAR(80) NOT NULL,
             id_artist  INT(10) NOT NULL, 
             name_artist  VARCHAR(40) NOT NULL,
             popularity_track  FLOAT(4,1),
             comment_url_track  VARCHAR(20),
             duration_track  INT(10),
             copyright_track  INT(10),
             position_track  INT(5) NOT NULL,
             comment_count_track INT(10),
             PRIMARY KEY (id_track)
             )"""
    cursor.execute(sql)
    print("CREATE TABLE track OK")
    db.close()


# 将 track 信息添加到TABLE中
def insert_sql_track(id_track, name_track, id_album, name_album, id_artist, name_artist, popularity_track,
                     comment_url_track, duration_track, copyright_track, position_track):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO `track` (id_track, name_track, id_album, name_album, id_artist, name_artist," \
          " popularity_track, comment_url_track, duration_track, copyright_track, position_track)" \
          " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (id_track, name_track, id_album, name_album, id_artist, name_artist, popularity_track,
                             comment_url_track, duration_track, copyright_track, position_track))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 从数据库中获取 track 的 id 信息, 并返回列表
def get_sql_track():
    album_data = []
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = 'SELECT * FROM `track` WHERE 1=1'
    try:
        cursor.execute(sql)
        for user in cursor:
            album_data.append([user['id_track'], user['name_track']])
        db.commit()
        return album_data
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 删除 album 中数据
def del_sql_track(id_del):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "DELETE FROM `track` WHERE id_track = %s" % id_del
    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 更新 track 中评论总数信息
def upd_sql_track(id_track, total_track_comment):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "UPDATE `track` SET comment_count_track = %s WHERE id_track = %s"
    try:
        cursor.execute(sql, (total_track_comment, id_track))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 创建 TABLE comment
def create_sql_comment():
    db = pymysql.connect(**config)
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS `comment`")
    sql = """CREATE TABLE `comment` (
             id_comment  INT(10) NOT NULL,
             user_name  VARCHAR(50) NOT NULL,
             user_id  INT(10) NOT NULL,
             user_vip INT(2) NOT NULL,
             like_count INT(6) NOT NULL,
             time_comment BIGINT(15) NOT NULL,
             content_comment VARCHAR(200) NOT NULL,
             replied_user_name  VARCHAR(50),
             replied_user_id  INT(10),
             replied_content_comment  VARCHAR(200),
             id_track  INT(10) NOT NULL,
             name_track  VARCHAR(80),
             id_album  INT(10), 
             name_album  VARCHAR(80),
             id_artist  INT(10), 
             name_artist  VARCHAR(40),
             CONSTRAINT track_comment PRIMARY KEY (id_comment, id_track)
             )"""
    cursor.execute(sql)
    print("CREATE TABLE comment OK")
    db.close()


# 将 comment 信息添加到TABLE中
def insert_sql_comment(id_comment, user_name, user_id, user_vip, like_count, time_comment, content_comment, id_track):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "INSERT INTO `comment` (id_comment, user_name, user_id, user_vip, like_count, time_comment," \
          " content_comment, id_track) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        cursor.execute(sql, (id_comment, user_name, user_id, user_vip, like_count, time_comment, content_comment, id_track))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


# 更新 comment 的被回复信息
def upd_sql_comment(id_comment, replied_user_name, replied_user_id, replied_content_comment):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "UPDATE `comment` SET replied_user_name = %s, replied_user_id = %s, " \
          "replied_content_comment = %s WHERE id_comment = %s"
    try:
        cursor.execute(sql, (replied_user_name, replied_user_id, replied_content_comment, id_comment))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()


def upd_time_sql_comment(id_track):
    db = pymysql.connect(**config)
    cursor = db.cursor()
    sql = "UPDATE `track` SET update_time = %s WHERE id_track = %s"
    try:
        cursor.execute(sql, (str(datetime.datetime.now()), id_track))
        db.commit()
    except Exception as e:
        print('Error', e)
        db.rollback()
    db.close()
