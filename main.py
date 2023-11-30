from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
from datetime import datetime
from datetime import timedelta
from datetime import timezone

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)
timezone="Asia/Shanghai"
# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)

today = beijing_now.now()
time = str(beijing_now.date())+" "+beijing_now.date().strftime("%A")

# today = datetime.now()
# time = str(date.today())+" "+date.today().strftime("%A")

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather(city):
  url = "http://t.weather.itboy.net/api/weather/city/101120710" 
  res = requests.get(url).json()
  weather = res['data']['forecast'][0]
  return weather['type'], weather['low'], weather['high'], weather['notice']

def get_count():
  delta = datetime.now(pytz.timezone(timezone)) - datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=pytz.timezone(timezone))
  return delta.days

def get_retired():
  delta = datetime.strptime("2058-01-01", "%Y-%m-%d") - today
  return delta.days

def get_birthday():
  today1 = datetime.now(pytz.timezone(timezone)).date()
  next = datetime.strptime(str(today1.year) + "-" + birthday, "%Y-%m-%d").replace(tzinfo=pytz.timezone(timezone))
  if next < datetime.now(pytz.timezone(timezone)):
    next = next.replace(year=next.year + 1)
  return (next - datetime.now(pytz.timezone(timezone))).days

def get_words():
  url = "https://api.shadiao.pro/"
  param = ["du","chp","pyq"]
  url += str(param[random.randint(0,2)]) 
  words = requests.get(url)
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


citys = city.split()
datas = []
words_day = '报告：今天依旧也是爱老公的一天'
for index in range(len(citys)):
    wea, low, high, notice =  get_weather(citys[index])
    data = {}
    if index==0:
        data = {"time":{"value":time,"color":get_random_color()},"city":{"value":citys[index],"color":get_random_color()},"weather":{"value":wea,"color":get_random_color()},"low":{"value":low,"color":get_random_color()},"high":{"value":high,"color":get_random_color()},
                "days":{"value":get_count(),"color":get_random_color()},"birthday":{"value":get_birthday(),"color":get_random_color()},"words":{"value":notice, "color":get_random_color()}}
    elif index==4:
        data = {"time":{"value":time},"city":{"value":citys[index]},"weather":{"value":wea},"low":{"value":low},"high":{"value":high},"days":{"value":get_retired()},"words":{"value":get_words(), "color":get_random_color()}}
    else:
        data = {"time":{"value":time},"city":{"value":citys[index]},"weather":{"value":wea},"low":{"value":low},"high":{"value":high},"words":{"value":get_words(), "color":get_random_color()}}
    datas.append(data)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

users = user_id.split()
templates = template_id.split()
for index in range(len(users)):
   wm.send_template(users[index], template_id, datas[0])
