import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def qxwx_push(content, balance_log, config):
    print("企业微信应用消息推送开始")
    qywx_corpid = config.get("qywx_corpid")
    qywx_agentid = config.get("qywx_agentid")
    qywx_corpsecret = config.get("qywx_corpsecret")
    qywx_touser = config.get("qywx_touser")
    res = requests.get(
        f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
    )
    token = res.json().get("access_token", False)
    data = {
        "touser": qywx_touser,
        "agentid": int(qywx_agentid),
        "msgtype": "text",
        "text": {
            "content": f"HNU电费查询: {balance_log}\n\n{content}",
        },
    }
    res = requests.post(
        url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
        data=json.dumps(data),
    )
    res = res.json()
    if res.get("errcode") == 0:
        print("企业微信应用消息推送成功")
    else:
        print("企业微信应用消息推送失败")


def serverchan_push(content, balance_log, config):
    print("Server酱推送开始")
    serverchan_key = config.get("serverchan_key")
    text = f"HNU电费查询: {balance_log}"
    content = content.replace("\n", "\n\n")
    res = requests.post(
        f"https://sctapi.ftqq.com/{serverchan_key}.send?title={text}&desp={content}"
    )
    res = res.json()
    if res.get("code") == 0 and res.get("data").get("errno") == 0:
        print("Server酱推送成功")
    else:
        print("Server酱推送失败")

def showdoc_push(content, balance_log, config):
    print("Showdoc推送开始")
    showdoc_url = config.get("showdoc_url")
    text = f"HNU电费查询: {balance_log}"
    content = content.replace("\n", "\n\n")
    res = requests.post(
        f"{showdoc_url}?title={text}&content={content}"
    )
    res = res.json()
    if res.get("error_code") == 0:
        print("Showdoc推送成功")
    else:
        print("Showdoc推送失败")

def qqmail_push(content, balance_log, config):
    print("QQ邮箱推送开始")
    qqmail_user = config.get("qqmail_user")
    qqmail_password = config.get("qqmail_password")
    qqmail_to = qqmail_user  # 默认发送到自己
    
    msg = MIMEText(f"{content}", 'plain', 'utf-8')
    msg['Subject'] = Header(f'HNU电费查询: {balance_log}', 'utf-8')
    msg['From'] = qqmail_user
    msg['To'] = qqmail_to

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(qqmail_user, qqmail_password)
        server.sendmail(qqmail_user, qqmail_to, msg.as_string())
        print("QQ邮箱推送成功")
    except Exception as e:
        print(f"QQ邮箱推送失败: {e}")
    finally:
        server.quit()

def send(content, balance_log, config):
    if config.get("type") == "qywx":
        qxwx_push(content, balance_log, config)
    elif config.get("type") == "serverchan":
        serverchan_push(content, balance_log, config)
    elif config.get("type") == "showdoc":
        showdoc_push(content, balance_log, config)
    elif config.get("type") == "qqmail":
        qqmail_push(content, balance_log, config)
    else:
        print("未知推送方式")
    return
