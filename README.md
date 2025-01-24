# 湖南大学 剩余电量查询
一个用于服务器定时查询HNU宿舍电量/电费余额的简单脚本<br>
使用企业微信（不推荐）、server酱（推荐）作为信息推送<br>
如果有其他推送需求，请参考网络上的其他仓库自行补充，向本仓库贡献代码或者提出issue并等待更新<br>

## 如何使用
1. 在长期运行的联网设备上克隆本仓库`git clone https://github.com/cnwxi/ElectricCheckForHNU.git`<br>
2. 配置好你的python环境，安装必要的依赖库`pip install request`或者`pip install -r requirements.txt`，使用requirements.txt文件时请注意先cd到对应文件夹下<br>
3. 参考说明文档 README.md 修改配置文件并重命名为`config.json`<br>
4. 使用`python /your path/ElectricCheckForHNU/index.py`测试是否正确配置并推送信息<br>
5. 配置定时任务使脚本定期运行查询电量。

以Linux例配置定时任务：
1. 进入终端
2. 输入`crontab -e`
3. 选择vi或者vim等编辑器，按下`a`在文件末尾添加`0 18 * * * cd /your path/ElectricCheckForHNU/ && python ./index.py`，按下`Esc`后输入`:wq`按下`Enter`保存文件，以定时每天18点查询电量。具体crontab前5位数值定义请搜索查阅相关信息。
---

## config文件解释
```
{
  "config": [
    { # 用户1
      "push": false, # 是否启用推送 true/false
      "push_config": { # 所用推送方式需要的必要参数
        "type": "qywx", # 使用的推送方式：企业微信/server酱
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
    }
  ]
}
```

### parkNo & buildingNo 参数说明

园区、楼栋后的数字为对应的parkNo、buildingNo代码<br>
如下参数若未包含你所在宿舍，请使用fiddler classic在电脑上对微信公众号进行抓包：湖南大学-校园缴费-在线购电，选择你的宿舍。<br>
该操作可以抓取所有相关的参数<br>


### 南校区 `1`

8舍 `20` 10舍 `21` 14舍 `22`
15舍 `23` 17舍 `24` 18舍 `25`
南楼 `26` 培训小楼 `27`

### 财院校区 `2`

1栋 `01` 2栋 `02` 5栋 `03`
6栋 `04` 12栋 `05` A栋 `06`
B栋 `07` 研楼7栋 `08`

```财院校区A栋，请在房间号首位加上A、B、C ```

### 天马园区 `3`

1区1栋 `28` 1区2栋 `29` 1区3栋 `30`<br>
2区1栋 `31` 2区2栋 `32` 2区3栋 `33`
2区4栋 `34` 2区5栋 `35` 2区6栋 `36`
2区7栋 `37`  <br>
3区9栋 `38` 3区10栋 `39`
3区11栋 `40` 3区12栋 `41` 3区13栋 `42`
3区16栋 `43` 3区17栋 `44` 3区18栋 `45`
3区19栋 `46` 3区20栋 `46-1`<br>
4区1栋 `47` 4区2栋 `48`
4区3栋 `49` 4区4栋 `50` 事务大楼 `56`<br>

### 德智园区 `4`

2栋 `09` 5栋 `10` 6栋 `11`
7栋 `12` 8栋 `13` 9栋 `14`
10栋 `15` 11栋 `16` 13栋 `17`

### 德智留学生公寓 `5`

留学生公寓(电+热水) `18` 留学生公寓(冷水) `19`

### 望麓桥学生公寓 `6`

1栋 `51` 2栋北 `52` 2栋南 `53`
3栋北 `54` 3栋南 `55` 
