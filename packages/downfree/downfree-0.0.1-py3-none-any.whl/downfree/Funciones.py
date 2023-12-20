from pathlib import Path
from bs4 import BeautifulSoup
import requests
import os
from colorama import Fore , init
import shutil
import ast
import os
import platform
sistema_operativo = platform.system()
import urllib3
import urllib
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import pymongo
from pymongo import MongoClient
import dns.resolver
from pyshortext import unshort
import time
import sys
sys.setrecursionlimit(1500)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"}
# Database
DATABASE = "mongodb+srv://hiyabo23:aDhVDUC2-@chunks.nvltccv.mongodb.net/?retryWrites=true&w=majority"
CLIENT_MONGO = MongoClient(DATABASE, serverSelectionTimeoutMS=9999999) 

Global_c = CLIENT_MONGO["Downloads_Config" ] #! Globales 

Global_configs = Global_c["downloads_config"]  

c_user = Global_configs.find_one({"Global_c" : "Down_Free"})

def make_session(dl):
    session = requests.Session()
    username = dl['u']
    password = dl['p']
    if dl['m'] == 'm':
      return session
    if dl['m'] == 'moodle':
        if dl['c'] == "https://evea.uh.cu/" and not dl['u']:
            username = c_user['user_evea']
            password = c_user['pass_evea']
        elif dl['c'] == "https://eva.uo.edu.cu/" and not dl['u']:
            username = c_user['user_eva']
            password = c_user['pass_eva']
        url = dl['c']+'login/index.php'
    elif dl["m"] == "mined":
        url = "https://bienestar-apmined.xutil.net/"
        resp = session.get(url+"sysapmined/esES/neoclassic/services/webentry/anonymousLogin?we_uid=5819359306473f170cb9eb1049011769",headers={"Upgrade-Insecure-Requests":"1",**headers})
        resp = session.get(url+"sysapmined/esES/neoclassic/cases/cases_Open?APP_UID=81475984365760ce3e22133018715878&DEL_INDEX=1&action=draft",headers={"Upgrade-Insecure-Requests":"1",**headers})
        return session
    else:
      url = dl['c'].split('/$$$call$$$')[0]+ '/login/signIn'
    resp = session.get(url,headers=headers,allow_redirects=True,verify=False)
    soup = BeautifulSoup(resp.text, "html.parser")
    if dl['m'] == 'moodle':
      try:
        token = soup.find("input", attrs={"name": "logintoken"})["value"]
        payload = {"anchor": "",
        "logintoken": token,
        "username": username,
        "password": password,
        "rememberusername": 1}
      except:
        payload = {"anchor": "",
        "username": username,
        "password": password,
        "rememberusername": 1}
    elif dl["m"] == "mined":
        CSRFToken = soup.find("input",attrs={"name":"__CSRFToken__"})["value"]
        payload = {"__CSRFToken__": CSRFToken,"luser": dl["u"],"lpasswd": dl["p"]}
    else:
      try:
          csrfToken = soup.find('input',{'name':'csrfToken'})['value']
          payload = {}
          payload['csrfToken'] = csrfToken
          payload['source'] = ''
          payload['username'] = username
          payload['password'] = password
          payload['remember'] = '1'
      except Exception as ex:
          print(ex)
    
    resp = session.post(url,headers=headers,data=payload,verify=False)
    if resp.url!=url:
        return session
    return None