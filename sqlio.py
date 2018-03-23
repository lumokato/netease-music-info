import pymysql
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'suzto',
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
    sql = 'SELECT * FROM `album_artist` WHERE 1=1'
    try:
        cursor.execute(sql)
        for user in cursor:
            artist_data[user['id']] = user['name']
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


