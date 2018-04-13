import time
from webapi import *
from sqlio import *


# 根据歌曲id获取第一页评论
def get_comment_fp(id_track):
    # pages = 0
    # url_comment = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' \
    #               + str(id_track) + '?limit=20&offset=' + str(pages)
    url_comment = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(id_track)
    req_comment = {"uid": id_track, "offset": "0", "csrf_token": "", "limit": "20"}
    page_track = get_html(url_comment, req_comment)
    total_track_comment = page_track['total']
    # 将评论数信息存入 TABLE track
    upd_sql_track(id_track, total_track_comment)
    for dic_comment in page_track['comments']:
        id_comment = dic_comment['commentId']
        user_name = dic_comment['user']['nickname']
        user_id = dic_comment['user']['userId']
        user_vip = dic_comment['user']['vipType']
        like_count = dic_comment['likedCount']
        time_comment = dic_comment['time']
        content_comment = dic_comment['content']
        insert_sql_comment(id_comment, user_name, user_id, user_vip, like_count, time_comment, content_comment, id_track)
        if dic_comment['beReplied']:
            for replied_comment in dic_comment['beReplied']:
                replied_user_name = replied_comment['user']['nickname']
                replied_user_id = replied_comment['user']['userId']
                replied_content_comment = replied_comment['content']
            upd_sql_comment(id_comment, replied_user_name, replied_user_id, replied_content_comment)
    if total_track_comment < 20:
        upd_time_sql_comment(ids_track)
    return total_track_comment


# 获取后续页面评论
def get_comment_x(id_track_m, pages):
    offset = 20 * (pages + 1)
    # url_comment = 'http://music.163.com/api/v1/resource/comments/R_SO_4_' \
    #               + str(id_track) + '?limit=20&offset=' + str(pages)
    url_comment = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(id_track_m)
    req_comment = {"uid": id_track_m, "offset": offset, "csrf_token": "", "limit": "20"}
    page_track = get_html(url_comment, req_comment)
    for dic_comment in page_track['comments']:
        id_comment = dic_comment['commentId']
        user_name = dic_comment['user']['nickname']
        user_id = dic_comment['user']['userId']
        user_vip = dic_comment['user']['vipType']
        like_count = dic_comment['likedCount']
        time_comment = dic_comment['time']
        ct_comment = dic_comment['content']
        insert_sql_comment(id_comment, user_name, user_id, user_vip, like_count, time_comment, ct_comment, id_track_m)
        if dic_comment['beReplied']:
            for replied_comment in dic_comment['beReplied']:
                replied_user_name = replied_comment['user']['nickname']
                replied_user_id = replied_comment['user']['userId']
                replied_content_comment = replied_comment['content']
            upd_sql_comment(id_comment, replied_user_name, replied_user_id, replied_content_comment)


if __name__ == '__main__':
    list_track = get_sql_track()
    track_num = 17406
    while 1 == 1:
        ids_track = list_track[track_num-1][0]
        names_track = list_track[track_num-1][1]
        try:
            comment_count = get_comment_fp(ids_track)
            print(track_num, ids_track, names_track, comment_count)
            track_num += 1
            time.sleep(0.1)
        except Exception as e:
            print(track_num, ids_track, names_track, e)
            with open('track.txt', 'a') as file:
                file.write('%s,%s,%s,%s,%s\n' % (str(track_num), str(ids_track), names_track, str(e)))
            file.close()
            time.sleep(5)
