import requests

import requests
import json

def get_userid_by_mobile():
    with open('./config.json', "r", encoding="utf-8") as f:
        config = json.loads(f.read())
    config = config.get('config')[0]# 读取有推送配置的config
    qywx_corpid = config.get('qywx_corpid')
    qywx_agentid = config.get('qywx_agentid')
    qywx_corpsecret = config.get('qywx_corpsecret')
    qywx_touser = config.get('qywx_touser')
    res = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
    )
    access_token = res.json().get("access_token", False)
    print(access_token)
    department_id = 1
    url = f"https://qyapi.weixin.qq.com/cgi-bin/user/simplelist?access_token={access_token}&department_id={department_id}"
    response = requests.get(url)
    data = response.json()
    print(data)

# 获取userid
get_userid_by_mobile()
