# -*- coding: UTF-8 -*-

from aip import AipOcr
import os
import http.client
import hashlib
from urllib import parse
import random
import json

# 定义常量
APP_ID = '10379743'
#OCRD的id和key
API_KEY = 'QGGvDG2yYiVFvujo6rlX4SvD'
SECRET_KEY = 'PcEAUvFO0z0TyiCdhwrbG97iVBdyb3Pk'
#翻译的ID和KEY
appid = '20180714000185578'
secretKey = 'kl5YaTfsWBIdkdvTz9EZ'

# 定义参数变量（主要识别图片中的英文和中文）
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}
#定义待翻译语言为中文，目标语言为英文
fromLang = 'zh'
toLang = 'en'

#统计文件夹中有多少图片
imgFileNameF = 'H:/Translation/img'
imgNum = len([name for name in os.listdir(imgFileNameF) if os.path.isfile(os.path.join(imgFileNameF, name))])

def Translation(q):
    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    sign = appid + q + str(salt) + secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode(encoding='utf-8'))
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)
    response = httpClient.getresponse()
    res = response.read().decode('utf-8')
    res = eval(res)
    httpClient.close()
    return res['trans_result'][0]['dst']

# 初始化文字识别分类器
aipOcr=AipOcr(APP_ID, API_KEY, SECRET_KEY)

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

#依次读入图片
for i in range(imgNum):
    imgFileName = './img/' + str(i) + '.jpg'
    print(imgFileName)
    result = aipOcr.webImage(get_file_content(imgFileName), options)

    #内容写入TXT
    with open('data.txt','a') as f:
        f.write('^^^^^^^^^^^^^^     ' + str(i) + '.jpg      识别翻译结果如下：^^^^^^^^^^^^^^' + "\n")
        for j in result['words_result']:
            f.write(j['words'] + "\n")
            print(j['words'])

            tra = Translation(j['words'])
            f.write(tra + "\n")
            print(tra)

