from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather(city):
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_retired():
  delta = datetime.strptime("2058-01-01", "%Y-%m-%d") - today
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

citys = city.split()
datas = []
for index in range(len(citys)):
    wea, temperature = get_weather(citys[index])
    data = {}
    if index==0:
        data = {"weather":{"value":wea},"temperature":{"value":temperature},"days":{"value":get_count()},"birthday":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
    elif index==4:
        data =  {"weather":{"value":wea},"temperature":{"value":temperature},"days":{"value":get_retired()},"words":{"value":get_words(), "color":get_random_color()}}
    else:
        data = {"weather":{"value":wea},"temperature":{"value":temperature},"words":{"value":get_words(), "color":get_random_color()}}
    datas.append(data)

client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

users = user_id.split()
templates = template_id.split()
for index in range(len(users)):
   wm.send_template(users[index], templates[index], datas[index])
