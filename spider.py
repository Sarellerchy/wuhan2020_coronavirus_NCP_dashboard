import requests
import json
import pandas as pd

# 全国数据
class data_total():
    data_total_html = requests.get('https://interface.sina.cn/news/wap/fymap2020_data.d.json?')
    data_total_html.encoding = 'utf-8'
    data_total_json = json.loads(data_total_html.text)
    mtime = data_total_json['data']['mtime'] # 数据更新时间
    cachetime = data_total_json['data']['cachetime'] # 网页刷新时间
    gntotal = int(data_total_json['data']['gntotal']) # 确诊
    deathtotal = int(data_total_json['data']['deathtotal']) # 死亡
    sustotal = int(data_total_json['data']['sustotal']) # 疑似
    curetotal = int(data_total_json['data']['curetotal']) # 治愈
    # by day
    data_total_history = []
    for item in data_total_json['data']['historylist']:
        data_total_history.insert(len(data_total_history),[item['date'],item['cn_conNum'],item['cn_deathNum'],item['cn_cureNum'],item['cn_susNum']])
    df_data_total_history = pd.DataFrame(data_total_history)
    df_data_total_history.columns = ['date','confirm','dead','heal','suspect']
    # 世界数据
    data_total_worldlist = []
    for item in data_total_json['data']['worldlist']:
        data_total_worldlist.insert(len(data_total_worldlist),[item['name'],item['value'],item['deathNum'],item['cureNum'],item['susNum']])
    df_data_total_worldlist = pd.DataFrame(data_total_worldlist)
    df_data_total_worldlist.columns = ['country','confirm','dead','heal','suspect']

# 各省份数据
class province_city_data():
    def province_data(url,province_list,city_list,history_list):
        data_province_html = requests.get(url)
        data_province_html.encoding = 'utf-8'
        data_province_json = json.loads(data_province_html.text)
        province_list.insert(len(province_list),[data_province_json['data']['province'],data_province_json['data']['contotal'],
                                             data_province_json['data']['deathtotal'],data_province_json['data']['curetotal'],
                                             data_province_json['data']['sustotal']])
        for item in data_province_json['data']['city']:
            city_list.insert(len(city_list),[data_province_json['data']['province'],item['mapName'],item['conNum'],item['deathNum'],item['cureNum'],item['susNum']])
        for date_item in data_province_json['data']['historylist']:
            history_list.insert(len(history_list),[data_province_json['data']['province'],date_item['date'],date_item['conNum'],
                                               date_item['deathNum'],date_item['cureNum'],date_item['susNum']])
        return province_list,city_list,history_list

    province_data_list = []
    city_data_list = []
    history_data_list = []
    province_name = [provincename.strip() for provincename in open('./notes/provincename.txt').readlines() ]
    for item in province_name:
        url_province = 'https://interface.sina.cn/news/wap/historydata.d.json?province='+item
        data_result = province_data(url_province,province_data_list,city_data_list,history_data_list)
    df_province_data_list = pd.DataFrame(data_result[0])
    df_province_data_list.columns = ['province','confirm','dead','heal','suspect']
    df_city_data_list = pd.DataFrame(data_result[1])
    df_city_data_list.columns = ['province','city','confirm','dead','heal','suspect']
    df_history_data_list = pd.DataFrame(data_result[2])
    df_history_data_list.columns = ['province','date','confirm','dead','heal','suspect']

# 疫情动态
class news_data():
    url_news = 'https://interface.sina.cn/wap_api/wap_std_subject_feed_list.d.json?component_id=_conf_13|wap_zt_std_theme_timeline|http://news.sina.cn/zt_d/yiqing0121&page='
    news_list = []
    for i in range(0,100):
        news_data_html = requests.get(url_news+str(i))
        news_data_html.encoding = 'utf-8'
        news_data_json = json.loads(news_data_html.text)
        if news_data_json['result']['data']['data'] != []:
            for item in news_data_json['result']['data']['data']:
                news_list.insert(len(news_list),[item['title'],item['url'],item['media'],item['date']])
    df_news = pd.DataFrame(news_list)
    df_news.columns = ['title','link','media','date']