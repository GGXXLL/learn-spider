# coding=utf-8
import requests
import re
from lxml import etree
import json
# from naoqi import ALProxy


def get_data():
    headers = {
        'Referer': 'http://www.weather.com.cn/weather1d/101010100.shtml',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    resp = requests.get(
        'http://d1.weather.com.cn/dingzhi/101010100.html?_=1523523092206', headers=headers)
    resp.encoding = 'utf-8'
    data = json.loads(re.findall(
        r'var cityDZ101010100 =(.*);', resp.text)[0])['weatherinfo']
    for i in data:
        data[i] = data[i].encode('utf-8')
    cityname = data['cityname']
    temp = data['temp']
    tempn = data['tempn']
    weather = data['weather']
    wd = data['wd']
    ws = data['ws']
    data1 = '今日概况:城市:{},温度:{}到{},天气:{},风向:{}'.format(
        cityname, temp, tempn, weather, wd, ws)

    resp = requests.get(
        'http://d1.weather.com.cn/sk_2d/101010100.html?_=1523522128393', headers=headers).text
    data = json.loads(re.findall(r'var dataSK = (.*)', resp)[0])
    for i in data:
        data[i] = data[i].encode('utf-8')
    temp = data['temp']
    wd = data['WD']
    ws = data['WS']
    sd = data['SD']
    time = data['time']
    weather = data['weather']
    aqi_type = ['优', '良', '轻度污染', '中度污染', '重度污染']
    aqi = data['aqi'] + aqi_type[int(data['aqi']) // 50]
    limitnumber = data['limitnumber']

    data2 = '此刻概况:城市:{},时间:{},温度:{}摄氏度,风向:{},风速:{},相对湿度:{},天气:{},空气质量:{},车辆限行:{}'.format(
        cityname, time, temp, wd, ws, sd, weather, aqi, limitnumber)
    return data1 + '\r' + data2


if __name__ == '__main__':
    data = get_data()
    print data
    # a = input()
    # IP = '192.168.3.154'
    # tts = ALProxy("ALTextToSpeech", IP, 9559)
    # tts.say(data)
