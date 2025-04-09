import requests

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
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
}

tips = "园区、楼栋后的数字为对应的parkNo、buildingNo代码,如下参数若未包含你所在宿舍：\n\n①请使用fiddler classic在电脑上对微信公众号进行抓包：湖南大学-校园缴费-在线购电，选择你的宿舍，抓取所有相关的参数\n\n②使用本仓库中`updateNoInfo.py`脚本获取数据更新\n\n```温馨提示：\n【学生电价：每度0.619元。交费高峰期，数据更新可能延时两小时。】\n1. 南校区19舍附楼，请在房间号首位加上F，如：F201、F301、F401\n2. 财院校区A栋，请在房间号首位加上A、B、C\n3. 德智园区，请在房间号首位加上楼栋号2、5、6、7、8、9、10、11，如：2101（2栋101房）、10101（10栋101房）……\n```\n"


def getParkNo():
    url = "http://wxpay.hnu.edu.cn/api/appElectricCharge/parklist"
    ret = requests.get(url=url, headers=headers).json()
    print(f"查询返回json：{ret}")
    if ret.get("msg") == "成功":
        parkList = ret.get("data")
    else:
        print("查询失败")
        parkList = []
    return parkList


def getBuildingNo(parkNo):
    url = f"http://wxpay.hnu.edu.cn/api/appElectricCharge/buildinglist?parkNo={parkNo}"
    ret = requests.get(url=url, headers=headers).json()
    print(f"查询返回json：{ret}\n")
    if ret.get("msg") == "成功":
        buildingList = ret.get("data")
    else:
        print("查询失败")
        buildingList = []
    return buildingList


def getTips():
    url = "http://wxpay.hnu.edu.cn/electricCharge/home/"
    ret = requests.get(url=url, headers=headers)
    print(f"查询返回json：{ret}")


def processList(someList):
    result = []
    for i in someList:
        result.append([i.get("Name"), i.get("Code")])
    print(f"处理后的数据：{result}\n")
    # 处理后的数据格式为[[名称, 编号], [名称, 编号], ...]
    return result


def getMarkDown(allInfoList):
    markdown_table = "| 园区 | parkNo | 楼栋 | buildingNo |\n"
    markdown_table += "|------|------|------|------|\n"
    for i, parkInfo in enumerate(allInfoList):
        name = parkInfo[0]
        no = parkInfo[1]
        buildingNoList = parkInfo[2]
        for j, buildingInfo in enumerate(buildingNoList):
            if j == 0:
                markdown_table += f"| {name} | {no} | {buildingInfo[0]} | {buildingInfo[1]} |\n"
            else:
                markdown_table += f"|      |      | {buildingInfo[0]} | {buildingInfo[1]} |\n"
        # if i != len(allInfoList) - 1:
        #     markdown_table += "|------|------|------|------|\n"
    print(f"markdown_table：\n{markdown_table}")
    return markdown_table


def storeInfo(allInfoList):
    with open("allInfo.md", "w", encoding="utf-8") as f:
        f.write(markdown_table)


def repalce(newInfo):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    # 找到目标段落之前的所有内容
    target_paragraph = "### parkNo & buildingNo 参数说明\n\n"
    target_index = readme.find(target_paragraph)
    # 如果找到了目标段落
    if target_index != -1:
        print(f"找到目标段落")
        # 将目标段落之前的内容和新的内容拼接起来
        new_readme = readme[:target_index] + target_paragraph + tips + markdown_table
        print(f"更新README.md内容")
    else:
        # 如果没有找到目标段落，则直接在文件末尾添加新的内容
        new_readme = readme + "\n" + tips + markdown_table
    # 写入新的README.md文件
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)


if __name__ == "__main__":
    # 获取所有的parkNo
    parkList = getParkNo()
    # 处理parkList
    parkNoList = processList(parkList)
    # 获取所有的buildingNo
    finalAllInfoList = []
    for i in parkNoList:
        name = i[0]
        no = i[1]
        # 获取该园区的所有楼栋
        buildingList = getBuildingNo(no)
        # 处理buildingList
        buildingNoList = processList(buildingList)
        finalAllInfoList.append([name, no, buildingNoList])
    # 打印最终的结果
    print(f"所有信息：{finalAllInfoList}")
    # 获取markdown格式的表格
    markdown_table = getMarkDown(finalAllInfoList)
    # 写入文件
    storeInfo(finalAllInfoList)
    # 替换README.md中的内容
    repalce(finalAllInfoList)

    # 获取提示信息
