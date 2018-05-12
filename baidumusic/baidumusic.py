# coding=utf-8
import requests
import re
import json


def get_urls(song_id):
    # 把sid拼接进请求链接
    #     url = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17205500581185420972_1513324047403&songid=%s&_=1513324048127' % song_id
    url = 'http://music.baidu.com/data/tingapi/v1/restserver/ting?method=baidu.ting.song.play&songid=%s' % song_id
    data = requests.get(url).text  # 获取请求信息文本   str
    # data = re.findall(r'\((.*)\)', data)[0]  # 使用第一个url,返回数据需要去掉圆括号
    data = json.loads(data)  # 转为json格式    dict
    music_msg = {}
    music_msg['title'] = data['songinfo']['title']  # 获取歌曲名称
    music_msg['singer'] = data['songinfo']['author']
    music_msg['song_url'] = data['bitrate']['file_link']  # 获取下载链接
    return music_msg


def download_song(song_id):
    music_msg = get_urls(song_id)
    title,song_url = music_msg['title'],music_msg['song_url']
    data = requests.get(song_url).content  # 存储数据

    download_path = 'C:\\Users\\Administrator\\Music\\' + \
        '%s.mp3' % (title)  # 指定本地存储路径

    print '%s 正在下载...' % title.encode('utf-8')
    with open(download_path, 'wb') as f:  # 写入文件到指定路径
        f.write(data)
    print '%s 下载完成' % title.encode('utf-8')


def get_music_ids(song_name):
    api = 'http://music.baidu.com/search/song?key=%s' % song_name
    resp = requests.get(api)  # response
    resp.encoding = 'utf-8'  # 格式转换
    html = resp.text  # 获取html文本
    ul = re.findall(r'<ul.*</ul>', html, re.S)[0]  # 匹配ul标签
    sids = re.findall(r'sid&quot;:(\d+),', ul, re.S)  # 匹配歌曲id
    return sids[0]

def main():
    song_name = raw_input('请输入歌曲（歌手）名:')
    sid = get_music_ids(song_name)  # 获取歌手为xxx的歌曲信息
    music_msg = get_urls(sid)
    for x,y in music_msg.items():
        print x,y



if __name__ == '__main__':
    while 1:
        main()
