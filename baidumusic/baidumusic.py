# coding=utf-8
import requests
import re
import json

header = {
    'Cookie': 'BUSS=VJQRVRDaG90QWxNTnhPVE9lTFZxTUYtTzlKQkRmSGZRanctaGRIZnBnS2dyU0JjQVFBQUFBJCQAAAAAAAAAAAEAAACQgIdUU2t5uKHJ-tm8w87h6gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAKAg-VugIPlbT; u_login=1; userid=1418166416; BAIDUID=5C27CF84DF53886605E4FC22F9551702:FG=1; Hm_lvt_d0ad46e4afeacf34cd12de4c9b553aa6=1583675303; log_sid=15836753035765C27CF84DF53886605E4FC22F9551702; __qianqian_pop_tt=7; Hm_lpvt_d0ad46e4afeacf34cd12de4c9b553aa6=1583675310; tracesrc=-1%7C%7C-1; u_lo=0; u_id=; u_t=',
    'Referer': 'https://music.taihe.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
}


def get_urls(song_id):
    # 把sid拼接进请求链接
    #     url = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&callback=jQuery17205500581185420972_1513324047403&songid=%s&_=1513324048127' % song_id

    # data = re.findall(r'\((.*)\)', data)[0]  # 使用第一个url,返回数据需要去掉圆括号
    music_msg = {}

    return music_msg


def download_song(song_id):
    url = 'http://music.baidu.com/data/tingapi/v1/restserver/ting?method=baidu.ting.song.play&songid=%s' % song_id
    data = requests.get(url).json()  # 获取请求信息文本   str

    title = data['songinfo']['title']  # 获取歌曲名称
    author = data['songinfo']['author']
    if not data['bitrate']:
        print(f'{title}-{author} 无法下载...')
        return
    file_link = data['bitrate']['file_link']  # 获取下载链接

    data = requests.get(file_link).content  # 存储数据
    download_path = f'{title}-{author}.mp3'  # 指定本地存储路径
    print(f'{title}-{author} 正在下载...')
    with open(download_path, 'wb') as f:  # 写入文件到指定路径
        f.write(data)
    print(f'{title}-{author} 下载完成')


def get_music_ids(song_name):
    api = 'http://music.taihe.com/search?key=%s' % song_name
    resp = requests.get(api, headers=header)  # response
    resp.encoding = 'utf-8'  # 格式转换
    html = resp.text  # 获取html文本
    ul = re.findall(r'<ul.*</ul>', html, re.S)[0]  # 匹配ul标签
    sids = re.findall(r'sid&quot;:(\d+),', ul, re.S)  # 匹配歌曲id
    return sids


def main():
    # song_name = input('请输入歌曲（歌手）名:')
    song_name = '韩红 一时间'
    sids = get_music_ids(song_name)  # 获取歌手为xxx的歌曲信息
    print('找到相关歌曲 {}首'.format(len(sids)))
    for sid in sids:
        download_song(sid)


if __name__ == '__main__':
    main()
