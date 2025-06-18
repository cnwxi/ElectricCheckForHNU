# -*- coding: utf8 -*-
import json
from utils.tool import check_one_place
from utils.push_tool import send
from utils.tool import extract_value_and_unit

def main_handler():
    with open("./config.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())
    config_list = config.get("config")
    print("-----------------------------")
    for config in config_list:
        dormitory_config = config.get("dormitory_config")
        push_config = config.get("push_config")
        msg, now_balance_log = check_one_place(dormitory_config)
        print(msg)
        now_balance, unit = extract_value_and_unit(now_balance_log)
        if unit == "度":
            now_balance=now_balance * 0.619  # 电费转换为元
            print(f"当前余额转换为元: {now_balance:.2f}元")
        if config.get("push") or now_balance <= config.get('balance_limit'): # 如果开启推送或余额小于等于设定的限制金额则推送信息
            send(msg, now_balance_log, push_config)
        print("-----------------------------")


if __name__ == "__main__":
    main_handler()
