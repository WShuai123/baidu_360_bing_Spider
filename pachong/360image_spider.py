import requests
import json
import urllib
import pypinyin
import os



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

#从百度图片搜索结果中抓取图片，相当于在搜索框中直接搜索
def get360Imag(Collect_Picture_category,Collect_Picture_length,Collect_Picture_SavePath):
    if not os.path.exists(Collect_Picture_SavePath):
        os.mkdir(Collect_Picture_SavePath)
    try:
        #最后面的参数pn代表从pn开始抓取，rn为抓取的图片数量
        if len(CurrentPicture_list()) != 0:
            start_Collect_Index = int(max(CurrentPicture_list())) + 1
        else:
            start_Collect_Index = 0
        print('start_Collect_Index:' + str(start_Collect_Index))
        Current_Collect_Length = Collect_Picture_length
        n = 0
        Each_start_Index = start_Collect_Index
        for x in range(10000):
            print('****************')
            print('x：' + str(x))
            print('Each_start_Index:'+str(Each_start_Index))
            imgs = requests.get(
                'https://image.so.com/j?q=' + Collect_Picture_category + '&pd=1&pn=60&correct=' + Collect_Picture_category + '&adstar=0&tab=all&sid=6e2b80da466282eeb2cba21162efa997&ras=6&cn=0&gn=0&kn=50&src=srp&sn='+str(Each_start_Index)+'&ps=0&pc=0')
            jd = json.loads(imgs.text)
            jd = jd['list']  # 删除最后一个元素，因为最后一个元素没有内容
            items_in_page = len(jd)
            print('items_in_page:' + str(items_in_page))
            if Current_Collect_Length > 0:
                if Current_Collect_Length <= items_in_page:
                    jd = jd[0:Current_Collect_Length]
            else:
                break
            imgs_url = []
            for j in jd:
                imgs_url.append(j['img'])
            n = Each_start_Index
            for img_url in imgs_url:
                print('\r\n' + Collect_Picture_Source + '_' + pinyin(Collect_Picture_category) + '_' + str(n).rjust(4, '0') + '.jpg' + '  Downloading...')
                try:
                    urllib.request.urlretrieve(img_url,Collect_Picture_SavePath + Collect_Picture_Source + '_' + pinyin(Collect_Picture_category) + '_' + str(n).rjust(4,'0') + '.jpg')
                except:
                    print('\r\n' + Collect_Picture_Source + '_' + pinyin(Collect_Picture_category) + '_' + str(n).rjust(4,'0') + '.jpg' + '  Download failed')
                else:
                    Current_Collect_Length = Current_Collect_Length - 1
                # print('n:' + str(n))
                n = n + 1
            Each_start_Index = n
        print('Download complete!')
    except:
        print(
            '\r\n' + Collect_Picture_Source + ' Internet Requests failed,Please Check the Internet is Connected!')
        pass


if __name__ == "__main__":
    Collect_Picture_Source_Index = 2
    Collect_Picture_Source = pinyin('360图片')
    Collect_Picture_category = input("请输入你想爬取的图片： ")
    Collect_Picture_length = int(input("请输入你要爬取图片的数量： "))
    if not os.path.isdir('./%s' % Collect_Picture_category):
        os.mkdir('./%s' % Collect_Picture_category)
    Collect_Picture_SavePath = './%s/' % Collect_Picture_category # 保存路径，默认会在该文件的目录下新建一个和Collect_Picture_category同名的文件夹来保存图片
    get360Imag(Collect_Picture_category,Collect_Picture_length,Collect_Picture_SavePath)
