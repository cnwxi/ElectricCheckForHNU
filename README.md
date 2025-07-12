# 湖南大学 剩余电量查询
一个用于服务器定时查询HNU宿舍电量/电费余额的简单脚本<br>
- 设备/网络限制:
  - 一台长期开机使用的联网设备
  - 可以运行python脚本
  - 可以访问微信公众号“湖南大学-校园服务-校园缴费-在线购电”网页
    - 注：校内办理的校园宽带（如电信）无法访问hnu.edu.cn网址，请注意。
- 推送方式：
  - 使用qq邮箱（优先推荐）：QQ邮箱，启用smtp服务。QQ邮箱接入安卓/IOS推送服务情况良好，直接使用QQ邮箱客户端接收信息推送；可在微信中设置接收QQ邮件信息提醒。
    - 收信客户端：QQ邮箱、微信
    - 可自行修改代码调整为其他邮箱
  - server酱（一般）：免费账户必须点击链接查看详情，但够用。
    - 收信客户端：微信
  - 企业微信（如果已有则推荐，没有则不推荐，已限制个人注册）。
    - 收信客户端：微信
  - Showdoc（推荐）：从[showdoc](https://push.showdoc.com.cn/#/push)扫码绑定微信获得专属推送地址，可在公众号中获取信息，没有每日推送数量限制。
    - 收信客户端：微信

如果有其他推送需求，请参考网络上的其他仓库自行补充，向本仓库贡献代码或者提出issue并等待更新<br>

## 如何使用
1. 在长期运行的联网设备上克隆本仓库`git clone https://github.com/cnwxi/ElectricCheckForHNU.git`<br>
2. 配置好你的python环境，安装必要的依赖库`pip install request`或者`pip install -r requirements.txt`，使用requirements.txt文件时请注意先cd到对应文件夹下<br>
3. 参考说明文档 README.md 修改配置文件并重命名为`config.json`<br>
4. 使用`python /your path/ElectricCheckForHNU/index.py`测试是否正确配置并推送信息<br>
5. 配置定时任务使脚本定期运行查询电量。

### 以Linux例配置定时任务：
1. 进入终端
2. 输入`crontab -e`
3. 选择vi或者vim等编辑器，按下`a`在文件末尾添加`0 18 * * * cd /your path/ElectricCheckForHNU/ && python ./index.py`，按下`Esc`后输入`:wq`按下`Enter`保存文件，以定时每天18点查询电量。具体crontab前5位数值定义请搜索查阅相关信息。

### 青龙面板配置
1. 在【脚本管理】新建文件夹，以 `ElectricCheckForHNU` 为例，并上传所有项目文件；
2. 按照 `config.template.json` 示例文件，结合下方config文件解释，在脚本根目录（`ElectricCheckForHNU`）下添加 `config.json` 文件并保存；
3. 在【定时任务】创建任务，名称随意，命令/脚本填写 `task 该脚本文件夹名称/index.py`（如 `task ElectricCheckForHNU/index.py`），定时规则按照crontab规则写，其余默认。

## config文件解释
```
{
  "config": [
    { # 用户1
      "push": false, # 是否启用推送 true/false，如果不想每天收到推送可关闭
      "balance_limit": 10, # 无论是否启用推送，当余额小于10元均会推送
      "push_config": { # 所用推送方式需要的必要参数
        "type": "qywx", # 使用的推送方式：企业微信/server酱/qq邮箱/showdoc
        "qywx_corpid": "企业微信推送参数——企业编号",
        "qywx_agentid": "企业应用编号",
        "qywx_corpsecret": "企业应用密钥",
        "qywx_touser": "@all"
      },
      "dormitory_config": { # 宿舍信息
        "parkNo": "园区编号",
        "buildingNo": "楼栋号",
        "roomNo": "房间号",
        "username": "用户名1" # 若有同一宿舍用户，用于区分，避免文件读写错误
      }
    },
    { # 用户2
      "push": false,
      "balance_limit": 10,
      "push_config": {
        "type": "serverchan",
        "serverchan_key": "server酱密钥"
      },
      "dormitory_config": {
        "parkNo": "园区编号",
        "buildingNo": "楼栋号",
        "roomNo": "房间号",
        "username": "用户名2"
      }
    },
    { # 用户3
      "push": false,
      "balance_limit": 10,
      "push_config": {
        "type": "qqmail",
        "qqmail_user": "qq@qq.com", # 你的qq邮箱
        "qqmail_password": "smtp密钥" # qq邮箱启用smtp服务时生成的密钥
      },
      "dormitory_config": {
        "parkNo": "园区编号",
        "buildingNo": "楼栋号",
        "roomNo": "房间号",
        "username": "用户名3"
      }
    },
    { # 用户4
      "push": false,
      "balance_limit": 10,
      "push_config": {
        "type": "showdoc",
        "showdoc_url": "完整的showdoc推送链接" # 在showdoc官网微信扫码绑定/登录后获得的专属推送链接
      },
      "dormitory_config": {
        "parkNo": "园区编号",
        "buildingNo": "楼栋号",
        "roomNo": "房间号",
        "username": "用户名3"
      }
    }
  ]
}
```

### parkNo & buildingNo 参数说明

园区、楼栋后的数字为对应的parkNo、buildingNo代码，如下参数若未包含你所在宿舍：

①请使用fiddler classic在电脑上对微信公众号进行抓包：湖南大学-校园缴费-在线购电，选择你的宿舍，抓取所有相关的参数

②使用`python ./utils/updateNoInfo.py`脚本获取数据更新

③本仓库使用Github Action每月自动更新信息

```
温馨提示：
【学生电价：每度0.619元。交费高峰期，数据更新可能延时两小时。】
1. 南校区19舍附楼，请在房间号首位加上F，如：F201、F301、F401
2. 财院校区A栋，请在房间号首位加上A、B、C
3. 德智园区，请在房间号首位加上楼栋号2、5、6、7、8、9、10、11，如：2101（2栋101房）、10101（10栋101房）……
```
| 园区 | parkNo | 楼栋 | buildingNo |
|------|------|------|------|
| 南校区 | 1 | 7舍 | 19-1 |
|      |      | 8舍 | 20 |
|      |      | 10舍 | 21 |
|      |      | 11舍 | 21-0 |
|      |      | 12舍 | 21-1 |
|      |      | 13舍 | 21-2 |
|      |      | 14舍 | 22 |
|      |      | 15舍 | 23 |
|      |      | 17舍 | 24 |
|      |      | 18舍 | 25 |
|      |      | 19舍1号楼 | 25-1 |
|      |      | 19舍2号楼 | 25-2 |
|      |      | 19舍3号楼 | 25-3 |
|      |      | 19舍4号楼 | 25-4 |
|      |      | 南楼 | 26 |
|      |      | 培训小楼 | 27 |
| 财院校区 | 2 | 1栋 | 01 |
|      |      | 2栋 | 02 |
|      |      | 5栋 | 03 |
|      |      | 6栋 | 04 |
|      |      | 12栋 | 05 |
|      |      | A栋 | 06 |
|      |      | B栋 | 07 |
|      |      | 研楼7栋 | 08 |
| 天马园区 | 3 | 1区1栋 | 28 |
|      |      | 1区2栋 | 29 |
|      |      | 1区3栋 | 30 |
|      |      | 1区4栋 | 30-1 |
|      |      | 2区1栋 | 31 |
|      |      | 2区2栋 | 32 |
|      |      | 2区3栋 | 33 |
|      |      | 2区4栋 | 34 |
|      |      | 2区5栋 | 35 |
|      |      | 2区6栋 | 36 |
|      |      | 2区7栋 | 37 |
|      |      | 3区9栋 | 38 |
|      |      | 3区10栋 | 39 |
|      |      | 3区11栋 | 40 |
|      |      | 3区12栋 | 41 |
|      |      | 3区13栋 | 42 |
|      |      | 3区16栋 | 43 |
|      |      | 3区17栋 | 44 |
|      |      | 3区18栋 | 45 |
|      |      | 3区19栋 | 46 |
|      |      | 3区20栋 | 46-1 |
|      |      | 4区1栋 | 47 |
|      |      | 4区2栋 | 48 |
|      |      | 4区3栋 | 49 |
|      |      | 4区4栋 | 50 |
| 德智园区 | 4 | 2栋 | 09 |
|      |      | 5栋 | 10 |
|      |      | 6栋 | 11 |
|      |      | 7栋 | 12 |
|      |      | 8栋 | 13 |
|      |      | 9栋 | 14 |
|      |      | 10栋 | 15 |
|      |      | 11栋 | 16 |
|      |      | 13栋 | 17 |
| 德智留学生公寓 | 5 | 留学生公寓(照明+热水+冷水) | 18 |
| 望麓桥学生公寓 | 6 | 1栋 | 51 |
|      |      | 2栋北 | 52 |
|      |      | 2栋南 | 53 |
|      |      | 3栋北 | 54 |
|      |      | 3栋南 | 55 |
|      |      | 4栋 | 57 |

最后更新时间（北京时间）：2025-07-09 16:28:23
