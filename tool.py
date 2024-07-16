import re
import requests
import datetime
import json
import os

format_str = "%Y/%m/%d|%H:%M:%S"


def check_one_place(config):
    ret = http_request(config)
    msg = []
    if ret.get("res") == "success":
        result = ret.get("data", {})
        place = f"{result.get('ParkName')}{result.get('BuildingName')}{result.get('RoomNo')}"
        msg.append({"name": "宿舍", "value": place})
        msg.append({"name": "当前余额", "value": result.get('Balance')})
        current_time = datetime.datetime.now().strftime(format_str)
        last_log = None
        final_write_mode = 'a'
        log_file_path = f"./log/{place}"
        if os.path.exists(log_file_path):
            with open(log_file_path, "rb") as log_file:
                try:
                    log_file.seek(-2, 2)  # 将光标移动到文件的末尾位置的倒数第二个字节
                    if log_file.tell() == 0:
                        last_log = log_file.read().decode('utf-8').strip()
                    else:
                        while log_file.read(1) != b'\n':  # 查找倒数第二个换行符
                            log_file.seek(-2, 1)  # 将光标向前移动两个字节
                            if log_file.tell() == 0:
                                break
                    last_log = log_file.readline().decode('utf-8').replace(
                        '\n', '')  # 读取最后一行内容
                    last_time = last_log.split(' ', 1)[0]
                    delta = cal_time(current_time, last_time)
                    msg.append({"name": "上次查询", "value": last_time})
                    msg.append({"name": "当前查询", "value": current_time})
                    msg.append({"name": "查询间隔", "value": delta})
                    last_balance_log = last_log.rsplit(' ', 1)[-1]
                    last_balance, unit = extract_value_and_unit(
                        last_balance_log)
                    now_balance_log = result.get("Balance")
                    now_balance, _ = extract_value_and_unit(now_balance_log)
                    cost = now_balance - last_balance
                    msg.append({"name": "电费变动", "value": f"{cost:.2f}{unit}"})
                    if cost > 0:  # 充值 刷新log,避免文件占用过大
                        print('覆盖写入记录文件')
                        final_write_mode = 'w'
                except:
                    print("error")
        else:
            msg.append({"name": "首次查询", "value": current_time})
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        with open(log_file_path, final_write_mode) as log_file:
            log_content = f"{current_time} {result.get('ParkName')}{result.get('BuildingName')}{result.get('RoomNo')} {result.get('Balance')}\n"
            log_file.write(log_content)
    else:
        msg.append({"name": "查询结果", "value": ret.get("msg")})
    msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])    
    return msg,now_balance_log


def cal_time(current_time, last_time):
    nd = datetime.datetime.strptime(current_time, format_str)
    ld = datetime.datetime.strptime(last_time, format_str)
    tmp = (nd - ld).total_seconds()
    if tmp / 60 < 1:
        tmp = tmp
        unit = '秒'
    elif tmp / 60 / 60 < 1:
        tmp = tmp / 60  # 分钟
        unit = '分钟'
    elif tmp / 60 / 60 < 1:
        tmp = tmp / 60 / 60
        unit = '小时'
    else:
        tmp = tmp / 60 / 60 / 24
        unit = '天'
    if tmp // 1 == 0:
        tmp = int(tmp)
    else:
        tmp = round(tmp, 2)
    return f"{tmp}{unit}"


def extract_value_and_unit(s):
    # 使用正则表达式匹配数字和单位
    match = re.match(r"(\d+\.\d+)(\D+)", s)

    if match:
        value = float(match.group(1))  # 第一个分组是数字部分
        unit = match.group(2)  # 第二个分组是单位部分

        return value, unit
    else:
        return None, None


def http_request(config):
    headers = {
        "Host": "wxpay.hnu.edu.cn",
        # "Proxy-Connection": "keep-alive",
        "Accept": "*/*",
        "User-Agent":
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6305002e)",
        "X-Requested-With": "XMLHttpRequest",
        # "Cookie": config.get('cookies'),
        "refere": "http://wxpay.hnu.edu.cn/electricCharge/home/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    url = f"http://wxpay.hnu.edu.cn/api/appElectricCharge/checkRoomNo?parkNo={config.get('parkNo')}&buildingNo={config.get('buildingNo')}&rechargeType=2&roomNo={config.get('roomNo')}"
    ret = requests.get(url=url, headers=headers).json()
    return ret
