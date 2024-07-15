# -*- coding: utf8 -*-
import requests
import json


def send(content, config):
    print("企业微信应用消息推送开始")
    qywx_corpid = config.get('qywx_corpid')
    qywx_agentid = config.get('qywx_agentid')
    qywx_corpsecret = config.get('qywx_corpsecret')
    qywx_touser = config.get('qywx_touser')
    res = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
    )
    token = res.json().get("access_token", False)
    data = {
        "touser": qywx_touser,
        "agentid": int(qywx_agentid),
        "msgtype": "textcard",
        "textcard": {
            "title": "电费查询",
            "description": content,
            "url": "URL",
        },
    }
    requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", data=json.dumps(data))
    return


def main_handler():
    with open('./config.json', "r",
              encoding="utf-8") as f:
        config = json.loads(f.read())
    url = f"http://wxpay.hnu.edu.cn/api/appElectricCharge/checkRoomNo?parkNo={config.get('parkNo')}&buildingNo={config.get('buildingNo')}&rechargeType=2&roomNo={config.get('roomNo')}"
    # http://wxpay.hnu.edu.cn/api/appElectricCharge/checkRoomNo?parkNo?parkNo={config.get('parkNo')}&buildingNo={config.get('buildingNo')}&rechargeType=2&roomNo={config.get('roomNo')}
    headers = {
        "Host": "wxpay.hnu.edu.cn",
        "Proxy-Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6305002e)",
        "X-Requested-With": "XMLHttpRequest",
        # "Cookie": config.get('cookies'),
        "refere": "http://wxpay.hnu.edu.cn/electricCharge/home/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    ret = requests.get(url=url, headers=headers).json()
    print(ret)
    msg = []
    if ret.get("res") == "success":
        result = ret.get("data", {})
        msg.append({"name": "园区", "value": result.get("ParkName")})
        msg.append({"name": "楼栋", "value": result.get("BuildingName")})
        msg.append({"name": "房号", "value": result.get("RoomNo")})
        msg.append({"name": "电费", "value": result.get("Balance")})
    else:
        msg.append({"name": "查询结果", "value": ret.get("msg")})
    msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
    print(msg)
    if config.get('push'):
        try:
            send(content=msg, config=config)
        except Exception as e:
            print("企业微信应用消息推送失败", e)
    return

if __name__ == "__main__":
    main_handler()
    
    
