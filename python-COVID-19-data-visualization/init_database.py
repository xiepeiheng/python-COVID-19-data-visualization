import sqlite3

savepath = 'cov.db'

#创建预测部分的表格

sql1 = '''
    create table 俄罗斯
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric
    );
'''
sql2 = '''
    create table 巴西
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric
    );
'''
sql3 = '''
    create table 德国
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric    
    );
'''
sql4 = '''
    create table 意大利
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric    
    );
'''
sql5 = '''
    create table 法国
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric    
    );
'''
sql6 = '''
    create table 美国
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric    
    );
'''
sql7 = '''
    create table 英国
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric    
    );
'''
sql8 = '''
    create table 西班牙
    (
    时间 text,
    累计确诊 numeric,
    序号 numeric,
    预测 numeric    
    );
'''
#创建数据屏所需的库

sql9 = '''
    create table country_his
    (
    时间 text,
    累计确诊 numeric,
    当日新增确诊 numeric,
    累计治愈 numeric,
    当日新增治愈 numeric,
    累计死亡 numeric,
    当日新增死亡 numeric,
    累计境外输入 numeric,
    当日新增境外输入 numeric
    );
'''

# 创建各省份表
sql10 = '''
    create table province
    (
    省份名称 text,
    新增确诊 numeric,
    现有确诊 numeric,
    累计确诊 numeric,
    累计治愈 numeric,
    累计死亡 numeric
    )
'''

# 创建全国今日数据表
sql11 = '''
    create table country_now
    (
    累计确诊 numeric,
    累计治愈 numeric,
    累计死亡 numeric,
    现有确诊 numeric,
    新增确诊 numeric,
    当日新增境外 numeric,
    累计境外 numeric
    )
'''

# 创建详情页数据表
sql12 = '''
    create table city
    (
    省份名称 text,
    城市名称 text,
    新增确诊 numeric,
    现有确诊 numeric,
    累计确诊 numeric,
    累计治愈 numeric,
    累计死亡 numeric
    )
'''

# 创建百度热搜词表
sql13 = '''
    create table baidu
    (
    热搜词条 text
    )
    '''

# 创建疫苗接种情况表
sql14 = '''
    create table vaccines
    (
    国内累计接种 text,
    国内新增接种 text,
    国内接种率 text,
    全球累计接种 text,
    全球新增接种 text,
    全球接种率 text
    )
    '''

sql15 = '''
    create table zero
    (
    省份名称 text,
    天数 numeric
    )           
'''

sql16 = '''
    create table earth
    (
    国家名称 text,
    新增确诊 numeric,
    累计确诊 numeric,
    累计治愈 numeric,
    累计死亡 numeric
    )           
'''

conn = sqlite3.connect(savepath)
cursor = conn.cursor()

cursor.execute(sql1)
cursor.execute(sql2)
cursor.execute(sql3)
cursor.execute(sql4)
cursor.execute(sql5)
cursor.execute(sql6)
cursor.execute(sql7)
cursor.execute(sql8)
cursor.execute(sql9)
cursor.execute(sql10)
cursor.execute(sql11)
cursor.execute(sql12)
cursor.execute(sql13)
cursor.execute(sql14)
cursor.execute(sql15)
cursor.execute(sql16)

conn.commit()
conn.close()

print('数据库创建完成')