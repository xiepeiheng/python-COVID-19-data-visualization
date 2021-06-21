import urllib.error
import urllib.request
import time
import json
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
import sqlite3
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import os


# 所有函数

# 爬取数据：
# get_now_data()，get_his_data()
# 获取数据：
# get_country_his(), get_country_now()
# get_provice()

def main():
    savepath = r'cov.db'

    

    # 爬取今日数据
    data_now = get_now_data()
    # 爬取历史数据
    data_his = get_his_data()

    # 以省份为单位存储数据，获得一个存满数据的数组
    data_province = get_provice_data(data_now)
    # 存储全国的每日历史数据
    data_country_his = get_country_his_data(data_his)
    # 存储全国当日数据
    data_country_now = get_country_now_data(data_now)
    # 获取详情页数据
    data_city = get_city_data(data_now)
    # 获取疫苗接种数据
    data_vaccines = get_vaccines()#从另一个网页爬取所以没有传参
    # 获取保持为0的天数
    data_zero = get_zero(data_his)
    # 获取全球数据从网易数据源
    data_global = get_global()#网址直接写进网易数据源所以没有传参

    # 获得热搜词
    # baidu = get_baidu()
    
    delete_database(savepath)

    # 将数据全部存储进数据库
    savedata(savepath, data_province, data_country_his, data_country_now, data_city, data_vaccines, data_zero, data_global)

    # 获得词云图片
    # wordcloud()

def get_zero(data_his):
    cmy = []
    for i in data_his['provinceCompare']:
        a = i
        b = data_his['provinceCompare'][i]['zero']
        cmy.append([a, b])
    return cmy

def get_global():
    url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total'
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"
    }
    request = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    zfh = json.loads(html)  # json字符串转字典
    cmy = []
    for i in zfh['data']['areaTree']:
        a = i['name']
        b = i['today']['confirm']
        c = i['total']['confirm']
        d = i['total']['heal']
        e = i['total']['dead']
        if b is not None and c is not None and d is not None and e is not None:
            cmy.append([a, b, c, d, e])
    return cmy


def get_vaccines():
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=VaccineTopData'
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"
    }
    request = urllib.request.Request(url, headers=head)
    response = urllib.request.urlopen(request)
    html = response.read().decode('utf-8')
    res = json.loads(html)  # json字符串转字典
    a = res['data']['VaccineTopData']['中国']['total_vaccinations']
    b = res['data']['VaccineTopData']['中国']['new_vaccinations']
    c = res['data']['VaccineTopData']['中国']['total_vaccinations_per_hundred']
    d = res['data']['VaccineTopData']['全球']['total_vaccinations']
    e = res['data']['VaccineTopData']['全球']['new_vaccinations']
    f = res['data']['VaccineTopData']['全球']['total_vaccinations_per_hundred']
    return [a, b, c, d, e, f]


def wordcloud():
    # 删除旧图片
    if os.path.exists(r'/bs/static/images/word.jpg'):
        os.remove(r'/bs/static/images/word.jpg')

    # 获取热搜语句并将他们连在一起
    con = sqlite3.connect('cov.db')
    cur = con.cursor()
    sql = '''
        select 热搜词条 from baidu
    '''
    data = cur.execute(sql)
    cmy = []
    for i in data:
        cmy.append(i[0])
    cur.close()
    con.close()
    text = ''
    for i in cmy:
        text = text + i

    # 通过jieba将长语句拆开变成词语
    cut = jieba.cut(text)
    string = ' '.join(cut)

    # 将背景图片变成二进制数组
    img = Image.open(r'/bs/static/images/词云背景图.png')
    img_array = np.array(img)  # 将图片转换为数组

    # 使用词云库进行处理，生成图片
    wc = WordCloud(
        background_color=None,
        mask=img_array,
        font_path=r'/bs/static/font/msyh.ttc',
        mode='RGBA',
    )
    wc.generate_from_text(string)

    # 保存图片
    fig = plt.figure(1)
    plt.imshow(wc)
    plt.axis('off')
    plt.tight_layout(pad=0.1)
    fig.set_size_inches(1, 1)
    plt.savefig(r'/bs/static/images/word.png', dpi=500, bbox_inches='tight', transparent=True)


# 爬取今日数据
def get_now_data():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"
    }
    request = urllib.request.Request(url, headers=head)
    response1 = urllib.request.urlopen(request)
    html1 = response1.read().decode('utf-8')
    res = json.loads(html1)  # json字符串转字典
    data_now = json.loads(res['data'])
    return data_now


# 爬取历史数据
def get_his_data():
    url_his = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"
    }
    request = urllib.request.Request(url_his, headers=head)
    response2 = urllib.request.urlopen(request)
    html2 = response2.read().decode('utf-8')
    res_his = json.loads(html2)
    data_his = json.loads(res_his['data'])
    return data_his


# 爬取省份数据
def get_provice_data(data_now):
    province_now = []
    # 说明，顺序依次为
    # 地区名称
    # 新增确诊
    # 现有确诊
    # 累计确诊
    # 治愈
    # 死亡
    for i in range(len(data_now['areaTree'][0]['children']) - 1):
        a = data_now['areaTree'][0]['children'][i]['name']
        b = data_now['areaTree'][0]['children'][i]['today']['confirm']
        c = data_now['areaTree'][0]['children'][i]['total']['nowConfirm']
        d = data_now['areaTree'][0]['children'][i]['total']['confirm']
        e = data_now['areaTree'][0]['children'][i]['total']['heal']
        f = data_now['areaTree'][0]['children'][i]['total']['dead']
        province_now.append([a, b, c, d, e, f])
    return province_now


# 爬取全国历史数据
def get_country_his_data(data_his):
    # 从历史表中爬取全国的历史数据

    # confirm1 累计确诊
    # confirm2 当日新增确诊
    # heal1    累计治愈
    # heal2    当日新增治愈
    # dead1    累计死亡
    # dead2    当日新增死亡

    history = []  # 所有需要存储的数据

    num = len(data_his['chinaDayList']) - 1

    for i in range(num):
        time = data_his['chinaDayList'][i]['y'] + '.' + data_his['chinaDayList'][i]['date']

        confirm1 = data_his['chinaDayList'][i]['confirm']
        confirm2 = data_his['chinaDayAddList'][i]['confirm']

        heal1 = data_his['chinaDayList'][i]['heal']
        heal2 = data_his['chinaDayAddList'][i]['heal']

        dead1 = data_his['chinaDayList'][i]['dead']
        dead2 = data_his['chinaDayAddList'][i]['dead']

        imported1 = data_his['chinaDayList'][i]['importedCase']  # 累计境外输入
        imported2 = data_his['chinaDayAddList'][i]['importedCase']  # 当日新增境外输入

        history.append([time, confirm1, confirm2, heal1, heal2, dead1, dead2, imported1, imported2])

    return history


# 爬取全国当日数据
def get_country_now_data(data_now):
    # 依次为 累计确诊 累计治愈 累计死亡 现有确诊 新增确诊 当日新增境外 累计境外
    a = data_now['chinaTotal']['confirm']
    b = data_now['chinaTotal']['heal']
    c = data_now['chinaTotal']['dead']
    d = data_now['chinaTotal']['nowConfirm']
    e = data_now['areaTree'][0]['today']['confirm']
    f = data_now['chinaAdd']['importedCase']
    g = data_now['chinaTotal']['importedCase']

    return [a, b, c, d, e, f, g]


# 获取详情页数据
def get_city_data(data):
    cmy = []
    for i in range(len(data['areaTree'][0]['children']) - 1):
        a1 = data['areaTree'][0]['children'][i]['name']
        for j in range(len(data['areaTree'][0]['children'][i]['children']) - 1):
            a2 = data['areaTree'][0]['children'][i]['children'][j]['name']
            b2 = data['areaTree'][0]['children'][i]['children'][j]['today']['confirm']
            c2 = data['areaTree'][0]['children'][i]['children'][j]['total']['nowConfirm']
            d2 = data['areaTree'][0]['children'][i]['children'][j]['total']['confirm']
            e2 = data['areaTree'][0]['children'][i]['children'][j]['total']['heal']
            f2 = data['areaTree'][0]['children'][i]['children'][j]['total']['dead']
            cmy.append([a1, a2, b2, c2, d2, e2, f2])
    return cmy


# 百度热搜词
def get_baidu():
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1'
    
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    option.add_argument('no-sandbox')
    option.add_argument('disable-dev-shm-usage')
    browser = webdriver.Chrome(executable_path='/bs/chromedriver',chrome_options=option)

    browser.get(url)
    but = browser.find_element_by_css_selector('/html/body/div[2]/div/div/div/section/div[3]/div/div/div[3]/div[11]')
    but.click()
    time.sleep(1)
    c = browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[2]/a/div')
    cmy = []
    for i in c:
        cmy.append(i.text)
    browser.quit()  
    return cmy


def delete_database(savepath):
    conn = sqlite3.connect(savepath)
    cursor = conn.cursor()
    # cursor.execute('DELETE from baidu')
        # cursor.execute('DELETE from city')
    cursor.execute('DELETE from country_his')
    cursor.execute('DELETE from country_now')
    cursor.execute('DELETE from vaccines')
    cursor.execute('DELETE from zero')
    # cursor.execute('DELETE from earth')
        # cursor.execute('DELETE from province')
    conn.commit()
    conn.close()
    

def savedata(savepath, data_province, data_country_his, data_country_now, data_city, data_vaccines, data_zero, data_global):
    conn = sqlite3.connect(savepath)
    cur = conn.cursor()

    for data in data_country_his:
        # 全国历史数据
        sql1 = '''
            insert into country_his(
            时间,
            累计确诊,
            当日新增确诊, 
            累计治愈, 
            当日新增治愈, 
            累计死亡, 
            当日新增死亡,
            累计境外输入,
            当日新增境外输入 
            )
        values(
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        '''
        cur.execute(sql1, (data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))

    for data in data_province:
        cur.execute(f"DELETE FROM province WHERE 省份名称 = '{data[0]}'")
        sql2 = '''
            insert into province(
            省份名称,
            新增确诊,
            现有确诊,
            累计确诊,
            累计治愈,
            累计死亡
            )
        values(
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
                '''
        cur.execute(sql2, (data[0], data[1], data[2], data[3], data[4], data[5]))

    # 全国当日数据
    sql3 = '''
        insert into country_now(
        累计确诊,
        累计治愈,
        累计死亡, 
        现有确诊, 
        新增确诊,
        当日新增境外,
        累计境外
        )
    values(
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    )
    '''
    cur.execute(sql3, (
        data_country_now[0], data_country_now[1], data_country_now[2], data_country_now[3], data_country_now[4], data_country_now[5], data_country_now[6]))

    for data in data_city:
        cur.execute(f"DELETE FROM city WHERE 城市名称 = '{data[1]}' and 省份名称 = '{data[0]}'")
        sql4 = '''
            insert into city(
            省份名称,
            城市名称,
            新增确诊,
            现有确诊,
            累计确诊,
            累计治愈,
            累计死亡
            )
        values(
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        '''
        cur.execute(sql4, (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))

    #存储百度热搜词
    # for data in baidu:
    #     sql5 = '''
    #         insert into baidu(
    #         热搜词条
    #         )
    #     values(
    #         ?
    #     )
    #       '''
    #     cur.execute(sql5, [data])

    # 保存疫苗接种情况
    sql6 = '''
        insert into vaccines(
        国内累计接种,
        国内新增接种,
        国内接种率,
        全球累计接种,
        全球新增接种,
        全球接种率
        )
    values(
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    )
           '''
    cur.execute(sql6, (data_vaccines[0],data_vaccines[1],data_vaccines[2],data_vaccines[3],data_vaccines[4],data_vaccines[5]))

    #保存迄今为止连续多少天新增为零
    for data in data_zero:
        sql7 = '''
            insert into zero(
            省份名称,
            天数
            )
        values(
            ?,
            ?
        )
           '''
        cur.execute(sql7, (data[0],data[1]))

    #保存全球数据
    for data in data_global:
        cur.execute(f"DELETE FROM earth WHERE 国家名称 = '{data[0]}'")
        sql8 = '''
            insert into earth(
            国家名称,
            新增确诊,
            累计确诊,
            累计治愈,
            累计死亡
            )
        values(
            ?,
            ?,
            ?,
            ?,
            ? 
        )
           '''
        cur.execute(sql8, (data[0],data[1],data[2],data[3],data[4]))

    conn.commit()
    cur.close()
    conn.close()


main()
print('全部工作完成')
