# -*- coding: utf8 -*-
import json
from tool import check_one_place
from push_tool import send


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
        if config.get("push"):
            send(msg, now_balance_log, push_config)
        print("-----------------------------")


if __name__ == "__main__":
    main_handler()
