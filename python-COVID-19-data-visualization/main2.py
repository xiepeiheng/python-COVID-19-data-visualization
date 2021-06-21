import urllib.error
import urllib.request
import time
import json
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
import sqlite3
from matplotlib import pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import os
import jieba
import sys


def main():
    savepath = r'cov.db'

    baidu = get_baidu()

    delete_database(savepath)
    
    savedata(savepath, baidu) 
    
    wordcloud()


def delete_database(savepath):
    conn = sqlite3.connect(savepath)
    cursor = conn.cursor()
    cursor.execute('DELETE from baidu')
    conn.commit()
    conn.close()         
        
        
        
        
def wordcloud():
    # 删除旧图片

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
    
    #删除旧图片
    if os.path.exists(r'/bs/static/images/word.jpg'):
        os.remove(r'/bs/static/images/word.jpg')
    
    #保存新图片
    plt.savefig(r'/bs/static/images/word.png', dpi=500, bbox_inches='tight', transparent=True)   
    
    
def get_baidu():
    url = 'https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_1'
    
    option = webdriver.ChromeOptions()
    option.add_argument('-headless')
    option.add_argument('-no-sandbox')
    browser = webdriver.Chrome(executable_path='/bs/chromedriver',chrome_options=option)
    try:
        browser.get(url)
        but = browser.find_element_by_css_selector('#ptab-1 > div.Virus_1-1-306_2SKAfr > div.Common_1-1-306_3lDRV2 > span')
        but.click()
        time.sleep(3)
        c = browser.find_elements_by_xpath('//*[@id="ptab-1"]/div[3]/div/div[2]/a/div')
    except:
        browser.close()
        browser.quit() 
        print('出现故障')
        sys.exit(0)
    else:
        cmy = []
        for i in c:
            cmy.append(i.text)
        browser.close()
        browser.quit()  
        return cmy    
    
    
    
def savedata(savepath, baidu):
    conn = sqlite3.connect(savepath)
    cur = conn.cursor()

    print('开始存储')

    #存储百度热搜词
    for data in baidu:
        sql5 = '''
            insert into baidu(
            热搜词条
            )
        values(
            ?
        )
           '''
        cur.execute(sql5, [data])

    conn.commit()
    cur.close()
    conn.close()
    
    
    
main()
print('完成')
        