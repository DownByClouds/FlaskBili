import requests
import logging
import os
import sys
import urllib
from urllib import error
'''
1.根据bv号即bvid获取title, cid;
API：https://api.bilibili.com/x/web-interface/view?bvid=BV1pu411x7m8
2.构造api页面
3.https://api.bilibili.com/x/player/playurl?avid=528778434&cid=1136224832&qn=1&type=&otype=json&platform=html5&high_quality=1
填充aid和cid
'''
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s : %(message)s')


class BiliCrawler():
    def getIDandTitle(self, bivd):
        aid = 0
        title = ''
        cid = 0
        baseurl = 'https://api.bilibili.com/x/web-interface/view?bvid='
        url = baseurl + bivd
        print(url)
        try:
            logging.info('开始获取视频的aid，cid以及title......')
            response = requests.get(url)
        except BaseException:
            logging.error('出现错误! 状态码为：%d', response.status_code)

        res_json = response.json()
        if res_json['code'] == -400:
            logging.info('BV号失效，视频不存在！')
        else:
            aid = res_json['data']['aid']
            title = res_json['data']['title']
            cid = res_json['data']['pages'][0]['cid']
        return (aid, title, cid)

    def getAudioLink(self, bivd):
        aid = 0
        title = ''
        cid = 0
        baseurl = 'https://api.bilibili.com/x/web-interface/view?bvid='
        url = baseurl + bivd
        print(url)
        try:
            logging.info('开始获取视频的aid，cid以及title......')
            response = requests.get(url)
        except BaseException:
            logging.error('出现错误! 状态码为：%d', response.status_code)

        res_json = response.json()
        if res_json['code'] == -400:
            logging.info('BV号失效，视频不存在！')
        else:
            aid = res_json['data']['aid']
            title = res_json['data']['title']
            cid = res_json['data']['pages'][0]['cid']

        baseUrl = 'https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn=1&type=&otype=json&platform=html5&high_quality=1'.format(
            aid, cid)
        currentVedioPath = os.path.join(sys.path[0], 'bilibili_vedio')
        try:
            response = requests.get(baseUrl)
            audioUrl = response.json()['data']['durl'][0]['url']
            logging.info('获取的视频页地址：%s', audioUrl)
            logging.info('网页状态码为：%d', response.status_code)
        except BaseException as e:
            logging.error('出现错误%s, 状态码为：%d', e, response.status_code)
        return audioUrl, title



    def getAudio(self, item):
        aid, title, cid = item[0], item[1], item[2]
        baseUrl = 'https://api.bilibili.com/x/player/playurl?avid={}&cid={}&qn=1&type=&otype=json&platform=html5&high_quality=1'.format(
            aid, cid)
        currentVedioPath = os.path.join(sys.path[0], 'bilibili_vedio')
        try:
            response = requests.get(baseUrl)
            audioUrl = response.json()['data']['durl'][0]['url']
            logging.info('获取的视频页地址：%s', audioUrl)
            logging.info('网页状态码为：%d', response.status_code)
        except BaseException as e:
            logging.error('出现错误%s, 状态码为：%d', e, response.status_code)

        opener = urllib.request.build_opener()
        opener.addheaders = [
            ('User-Agent',
             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'),
            ('Accept', '*/*'),
            ('Accept-Language', 'zh-CN,zh;q=0.9'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),
            ('Referer', 'https://api.bilibili.com/x/web-interface/view?bvid=' + bvid),
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive'),
        ]
        urllib.request.install_opener(opener)
        # 判断文件夹是否存在
        if not os.path.exists(currentVedioPath):
            os.makedirs(currentVedioPath)
        try:
            urllib.request.urlretrieve(url=audioUrl, filename=os.path.join(currentVedioPath, r'{}.mp4'.format(title)))
        except (error.HTTPError, error.URLError) as e:
            logging.info('发生错误：%s', e)


if __name__ == '__main__':
    # BV1md4y4Z2tL
    bvid = 'BV1Fv4y1d7mG'
    crawl = BiliCrawler()
    url = crawl.getAudioLink(bvid)
    # print(url)

