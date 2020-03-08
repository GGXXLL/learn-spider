# coding=utf-8
import requests
import re
import json


def get_data():
    headers = {
        'Referer': 'http://www.weather.com.cn/weather1d/101010100.shtml',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }

    resp = requests.get(
        'http://d1.weather.com.cn/dingzhi/101010100.html?_=1523523092206', headers=headers)
    resp.encoding = 'gzip'
    data = json.loads(re.findall(
        r'var cityDZ101010100 =(.*);', resp.text)[0])['weatherinfo']

    cityname = data['cityname']
    temp = data['temp']
    tempn = data['tempn']
    weather = data['weather']
    wd = data['wd']
    ws = data['ws']
    data1 = f'今日概况:城市:{cityname},温度:{temp}到{tempn},天气:{weather},风向:{wd},风速:{ws}'
    resp = requests.get(
        'http://d1.weather.com.cn/sk_2d/101010100.html?_=1523522128393', headers=headers)
    resp.encoding = 'gzip'

    data = json.loads(re.findall(r'var dataSK = (.*)', resp.text)[0])
    temp = data['temp']
    wd = data['WD']
    ws = data['WS']
    sd = data['SD']
    time = data['time']
    weather = data['weather']
    limitnumber = data['limitnumber']
    aqi_type = ['优', '良', '轻度污染', '中度污染', '重度污染']

    aqi = data['aqi'] + ' ' + aqi_type[int(data['aqi']) // 50]
    data2 = f'此刻概况:城市:{cityname},时间:{time},温度:{temp}摄氏度,风向:{wd},风速:{ws},相对湿度:{sd},天气:{weather},空气质量:{aqi},车辆限行:{limitnumber}'
    return data1 + '\n' + data2


if __name__ == '__main__':
    data = get_data()
    print(data)
