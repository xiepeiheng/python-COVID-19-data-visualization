from flask import Flask, render_template, request
import datetime
import sqlite3
import base64


app = Flask(__name__)

# ajax更新
@app.route('/ajax1')
def ajax1():
    with open('./static/images/word.png', 'rb') as img:
        img_stream = img.read()
        zfh = base64.b64encode(img_stream).decode()
    return zfh

@app.route('/ajax2')
def ajax2():
    # 页面开头数字大屏更新
    con = sqlite3.connect("cov.db")
    cur = con.cursor()
    table = {}
    sql1 = 'select 新增确诊,现有确诊,累计确诊,累计治愈,累计死亡,当日新增境外 from country_now'
    data1 = cur.execute(sql1)
    for i in data1:
        for j in range(len(i)):
            table[j] = i[j]
    cur.close()
    con.close()
    return table


@app.route('/forecast')
def forecast():
    cmy = []
    name = ['俄罗斯', '巴西', '德国', '意大利', '法国', '美国', '英国', '西班牙']
    con = sqlite3.connect("cov.db")
    cur = con.cursor()
    for i in name:
        a = []
        b = []
        c = []
        d = []
        sql = f'select * from {i}'
        data = cur.execute(sql)
        for j in data:
            if j[0] is None:
                a.append(' ')
            else:
                a.append(j[0])
            if j[1] is not None:
                b.append(j[1])
            c.append(j[2])
            d.append(round(j[3]))
        cmy.append([a, b, c, d])

    cur.close()
    con.close()
    return render_template('forecast.html', cmy=cmy, name=name)


@app.route('/brochure')
def brochure():
    return render_template('brochure.html')


@app.route('/datalist')
def datalist():
    cmy = []
    p1 = []

    con = sqlite3.connect("cov.db")
    cur = con.cursor()

    sql1 = 'select 省份名称,新增确诊,现有确诊,累计确诊,累计治愈,累计死亡 from province'
    data3 = cur.execute(sql1)
    zfh = []
    for i in data3:
        zfh.append(i)
    zfh.sort(key=lambda elem: elem[1], reverse=True)  # 使得按照新增人数的由多到少的顺序排列
    for i in zfh:
        cmy.append([i[0], i[1], i[2], i[3], i[4], i[5]])
    for i in cmy:
        sql2 = f"select 城市名称,新增确诊,现有确诊,累计确诊,累计治愈,累计死亡 from city WHERE 省份名称 = '{i[0]}'"
        data4 = cur.execute(sql2)
        for j in data4:
            p1.append([j[0], j[1], j[2], j[3], j[4], j[5]])
        i.append(p1)
        p1 = []

    cur.close()
    con.close()

    return render_template('datalist.html', cmy=cmy)


@app.route('/picture')
def picture():
    with open('./static/images/word.png', 'rb') as img:
        img_stream = img.read()
        zfh = base64.b64encode(img_stream).decode()

    # 表格1
    time = []
    nowconfirm = []
    confirm = []
    heal = []
    dead = []
    foreign_confirm = []
    foreign_nowconfirm = []

    # 表格2
    name = []
    num = []
    # 表格3
    cmy = []
    p1 = []
    p2 = []
    p3 = []
    # 表格4
    vaccines = []

    # 数据表格所需数据
    table = []

    # 现有确诊饼状图
    pie1 = []

    # 已经注射疫苗人数饼状图
    pie21 = []
    pie22 = []

    # 全球新增top10
    earth1 = []
    earth2 = []
    # 全球累计top10
    earth3 = []
    earth4 = []

    con = sqlite3.connect("cov.db")
    cur = con.cursor()

    sql1 = 'select * from country_his'
    data1 = cur.execute(sql1)
    for i in data1:
        time.append(i[0])
        nowconfirm.append(i[2])
        confirm.append(i[1])
        heal.append(i[3])
        dead.append(i[5])

        foreign_confirm.append(i[7])
        foreign_nowconfirm.append(i[8])

    sql2 = 'SELECT 省份名称,累计确诊 FROM province order by 累计确诊 desc LIMIT 7 OFFSET 1'
    data2 = cur.execute(sql2)
    for i in data2:
        name.append(i[0])
        num.append(i[1])

    sql3 = 'select 省份名称,累计确诊 from province'
    data3 = cur.execute(sql3)
    for i in data3:
        cmy.append([i[0], i[1]])
    for i in cmy:
        p2.append(i[0])
        p2.append(i[1])
        sql4 = f"select 城市名称,累计确诊 from city WHERE 省份名称 = '{i[0]}'"
        data4 = cur.execute(sql4)
        for j in data4:
            p3.append([j[0], j[1]])
        p2.append(p3)
        p1.append(p2)
        p3 = []
        p2 = []

    sql4 = 'select 国内累计接种,国内新增接种,国内接种率,全球累计接种,全球新增接种,全球接种率 from vaccines'
    data4 = cur.execute(sql4)
    for i in data4:
        vaccines.append(i)

    sql5 = 'select 新增确诊,现有确诊,累计确诊,累计治愈,累计死亡,当日新增境外 from country_now'
    data5 = cur.execute(sql5)
    for i in data5:
        table.append(i)

    sql6 = 'select 省份名称,现有确诊 FROM province where 现有确诊 != 0 '
    data6 = cur.execute(sql6)
    for i in data6:
        pie1.append(i)

    # 多少天没有新增的天数柱状图
    sql7 = 'select * FROM zero order by 天数 desc'
    data7 = cur.execute(sql7)
    for i in data7:
        pie21.append(i[0])
        pie22.append(i[1])

    # 全球新增top10
    sql8 = 'select 国家名称,新增确诊 FROM earth order by 新增确诊 desc limit 10'
    data8 = cur.execute(sql8)
    for i in data8:
        earth1.append(i[0])
        earth2.append(i[1])

    # 全球累计top10
    sql9 = 'select 国家名称,累计确诊 FROM earth order by 累计确诊 desc limit 10'
    data9 = cur.execute(sql9)
    for i in data9:
        earth3.append(i[0])
        earth4.append(i[1])

    cur.close()
    con.close()
    # 此时输出的数据格式为[['云南','12',[['昆明',‘13’],['大理','21']]],['上海','12',[['嘉定',‘13’],['浦东','21']]]]
    return render_template('picture.html', time=time, nowconfirm=nowconfirm, confirm=confirm, heal=heal, dead=dead,
                           name=name, num=num, p1=p1, vaccines=vaccines, table=table, foreign_confirm=foreign_confirm,
                           foreign_nowconfirm=foreign_nowconfirm, pie1=pie1, pie21=pie21, pie22=pie22, earth1=earth1,
                           earth2=earth2, earth3=earth3, earth4=earth4, zfh=zfh)



if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0',port=5000)
