import requests
import json
import urllib
import pypinyin
import os
from bs4 import BeautifulSoup
import time



# 不带声调的(style=pypinyin.NORMAL)
def pinyin(word):
    s = ''
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        s += ''.join(i)
    return s

def CurrentPicture_list():
    filename_number = []
    Collect_Pic_path = Collect_Picture_SavePath[0:len(Collect_Picture_SavePath) - 1]
    for files in os.listdir(Collect_Pic_path):
        if files.endswith(".jpg"):  # 填写规则
            (filename, extension) = os.path.splitext(files)
            if filename[0:len(Collect_Picture_Source + '_' + pinyin(
                    Collect_Picture_category) + '_')] == Collect_Picture_Source + '_' + pinyin(
                Collect_Picture_category) + '_':
                filename_number.append(
                    filename[len(Collect_Picture_Source + '_' + pinyin(Collect_Picture_category) + '_'):])
    return filename_number

#从必应图片搜索结果中抓取图片，相当于在搜索框中直接搜索
def getBingImag(Collect_Picture_category,Collect_Picture_length,Collect_Picture_SavePath):
    if not os.path.exists(Collect_Picture_SavePath):
        os.mkdir(Collect_Picture_SavePath)
    try:
        if len(CurrentPicture_list()) != 0:
            start_Collect_Index = int(max(CurrentPicture_list())) + 1
        else:
            start_Collect_Index = 0
        print('start_Collect_Index:' + str(start_Collect_Index))
        # imgs = requests.get(
        #     'https://pic.sogou.com/pics?query=' + Collect_Picture_category + '&mode=1&start=0&reqType=ajax&reqFrom=result&tn=0')
        # jd = json.loads(imgs.text)
        # jd = jd['items']
        items_in_page = 35
        pages = Collect_Picture_length // items_in_page
        pages_remainder = Collect_Picture_length % items_in_page
        print('pages：' + str(pages))
        print('pages_remainder：' + str(pages_remainder))
        # m = start_Collect_Index
        n_try = 0
        First_RequestFailed_Flag = 0
        for x in range(pages + 1):
            Each_start_Index = x * items_in_page + start_Collect_Index
            print('****************')
            print('x：' + str(x))
            # print('start:' + str(Each_start_Index))
            # 表示从索引为start的图片（即第start+1张图片）开始搜索48张图片，网页中图片以48张为一组，可以循环执行，通过修改start值抓取多个大批量图片
            # 请求失败时，则重复请求40次
            for y in range(30):
                try:
                    n = Each_start_Index
                    print('start:' + str(Each_start_Index))
                    url = 'http://cn.bing.com/images/async?q=' + urllib.parse.quote(
                        Collect_Picture_category) + '&first=' + str(Each_start_Index) + '&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0'
                    # 定义请求头
                    agent = {
                        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
                    page1 = urllib.request.Request(url, headers=agent)
                    page = urllib.request.urlopen(page1)
                    soup = BeautifulSoup(page.read(), 'html.parser')
                    jd = soup.select('.mimg')
                    if x == pages:
                        jd = jd[0:pages_remainder + n_try%items_in_page]
                    for StepOne in jd:
                        link = StepOne.attrs['src']
                        print(
                            '\r\n' + Collect_Picture_Source + '_' + pinyin(Collect_Picture_category) + '_' + str(
                                n).rjust(4, '0') + '.jpg' + '  Downloading...')
                        try:
                            time.sleep(0.2)
                            urllib.request.urlretrieve(link,
                                                       Collect_Picture_SavePath + Collect_Picture_Source + '_' + pinyin(
                                                           Collect_Picture_category) + '_' + str(n).rjust(4,
                                                                                                          '0') + '.jpg')
                        except:
                            print('\r\n' + Collect_Picture_Source + '_' + pinyin(
                                Collect_Picture_category) + '_' + str(n).rjust(4,
                                                                               '0') + '.jpg' + '  Download failed')
                        print('n:' + str(n))
                        n = n + 1
                    # m = n
                except:
                    if First_RequestFailed_Flag == 0:
                        print('\r\n Requests Failed, Tring to request times……')
                        First_RequestFailed_Flag = 1
                    n_try = n_try + 1
                    Each_start_Index = Each_start_Index + 1
                    print('(' + str(n_try) + ')')
                else:
                    break
            print('n_try：' + str(n_try))
        print('\r\n Download complete!')
    except:
        print(
            '\r\n' + Collect_Picture_Source + ' Internet Requests failed,Please Check the Internet is Connected!')
        pass


if __name__ == "__main__":
    Collect_Picture_Source_Index = 3
    Collect_Picture_Source = pinyin('Bing图片')
    Collect_Picture_category = input("请输入你想爬取的图片： ")
    Collect_Picture_length = int(input("请输入你要爬取图片的数量： "))
    if not os.path.isdir('./%s' % Collect_Picture_category):
        os.mkdir('./%s' % Collect_Picture_category)
    Collect_Picture_SavePath = './%s/' % Collect_Picture_category
    getBingImag(Collect_Picture_category,Collect_Picture_length,Collect_Picture_SavePath) #百度图片搜索“范冰冰”，抓取33张图片，保存在路径“D:/test/1/”文件夹下

