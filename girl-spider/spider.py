import requests
from lxml import etree
import os
from time import sleep
import re
url = 'http://www.meizitu.com/'

headers = {
    # "Accept": "text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, image / apng, * / *; q = 0.8",
    # "Accept - Language": "zh - CN, zh; q = 0.9",
    # "Connection": "keep - alive",
    # "Cookie": "safedog-flow-item =; UM_distinctid = 1626c11a8241b4-0f9e40582cbc1-3a61430c-15f900-1626c11a825291; CNZZDATA30056528 = cnzz_eid%3D869235129-1522230526-%26ntime%3D1522230526",
    # "Host": "www.meizitu.com",
    # "Upgrade - Insecure - Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
}
# 获取图片一级分类
resp = requests.get(url, headers=headers)
resp.encoding = 'gbk'
content = resp.text
tree = etree.HTML(content)
tag_hrefs = tree.xpath('//*[@id="subcontent clearfix"]/div[2]/span/a/@href')
tag_names = tree.xpath('//*[@id="subcontent clearfix"]/div[2]/span/a/@title')
tags = dict(zip(tag_names, tag_hrefs))
# print(tags)
for tag_name, tag_href in tags.items():
    # 通过一级标签获取二级分类
    print('----------', tag_name, '--------------')
    # 每个一级分类的分页处理
    for i in range(1, 2):
        tag_href = re.sub(
            r'http://www.meizitu.com/(.*)/(.*?)_?(\d?).html', r'http://www.meizitu.com/\1/\2_%d.html' % i, tag_href)
        # print(tag_href)
        try:
            resp = requests.get(tag_href, headers=headers)
        except Exception as e:
            print('*' * 50)
            break
        # resp = requests.get(tag_href, headers=headers)
        resp.encoding = 'gbk'
        content = resp.text
        # print(content)
        tree = etree.HTML(content)
        a_links = tree.xpath(
            '//*[@id="maincontent"]/div[1]/ul/li/div/div/a/@href')
        a_names = tree.xpath(
            '//*[@id="maincontent"]/div[1]/ul/li/div/h3/a/b/text()')
        ass = dict(zip(a_names, a_links))
        # print(a_links)
        # print(a_names)
        count = 0
        for a_name, a_link in ass.items():
            # 下载二级分类里的图片
            print(a_name, end='')
            resp = requests.get(a_link, headers=headers)
            resp.encoding = 'gbk'
            content = resp.text
            # print(content)
            tree = etree.HTML(content)
            img_urls = tree.xpath('//*[@id="picture"]/p/img/@src')
            img_name = tree.xpath('string(//*[@id="maincontent"]/div[1]/div[1]/h2/a)')
            # print(img_urls)

            file_path = 'images/{}/{}'.format(tag_name, img_name)
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            for i in range(len(img_urls)):
                r = requests.get(img_urls[i], headers=headers)
                img_path = '{}/{}.jpg'.format(file_path, i + 1)
                if not os.path.exists(img_path):
                    with open(img_path, 'wb') as f:
                        f.write(r.content)
                    count += 1
                else:
                    continue
                sleep(0.5)

        print('\t%d' % count)
