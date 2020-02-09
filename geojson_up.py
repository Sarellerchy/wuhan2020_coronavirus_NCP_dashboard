import json
import requests
from spider import province_city_data

# 获取省市数据
def chinadata_get():
    province = requests.get('https://geo.datav.aliyun.com/areas/bound/100000_full.json')
    province.encoding = 'utf-8'
    json_province = json.loads(province.text)
    with open('./data/province.json','w',encoding='utf-8') as f:
        f.write(json.dumps(json_province,ensure_ascii=False))

    for i in range(0,34):
        url_city = 'https://geo.datav.aliyun.com/areas/bound/'\
                  +str(json_province['features'][i]['properties']['adcode'])+'_full.json'
        city = requests.get(url_city)
        city.encoding = 'utf-8'
        json_city = json.loads(city.text)
        with open('./data/city_'+str(json_province['features'][i]['properties']['adcode'])+'.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_city, ensure_ascii=False))
        print(str(json_province['features'][i]['properties']['name']+'地理位置数据更新完成'))

# 获取json数据
class geojson_combine():
    def province_json(self):
        province_count = province_city_data.data_result[0]
        province_area = json.load(open("./data/province.json", encoding='utf-8'))
        for item in province_area['features']:
            for i in province_count:
                if i[0] == item['properties']['name']:
                    item['properties']["confirm"] = int(i[1])
                    item['properties']["dead"] = int(i[2])
                    item['properties']["heal"] = int(i[3])
                    item['properties']["suspect"] = int(i[4])
        with open('./static/province_geojson.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(province_area, ensure_ascii=False))

# 地图标注数据
def map_tag(file_name):
    tag_data = json.load(open(file_name, encoding='utf-8'))
    tag_data_list = []
    for item in tag_data['features']:
        if item['properties']['name'] !='':
            tag_data_list.insert(len(tag_data_list),{'name':item['properties']['name'],
                                                     'j':item['properties']['center'][0],
                                                     'w':item['properties']['center'][1]})
    tag_data_json = {"list":tag_data_list}
    with open('./static/province_tag.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(tag_data_json, ensure_ascii=False))