# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree


def get_text(query_word):
    url = 'https://baike.baidu.com/item/'

    headers = {
        'Host': 'baike.baidu.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    # 对url中的中文进行处理,得到编码后的url
    url = url + query_word
    # 发送请求
    resp = requests.get(url, headers=headers)
    # 对响应进行格式设置
    resp.encoding = 'utf8'
    content = resp.text
    # xpath匹配需要的内容
    tree = etree.HTML(content)
    text = tree.xpath('string(//div[@class="lemma-summary"])')
    # 正则过滤[1][2-3]之类的注释标签
    text = re.sub(r'(\[\d? ?-? ?\d?\])', '', text)
    return text


if __name__ == '__main__':

    query_word = input('输入词条:')
    text = get_text(query_word)
    if text:
        print(text)
    else:
        print('\r\n未检索到{}的信息,请完善或修改词条\r\n'.format(query_word))

