import urllib.request
import urllib
import re
import time
import random
import socket
import threading
from webapi import *


def get_html_new(url, req, proxy):
    hds = {'Cookie': 'os=pc; osver=Microsoft-Windows-8-Professional-build-9200-64bit; appver=1.5.0.75771;',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                         ' Chrome/35.0.1916.138 Safari/537.36',
           'Referer': 'http://music.163.com/'}
    # proxy = {'http': '183.159.87.111:18118'}
    data = encrypted_request(req)
    response = requests.post(url, headers=hds, data=data, proxies=proxy)
    html_data = response.json()
    return html_data

# 抓取代理IP
ip_totle = []
for page in range(1, 3):
    # url = 'http://ip84.com/dlgn/' + str(page)
    url='http://www.xicidaili.com/nn/'+str(page) #西刺代理
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"}
    request = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    print('get page', page)
    pattern = re.compile('<td>(\d.*?)</td>')  # 截取<td>与</td>之间第一个数为数字的内容
    ip_page = re.findall(pattern, str(content))
    ip_totle.extend(ip_page)
    time.sleep(random.choice(range(1, 3)))
# 打印抓取内容
print('代理IP地址     ', '\t', '端口', '\t', '速度', '\t', '验证时间')
for i in range(0, len(ip_totle), 4):
    print(ip_totle[i], '    ', '\t', ip_totle[i + 1], '\t', ip_totle[i + 2], '\t', ip_totle[i + 3])
# 整理代理IP格式
proxys = []
for i in range(0, len(ip_totle), 4):
    proxy_host = ip_totle[i] + ':' + ip_totle[i + 1]
    proxy_temp = {"http": proxy_host}
    proxys.append(proxy_temp)


# 验证代理IP有效性的方法
def test(i):
    socket.setdefaulttimeout(5)  # 设置全局超时时间
    url = "http://music.163.com/api/v1/resource/comments"  # 打算爬取的网址
    try:
        proxy_support = proxys[i]
        id_list = [500392152, 500392153, 500392154, 500392155, 500392156]
        for id_tracks in id_list:
            url_t = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + str(id_tracks)
            req_t = {"uid": id_tracks, "offset": "0", "csrf_token": "", "limit": "20"}
            data_t = get_html_new(url_t, req_t, proxy_support)['total']
        print(proxys[i], 'is OK')
        with open('proxy_ip.txt', 'a') as file:
            file.write('%s\n' % str(proxys[i]))  # 写入该代理IP
        file.close()
    except Exception as e:
        print(proxys[i], e)


if __name__ == '__main__':
    # 单线程验证
    '''for i in range(len(proxys)):
        test(i)'''
    # 多线程验证
    threads = []
    for i in range(len(proxys)):
        thread = threading.Thread(target=test, args=[i])
        threads.append(thread)
        thread.start()
    # 阻塞主进程，等待所有子线程结束
    for thread in threads:
        thread.join()
