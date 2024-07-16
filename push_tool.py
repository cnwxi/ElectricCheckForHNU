import requests
import json


def qxwx_push(content, now_balance, config):
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
        "msgtype": "text",
        "text": {
            "content": f"HNU电费查询|{now_balance}\n{content}",
        },
    }
    res = requests.post(
        url=
        f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
        data=json.dumps(data))
    res = res.json()
    if res.get("errcode") == 0:
        print("企业微信应用消息推送成功")
    else:
        print("企业微信应用消息推送失败")


def serverchan_push(content, now_balance, config):
    print("Server酱推送开始")
    serverchan_key = config.get('serverchan_key')
    text = f"HNU电费查询|{now_balance}"
    content = content.replace("\n", "\n\n")
    print(text)
    res = requests.post(
        f"https://sc.ftqq.com/{serverchan_key}.send?title={text}&desp={content}")
    res = res.json()
    if res.get("code") == 0 and res.get('data').get('errno') == 0:
        print("Server酱推送成功")
    else:
        print("Server酱推送失败")


def send(content, now_balance, config):
    if config.get('type') == 'qywx':
        qxwx_push(content, now_balance, config)
    elif config.get('type') == 'serverchan':
        serverchan_push(content, now_balance, config)
    else:
        print("未知推送方式")
    return
