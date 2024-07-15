# -*- coding: utf8 -*-
import requests
import json
import os
import datetime

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
        "msgtype": "text",
        "text": {
            "content": f"HNU电费查询 | by cnwxi\n{content}",
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
    msg = []
    if ret.get("res") == "success":
        result = ret.get("data", {})
        msg.append({"name": "宿舍", "value": f"{result.get('ParkName')}{result.get('BuildingName')}{result.get('RoomNo')}"})
        # msg.append({"name": "楼栋", "value": result.get('BuildingName')})
        # msg.append({"name": "房号", "value": result.get('RoomNo')})
        msg.append({"name": "当前电费", "value": result.get('Balance')})
        format_str = "%Y/%m/%d|%H:%M:%S"
        current_time = datetime.datetime.now().strftime(format_str)
        last_log=None
        final_write_mode='a'
        if os.path.exists("./log"):
            with open("./log","rb") as log_file:
                try:
                    log_file.seek(-2, 2)  # 将光标移动到文件的末尾位置的倒数第二个字节
                    if log_file.tell() == 0:
                        last_log = log_file.read().decode('utf-8').strip()
                    else:
                        while log_file.read(1) != b'\n':  # 查找倒数第二个换行符
                            log_file.seek(-2, 1)  # 将光标向前移动两个字节
                            if log_file.tell() == 0:
                                break
                    last_log = log_file.readline().decode('utf-8')  # 读取最后一行内容
                    last_time=last_log.split(' ',1)[0]
                    nd=datetime.datetime.strptime(current_time,format_str)
                    ld=datetime.datetime.strptime(last_time,format_str)
                    tmp = f"{(nd-ld).total_seconds()/60/60:.2f}小时"
                    if (nd-ld).total_seconds()/60/60 < 1: # 小时
                         tmp = f"{(nd-ld).total_seconds()/60:.2f}分钟"
                    if (nd-ld).total_seconds()/60 < 1: # 分钟
                         tmp = f"{(nd-ld).total_seconds():.2f}秒"
                    delta=tmp
                    msg.append({"name": "上次查询", "value": last_time})
                    msg.append({"name": "查询间隔", "value": delta})
                    last_balance=float(last_log.rsplit(' ',1)[-1].replace('元',''))
                    now_balance=float(result.get("Balance").replace('元',''))
                    cost=now_balance-last_balance
                    msg.append({"name": "电费变动", "value": f"{cost:.2f}元"})
                    if cost>0: # 充值 刷新log,避免文件占用过大
                        print('覆盖写入记录文件')
                        final_write_mode='w'
                except:
                    print("error")
        else:
            msg.append({"name": "首次查询", "value": current_time})

        with open("./log",final_write_mode) as log_file:
                log_content=f"{current_time} {result.get('ParkName')}{result.get('BuildingName')}{result.get('RoomNo')} {result.get('Balance')}\n"
                log_file.write(log_content)
               
        
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
    
    
