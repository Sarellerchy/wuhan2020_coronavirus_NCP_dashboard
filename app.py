from flask import Flask,render_template
from spider import  data_total,news_data
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html",confirmtotal = '{:,}'.format(data_total.gntotal),suspecttotal = '{:,}'.format(data_total.sustotal),
                           healtotal = '{:,}'.format(data_total.curetotal),deadtotal = '{:,}'.format(data_total.deathtotal),
                           news_01_time = news_data.news_list[0][3]+'  '+news_data.news_list[0][2],news_01_title = news_data.news_list[0][0],
                           news_02_time = news_data.news_list[1][3]+'  '+news_data.news_list[1][2],news_02_title = news_data.news_list[1][0],
                           news_03_time = news_data.news_list[2][3]+'  '+news_data.news_list[2][2],news_03_title = news_data.news_list[2][0],
                           news_01_link = news_data.news_list[0][1],news_02_link = news_data.news_list[1][1],news_03_link = news_data.news_list[2][1],
                           line_y_json = json.loads(data_total.df_data_total_history.sort_values(by='date')[['date','confirm','dead','heal','suspect']].
                                                       to_json(orient = 'records', force_ascii = False)))


if __name__ == '__main__':
    app.run()
