import urllib.error
import urllib.request
import json
import sqlite3
import numpy as np
from scipy import optimize as op


def main():
    savepath = 'cov.db'
    url = 'https://api.inews.qq.com/newsqa/v1/automation/modules/list?modules=FAutoCountryMerge'
    c_name = ['俄罗斯', '巴西', '德国', '意大利', '法国', '美国', '英国', '西班牙']
    c_r = [0.002, 0.0018, 0.002, 0.0025, 0.002, 0.003, 0.004, 0.004]
    c_r = [0,0,0,0,0,0,0,0]
    c_p0 = [20000, 500000, 40000, 10000, 50000, 150000, 1000, 1000]
    country_data = []
    country_d_data = []
    duoyu = []



    # 从api得到数据
    data = get_data(url)

    # 获取原始数据
    for i in range(8):
        country_data.append(get_country(c_name[i], data))

    # 进行数据处理
    for j in range(8):
        A, B = deal_data(country_data[j], c_p0[j], c_r[j])
        country_d_data.append(A)
        duoyu.append(B)

    # print(country_d_data)
    # 建立真实数据存储库
    delete_database(savepath)

    # 存储数据
    savedata(savepath, country_d_data, c_name, duoyu)


# 存储数据
def savedata(savepath, country_d_data, c_name, duoyu):
    conn = sqlite3.connect(savepath)
    cur = conn.cursor()
    print('开始存储')
    h = -1
    for i in country_d_data:
        h = h + 1  # 轮番向数据中写入
        # 时间 text, 累计确诊 numeric,序号 numeric,预测 numeric
        for data in i:
            sql1 = f'''
                    insert into {c_name[h]}(
                    时间,
                    累计确诊,
                    序号,
                    预测
                    )
                values(
                    ?,
                    ?,
                    ?,
                    ?
                )
                '''
            cur.execute(sql1, (data[0], data[1], data[2], data[3]))
    h = -1
    for i in duoyu:
        h = h + 1
        for data in i:
            sql2 = f'''
                    insert into {c_name[h]}(
                    序号,
                    预测
                    )
                values(
                    ?,
                    ?
                )
                '''
            cur.execute(sql2, (data[0], data[1]))
    conn.commit()
    conn.close()


def delete_database(savepath):
    conn = sqlite3.connect(savepath)
    cursor = conn.cursor()
    cursor.execute('DELETE from 俄罗斯')
    cursor.execute('DELETE from 巴西')
    cursor.execute('DELETE from 德国')
    cursor.execute('DELETE from 意大利')
    cursor.execute('DELETE from 法国')
    cursor.execute('DELETE from 美国')
    cursor.execute('DELETE from 英国')
    cursor.execute('DELETE from 西班牙')
    conn.commit()
    conn.close()


# 获取国家数据
def get_country(name, data):
    cmy = []
    for i in data['data']['FAutoCountryMerge'][name]['list']:
        a = i['y']
        b = i['date']
        time = a + '.' + b
        confirm = i['confirm']
        cmy.append([time, confirm])
    return cmy


# 从网页获取数据
def get_data(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36 Edg/89.0.774.50"
    }
    request = urllib.request.Request(url, headers=head)
    response1 = urllib.request.urlopen(request)
    html = response1.read().decode('utf-8')
    data = json.loads(html)  # json字符串转字典
    return data


def deal_data(data, p01, r01):
    length = len(data)
    time = []
    time1 = []
    people = []
    for i in data:
        time.append(i[0])
        people.append(i[1])

    num = 0
    for i in range(length):
        num = num + 1
        time1.append(num)

    p0 = p01

    t_group = np.array(time1)
    p_group = np.array(people)

    def f_1(t, k, r):
        return k / (1 + (k / p0 - 1) * 2.718281828459045 ** (-r * t))

    k, r = op.curve_fit(f_1, t_group, p_group)[0]
    r = r - r01

    f_time = []
    f_people = []

    num = 0
    for i in range(length):
        num = num + 1
        f_time.append(num)
        f_people.append(k / (1 + (k / p0 - 1) * 2.718281828459045 ** (-r * num)))
    cmy = []
    for i in range(length):
        cmy.append([time[i], people[i], f_time[i], f_people[i]])
    zfh = []
    for i in range(length + 1, length + 100):
        zfh.append([i, k / (1 + (k / p0 - 1) * 2.718281828459045 ** (-r * i))])

    return cmy, zfh


main()
print('全部完成')
