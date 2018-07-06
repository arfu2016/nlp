## 服务器返回协议

总体结构：
```
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 1025,
        "data": data,
        "seq": "dd8fa466-4dd1-11e8-b4ed-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```



###1. 比赛id错误协议。当连接比赛使用的比赛id错误或不在ai球支持范围内时，返回该条错误

1.1 数据结构
```
/**
 * code = 1025(MatchIdError)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 1025,
        "data": {
            "msg": "比赛id错误"
        },
        "seq": "dd8fa466-4dd1-11e8-b4ed-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
1.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>消息内容</td></tr>
</table>


###2. 参数错误协议。当客户端发送的websocket协议参数错误时，返回该条消息

2.1 数据结构
```
/**
 * code = 1027(ParameterError)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 1027,
        "data": {
            "msg": "参数错误"
        },
        "seq": "dd9040c2-4dd1-11e8-af53-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
2.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>消息内容</td></tr>
</table>


###3. 事件绑定协议。当用户询问绑已定事件时（如第一个进球）时，服务器返回该条协。

3.1 数据结构
```
/**
 * code = 2000(EventBind)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2000,
        "data": {
            "event_type": 30,
            "num": 0,
            "team_id": 0
        },
        "seq": "dd9040c3-4dd1-11e8-8f0d-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
3.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->event_type</td><td>string</td><td>绑定的事件类型：30进球，40黄牌，50红牌，45两黄变红</td></tr>
<tr><td>result->data->num</td><td>int</td><td>第几个事件</td></tr>
<tr><td>result->data->team_id</td><td>int</td><td>所属球队id，0代表未指定主客队</td></tr>
</table>


###4. 直播事件协议。比赛进行中，球场发生事件时，服务器端会主动发送该条协议给客户端。

4.1 数据结构
```
/**
 * code = 2048(Event)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2048,
        "data": {
            "away_name": "xxx",
            "event_id": "111111",
            "feedtype": "delta",
            "home_name": "aaaa",
            "match_period": "1H",
            "minute": "15",
            "msg": "鲁尼的进球",
            "origin_type": "0",
            "score": {"t1":"0", "t2": "1"},
            "second": "0",
            "source": 2,
            "ssid": "",
            "team": "0",
            "type": "30"
        },
        "seq": "dd90544c-4dd1-11e8-af9f-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
4.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->away_name</td><td>string</td><td>客队名称</td></tr>
<tr><td>result->data->event_id</td><td>string</td><td>事件id，事件的唯一标识符，id相同的事件为同一事件</td></tr>
<tr><td>result->data->feedtype</td><td>string</td><td>事件消息类型：delta为普通消息，deltaupdate为事件更新消息</td></tr>
<tr><td>result->data->home_name</td><td>string</td><td>主队名称</td></tr>
<tr><td>result->data->match_period</td><td>string</td><td>比赛阶段：1H上半场，HT中场，2H下半场</td></tr>
<tr><td>result->data->minute</td><td>string</td><td>事件发生的时间：分钟数</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>事件消息内容</td></tr>
<tr><td>result->data->origin_type</td><td>string</td><td>事件原如类弄型（type==-1）时需要使用origin_type判断事件类型</td></tr>
<tr><td>result->data->score->t1</td><td>string</td><td>事件发生时主队比分</td></tr>
<tr><td>result->data->score->t2</td><td>string</td><td>事件发生时客队比分</td></tr>
<tr><td>result->data->second</td><td>string</td><td>事件发生的时间：秒数</td></tr>
<tr><td>result->data->source</td><td>int</td><td>事件数据来源：2br，1GSM</td></tr>
<tr><td>result->data->ssid</td><td>string</td><td>事件发生比赛id（GSM）</td></tr>
<tr><td>result->data->team</td><td>string</td><td>事件归属方球队id（GSM）</td></tr>
<tr><td>result->data->type</td><td>string</td><td>事件类型</td></tr>
</table>


###5. 普通文本协议。当用户询问问题，回复为纯文本时，返回该条协议

5.1 数据结构
```
/**
 * code = 2049(Text)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2049,
        "data": {
            "msg": "普通文本协议"
        },
        "seq": "dd90544d-4dd1-11e8-9673-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
5.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>事件消息内容</td></tr>
</table>


###6. 图片协议。当服务器回复图片/或后台主动推送图片时，发送该条协议

6.1 数据结构
```
/**
 * code = 2050(Picture)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2050,
        "data": {
            "link": [{
                "img": "http://static.aiball.ai/303.gif",
                "compress_img": "http://static.aiball.ai/f9303.g"
            }],
            "type": 1
        },
        "seq": "dd90544e-4dd1-11e8-a464-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
6.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->link[0]->img</td><td>string</td><td>原图</td></tr>
<tr><td>result->data->link[0]->compress_img</td><td>string</td><td>缩略图</td></tr>
<tr><td>result->data->type</td><td>int</td><td>type:1静图，2动图，3多图，多图时有count</td></tr>
<tr><td>result->data->count</td><td>int</td><td>多图数量</td></tr>
</table>


###7. 表格协议。当服务器返回表格数据（如赛程时）会使用该条协议。即将废弃，使用2060协议

7.1 数据结构
```
/**
 * code = 2051(Table)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2051,
        "data": [
            ["排名", "球队", "场次", "积分"],
            [1, "拜仁慕尼黑", 31, 78],
            [2, "沙尔克04", 31, 56],
            [3, "多特蒙德", 31, 54],
            [4, "勒沃库森", 31, 51],
            [5, "霍芬海姆", 31, 49],
            [6, "莱比锡RB", 31, 47],
            [7, "法兰克福", 31, 46],
            [8, "门兴格拉德巴赫", 31, 43],
            [9, "柏林赫塔", 31, 42],
            [10, "斯图加特", 31, 42],
            [11, "奥格斯堡", 31, 40],
            [12, "不莱梅", 31, 37],
            [13, "汉诺威96", 31, 36],
            [14, "沃尔夫斯堡", 31, 30],
            [15, "美因茨", 31, 30],
            [16, "弗赖堡", 31, 30],
            [17, "汉堡", 31, 25],
            [18, "科隆", 31, 22]
        ],
        "seq": "dd9067d8-4dd1-11e8-b4fb-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
7.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data</td><td>list</td><td>内容列表（目前2051协议仅赛程用到）。列表内元素可放置任意数据</td></tr>
</table>


###8. 图标协议。当服务器发送内容为图表数据（如统计数据时使用）

8.1 数据结构
```
/**
 * code = 2052(Chart)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2052,
        "data": [{
            "away_team_name": "塞维利亚",
            "home": "51%",
            "away": "49%",
            "home_rate": 0.51,
            "sort": 1,
            "item": "控球率",
            "home_team_name": "莱万特",
            "away_rate": 0.49
        }],
        "seq": "dd9067d9-4dd1-11e8-b6c9-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
8.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data[0]->away_team_name</td><td>string</td><td>客队名称</td></tr>
<tr><td>result->data[0]->home_team_name</td><td>string</td><td>主队名称</td></tr>
<tr><td>result->data[0]->away</td><td>string</td><td>客队该统计项值</td></tr>
<tr><td>result->data[0]->home</td><td>string</td><td>主队该统计项值</td></tr>
<tr><td>result->data[0]->sort</td><td>int</td><td>该统计项在总项中排序（由服务器端控制统计数据排序时）</td></tr>
<tr><td>result->data[0]->item</td><td>string</td><td>该统计项名称</td></tr>
<tr><td>result->data[0]->away_rate</td><td>float</td><td>该统计项客队百分比</td></tr>
<tr><td>result->data[0]->home_rate</td><td>float</td><td>该统计项主队百分比</td></tr>
</table>


###9. 交互协议。已作废

```
/**
 * code = 2053(Interaction)
 */
{} //not support currently
```


###10. 单条新闻协议。用于单条新闻以及基于单条新闻上的其他内容（如活动中将名单查询等）

10.1 数据结构
```
/**
 * code = 2054(News)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2054,
        "data": {
            "msg": "大家喜爱的“克韩评球”栏目迎来第200期啦~为了感谢大家这一个赛季以来对AI球和克韩老师的厚爱，小美将在微博@爱球机器人和AI球App内抽出2件正品球衣哦~",
            "title": "【克韩评球，好礼成双】中奖名单公布页",
            "pics": ["http://static.aiball.ai/upload/b80594790d8ad3efd75d14e4d81a50542e3a1edb.jpg?x-oss-process=image/watermark,image_cm9ib3QvaWNvbi9XYXRlcm1hcmstTG9nby03NTAucG5n,g_sw"],
            "pic": "http://static.aiball.ai/upload/b80594790d8ad3efd75d14e4d81a50542e3a1edb.jpg?x-oss-process=image/watermark,image_cm9ib3QvaWNvbi9XYXRlcm1hcmstTG9nby03NTAucG5n,g_sw",
            "link": "http://h5.aiball.ai/#/detail/3468"
        },
        "seq": "dd9067db-4dd1-11e8-a6ff-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
10.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>消息内容</td></tr>
<tr><td>result->data->title</td><td>string</td><td>新闻标题</td></tr>
<tr><td>result->data->link</td><td>string</td><td>新闻详情页地址</td></tr>
<tr><td>result->data->pic</td><td>string</td><td>新闻图片地址（单图，兼容老版本使用）</td></tr>
<tr><td>result->data->pics</td><td>list</td><td>新闻图片地址（多图，每个元互为一个图片地址）</td></tr>
</table>


###11. 多条新闻协议。服务器端发送普通新闻时，会使用当前协议

11.1 数据结构
```
/**
 * code = 2055(NewsList)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2055,
        "data": {
            "msg": "以下是小美为你找到的克韩评球相关专栏内容：",
            "news": [{
                "title": "【克韩的足球冷知识】红色荣耀第40期：球场急需资金，收购不通，所以曼联只能上市",
                "link": "http://h5.aiball.ai/#/detail/3570",
                "rank": 0,
                "pic": "http://static.aiball.ai/upload/efce60a232b16d1f0d7340dfc566845a34edffde.jpg?x-oss-process=image/watermark,image_cm9ib3QvaWNvbi9XYXRlcm1hcmstTG9nby03NTAucG5n,g_sw",
                "news_id": 3570,
                "is_big_pic": 1
            }],
            "url": "http://h5.aiball.ai/#/newsList/index?tag=åé©è¯ç"
        },
        "seq": "dd9067dc-4dd1-11e8-bb1c-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
11.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>消息内容</td></tr>
<tr><td>result->data->url</td><td>string</td><td>新闻列表页地址</td></tr>
<tr><td>result->data->news[0]->title</td><td>string</td><td>单条新闻标题</td></tr>
<tr><td>result->data->news[0]->link</td><td>string</td><td>单条新闻详情页地址</td></tr>
<tr><td>result->data->news[0]->pic</td><td>string</td><td>单条新闻图片地址</td></tr>
<tr><td>result->data->news[0]->news_id</td><td>int</td><td>单条新闻id</td></tr>
<tr><td>result->data->news[0]->is_big_pic</td><td>int</td><td>图片是否首页大图，1是，0否（首页大图在新闻顶部显示，每个新闻列表中只有一个图片为首页大图）</td></tr>
<tr><td>result->data->news[0]->rank</td><td>int</td><td>新闻排序</td></tr>
</table>


###12. 赛程协议。服务器发送比赛赛程时，使用该条协议

12.1 数据结构
```
/**
 * code = 2056(Fixture)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2056,
        "data": [{
            "gsm_league_id": 8,
            "bg": "",
            "match_time": "2018-05-05 03:00:00",
            "home_name": "布莱顿",
            "away_team_id": 662,
            "away_name": "曼联",
            "status": 1,
            "gsm_match_id": 2463156,
            "home_team_id": 703,
            "league_name": "英超",
            "operation": 0,
            "fav": 0
        }],
        "msg": "",
        "seq": "dd90c998-4dd1-11e8-a9be-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
12.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data[0]->gsm_league_id</td><td>int</td><td>赛程中当前比赛归属联赛id</td></tr>
<tr><td>result->data[0]->bg</td><td>string</td><td>赛程中当前比赛背景图片地址</td></tr>
<tr><td>result->data[0]->match_time</td><td>string</td><td>比赛时间（ISO格式）</td></tr>
<tr><td>result->data[0]->home_name</td><td>string</td><td>主队名称</td></tr>
<tr><td>result->data[0]->away_team_id</td><td>int</td><td>客队球队id</td></tr>
<tr><td>result->data[0]->away_name</td><td>string</td><td>客队名称</td></tr>
<tr><td>result->data[0]-->status</td><td>int</td><td>比赛状态：1未开赛，2已完场，3进行中</td></tr>
<tr><td>result->data[0]-->gsm_match_id</td><td>int</td><td>比赛id</td></tr>
<tr><td>result->data[0]-->home_team_id</td><td>int</td><td>主队球队id</td></tr>
<tr><td>result->data[0]-->league_name</td><td>string</td><td>联赛名称</td></tr>
<tr><td>result->data[0]-->operation</td><td>int</td><td>是否运营比赛标志：1是，0否</td></tr>
<tr><td>result->data[0]-->fav</td><td>int</td><td>是否用户关注的比赛标志：1是，0否</td></tr>
</table>


###13. 阵容阵型协议。当服务器发送首发阵容信息时，使用当前协议

13.1 数据结构
```
/**
 * code = 2057(Formation)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2057,
        "data": {
            "away_formation": ["3", "6", "1"],
            "away_name": "拉齐奥",
            "away_team_id": 1245,
            "coach_team_a": "西蒙尼·因扎吉",
            "coach_team_h": "马扎里",
            "home_formation": ["3", "6", "1"],
            "home_name": "都灵",
            "home_team_id": 1268,
            "lineups_bench": [{
                "shirtnumber": "25",
                "person": "瓦尔吉奇",
                "replaced": 0,
                "person_id": "36716",
                "team_id": "1245"
            }],
            "player": {
                "home": [{
                    "position_y": "C",
                    "person": "西>里古",
                    "position_x": "GK",
                    "replaced": 0,
                    "shirtnumber": "39",
                    "person_id": "58378",
                    "team_id": "1268"
                }],
                "away": [{
                    "position_y": "CR",
                    "person": "路易斯·费利佩",
                    "position_x": "D1",
                    "replaced": 0,
                    "shirtnumber": "27",
                    "person_id": "405559",
                    "team_id": "1245"
                }]
            },
            "substitutions": {
                "home": [{
                    "xia_shirtnumber": "20",
                    "shang_person": "雅戈·法尔克",
                    "shang_shirtnumber": "14",
                    "xia_person": "S. Edera",
                    "minute": 62
                }]
            },
            "type": 1
        },
        "seq": "dd90c999-4dd1-11e8-8f39-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
13.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->away_formation</td><td>list[string]</td><td>客队阵型，["3", "6", "1"]表示客队使用3-6-1阵型</td></tr>
<tr><td>result->data->away_name</td><td>string</td><td>客队名称</td></tr>
<tr><td>result->data->away_team_id</td><td>int</td><td>客队id</td></tr>
<tr><td>result->data->coach_team_a</td><td>string</td><td>客队教练</td></tr>
<tr><td>result->data->coach_team_h</td><td>string</td><td>主队教练</td></tr>
<tr><td>result->data->type</td><td>int</td><td>显示类弄：1只显示主队阵容，2只显示客队阵容，3显示主客队阵容</td></tr>
<tr><td>result->data->home_formation</td><td>list[string]</td><td>主队阵型，["4", "3", "3"]表示客队使用4-3-3阵型</td></tr>
<tr><td>result->data->lineups</td><td></td><td>阵容信息</td></tr>
<tr><td>result->data->lineups_bench[0]->shirtnumber</td><td>string</td><td>阵容信息，当前球员：球衣号码</td></tr>
<tr><td>result->data->lineups_bench[0]->person</td><td>string</td><td>阵容信息，当前球员：名字</td></tr>
<tr><td>result->data->lineups_bench[0]->replaced</td><td>int</td><td>阵容信息，当前球员：是否被换下</td></tr>
<tr><td>result->data->lineups_bench[0]->person_id</td><td>string</td><td>阵容信息，当前球员：球员id</td></tr>
<tr><td>result->data->lineups_bench[0]->team_id</td><td>string</td><td>阵容信息，当前球员：所属球队id</td></tr>
<tr><td>result->data->player</td><td></td><td>球员阵型</td></tr>
<tr><td>result->data->player->home[0]->position_y</td><td>string</td><td>主队当前球员位置（Y轴）代码</td></tr>
<tr><td>result->data->player->home[0]->person</td><td>string</td><td>主队当前球员名字</td></tr>
<tr><td>result->data->player->home[0]->position_x</td><td>string</td><td>主队当前球员位置（X轴）代码</td></tr>
<tr><td>result->data->player->home[0]->replaced</td><td>int</td><td>主队当前球员是否被换下：1被换下，0未被换下</td></tr>
<tr><td>result->data->player->home[0]->shirtnumber</td><td>string</td><td>主队当前球员球衣号</td></tr>
<tr><td>result->data->player->home[0]->person_id</td><td>string</td><td>主队当前球员id</td></tr>
<tr><td>result->data->player->home[0]->team_id</td><td>string</td><td>主队当前球员所属球队id（即主队id）</td></tr>
<tr><td>result->data->substitutions</td><td></td><td>换人信息</td></tr>
<tr><td>result->data->substitutions->home[0]->xia_shirtnumber</td><td>string</td><td>主队第一个换人事件：被换下球员球衣号</td></tr>
<tr><td>result->data->substitutions->home[0]->shang_shirtnumber</td><td>string</td><td>主队第一个换人事件：换上球员球衣号</td></tr>
<tr><td>result->data->substitutions->home[0]->xia_person</td><td>string</td><td>主队第一个换人事件：被换下球员球</td></tr>
<tr><td>result->data->substitutions->home[0]->shang_person</td><td>string</td><td>主队第一个换人事件：换上球员</td></tr>
<tr><td>result->data->substitutions->home[0]->minute</td><td>int</td><td>主队第一个换人事件：换人时间</td></tr>
</table>


###14. 可扩展表格协议。支持动态扩展列数。版本号1.38及以下不支持该条协议

14.1 数据结构
```
/**
 * code = 2060(TableEx)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2060,
        "data": {
            "msg": "2060协议，表格列数不固定，最多有5个",
            "title": ["排名", "球队", "场次", "积分"],
            "value": [
                [1, "曼城", 29, 78],
                [2, "曼联", 29, 62],
                [3, "利物浦", 29, 60],
                [4, "托特纳姆热刺", 29, 58],
                [5, "切尔西", 29, 53]
            ],
            "type": 1
        },
        "seq": "d292fb72-4ea2-11e8-abd9-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
14.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>表格协议消息</td></tr>
<tr><td>result->data->title</td><td>list</td><td>表格title列表</td></tr>
<tr><td>result->data->type</td><td>int</td><td>指定表格类型，用于前端套用不同的样式</td></tr>
<tr><td>result->data->value</td><td>list</td><td>表格内容（表格内容已排序）</td></tr>
</table>


###15. 视频协议。当服务器端发送视频信息时使用

15.1 数据结构
```
/**
 * code = 2170(Video)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2170,
        "data": {
            "count": 0,
            "link": [{"compress_img": "", "img": ""}],
            "media": "",
            "media_all": [{
                "FileSize": "5143604",
                "url": "http://Act-ss-mp4-ld/3d911c3e01f734158fc720c2c7f18a35.mp4",
                "info": "640x360",
                "desc": "标清"
            }],
            "media_title": "",
            "title": "",
            "type": 1
        },
        "seq": "d2930efe-4ea2-11e8-8914-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
15.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->count</td><td>int</td><td>视频数量</td></tr>
<tr><td>result->data->link[0]->img</td><td>string</td><td>预览图地址（视频预览图列表中仅第一条有效）</td></tr>
<tr><td>result->data->link[0]->compress_img</td><td>string</td><td>预览图缩略图地址（视频预览图列表中仅第一条有效）</td></tr>
<tr><td>result->data->media</td><td>string</td><td>多媒体地址。当media_all不为空时，默认使用media_all第一条，仅当media_all为空时，使用media</td></tr>
<tr><td>result->data->media_title</td><td>string</td><td>多媒体标题</td></tr>
<tr><td>result->data->title</td><td>string</td><td>标题</td></tr>
<tr><td>result->data->type</td><td>int</td><td>媒体类型，视频协议永远为1</td></tr>
<tr><td>result->data->media_all</td><td>list</td><td></td></tr>
<tr><td>result->data->media_all[0]->FileSize</td><td>string</td><td>当前分辨率下视频文件大小</td></tr>
<tr><td>result->data->media_all[0]->url</td><td>string</td><td>当前分辨率地址</td></tr>
<tr><td>result->data->media_all[0]->info</td><td>string</td><td>当前分辨率视频分辨率</td></tr>
<tr><td>result->data->media_all[0]->desc</td><td>string</td><td>当前分辨率描述</td></tr>
</table>


###16. 音频协议。当服务器端发送音频信息时使用

16.1 数据结构
```
/**
 * code = 2180(Audio)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2180,
        "data": {
            "media": "",
            "media_title": "",
            "title": ""
        },
        "seq": "d2930eff-4ea2-11e8-b9fb-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
16.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->media</td><td>string</td><td>多媒体地址</td></tr>
<tr><td>result->data->media_title</td><td>string</td><td>多媒体标题</td></tr>
<tr><td>result->data->title</td><td>string</td><td>标题</td></tr>
</table>


###17. 连接的比赛已结束（超出支持时间范围）时返回该协议。已作废

17.1 数据结构
```
/**
 * code = 2177(MatchEnd)
 */
{} //not support currently
```


###18. 连接的比赛还未开始（超出支持时间范围）时返回该协议。已作废
```
/**
 * code = 2178(MatchNotStart)
 */
{} //not support currently
```


###19. 图文协议。当服务器发送包含图片以及文字内容的消息时使用

19.1 数据结构
```
/**
 * code = 2190(PictureText)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2190,
        "data": {
            "link": [{"compress_img": "", "img": ""}],
            "title": "",
            "url": ""
        },
        "seq": "d2930f02-4ea2-11e8-81cd-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
19.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->link[0]->compress_img</td><td>string</td><td>图片缩略图地址</td></tr>
<tr><td>result->data->link[0]->img</td><td>string</td><td>图片地址</td></tr>
<tr><td>result->data->url</td><td>string</td><td>跳转地址</td></tr>
<tr><td>result->data->title</td><td>string</td><td>图文协议内容</td></tr>
</table>


###20. 帮助协议。

20.1 数据结构
```
/**
 * code = 4096(Help)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 4096,
        "data": {
            "msg": "主人您好！我是您的英超私人助理小美！点击技能包，可以更深入的了解小美哦。",
            "link": "http: //app.aiball.ai/help"
        },
        "seq": "dd90dd27-4dd1-11e8-b57d-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
20.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->link</td><td>string</td><td>帮助页面连接</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>消息信息</td></tr>
</table>


###21. 追问协议。当用户问题主体发生重名，服务器追问时，发送该协议。无屏平台不支持该协议

21.1 数据结构
```
/**
 * code = 4097(AskBack)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 4097,
        "data": {
            "msg": "找到3个带有“科斯塔”的名字，点击选择你想询问的对象：",
            "values": [{
                    "type": "人员",
                    "line": 1,
                    "title": ["名字", "信置", "号码", "俱乐部"],
                    "items": [{
                        "idx": 1,
                        "name": "D.科斯塔",
                        "pos": "前锋",
                        "number": 0,
                        "club": "曼城"
                    }]
                },
                {
                    "type": "球队",
                    "line": 1,
                    "title": ["俱乐部名称", "所属联赛", "成立时间"],
                    "items": [{
                        "idx": 1,
                        "name": "xxxx科斯塔",
                        "league": "英超",
                        "time": "1957年"
                    }]
                },
                {
                    "type": "球场",
                    "line": 1,
                    "title": ["球场名称", "所属俱乐部", "启用时间"],
                    "items": [{
                        "idx": 1,
                        "name": "球场名称",
                        "club": "曼联",
                        "time": "1978年"
                    }]
                }
            ]
        },
        "seq": "dd90dd28-4dd1-11e8-8f31-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
21.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->msg</td><td>string</td><td>消息信息</td></tr>
<tr><td>result->data->values[0].type</td><td>string</td><td>重名实体后选项类型：“人员”，“球队”，“球场”（球员，教练，裁判都归属人员）</td></tr>
<tr><td>result->data->values[0].line</td><td>string</td><td>重名实体后选项当前类型：后选条目数量</td></tr>
<tr><td>result->data->values[0].title</td><td>list[string]</td><td>重名实体后选项当前类型：表格title</td></tr>
<tr><td>result->data->values[0].items[0].idx</td><td>int</td><td>重名实体后选项当前类型，当前后选项：排序号。从1开始，每种类型下独立排序</td></tr>
<tr><td>result->data->values[0].items[0].name</td><td>string</td><td>重名实体后选项当前类型，当前后选项：全名</td></tr>
<tr><td>result->data->values[0].items[0].pos</td><td>string</td><td>重名实体后选项当前类型，当前后选项：球员位置。仅为球员时有效</td></tr>
<tr><td>result->data->values[0].items[0].number</td><td>int</td><td>重名实体后选项当前类型，当前后选项：球衣号码。仅为球员时有效</td></tr>
<tr><td>result->data->values[0].items[0].club</td><td>string</td><td>重名实体后选项当前类型，当前后选项：所属俱乐部。球员、球场时有效</td></tr>
<tr><td>result->data->values[0].items[0].league</td><td>string</td><td>重名实体后选项当前类型，当前后选项：所属联赛。仅为球队时有效</td></tr>
<tr><td>result->data->values[0].items[0].time</td><td>string</td><td>重名实体后选项当前类型，当前后选项：成立时间。球队、球场时有效</td></tr>
</table>


###22. 新闻摘要协议。相对于多条新闻协议，只有新闻摘要信息。只为无屏平台发送

22.1 数据结构
```
/**
 * code = 4098(NewsAbstract)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 4098,
        "data": {
            "news_id": 11,
            "abstract": "xxxxxx"
        },
        "seq": "dd90dd29-4dd1-11e8-823b-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
22.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->news_id</td><td>int</td><td>新闻id</td></tr>
<tr><td>result->data->abstract</td><td>string</td><td>摘要内容</td></tr>
</table>


###23. 互动新闻协议。内容在inner_content中。inner_content包含其他协议

23.1 数据结构
```
/**
 * code = 4099(AINews)
 */
{
    "answered": 1,
    "method": 1000,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 4099,
        "data": {
            "buttons": [{
                "button_id": 27596,
                "word_id": null,
                "button_content": "换一篇",
                "button_order": 0,
                "button_type": 1,
                "word_content": null,
                "jump_order": null,
                "button_pic": "http://static.aiball.ai/robot/icon/new/1080/Continue_icon.png"
            }],
            "news": {
                "content_pool_id": 3453,
                "inner_content": {},
                "news_id": 10060,
                "order": 1
            }
        },
        "seq": "dd90dd2a-4dd1-11e8-858e-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
23.2 字段说明
<table>
<tr bgcolor="#00AAEE"><td>参数名</td><td>类型</td><td>说明</td></tr>
<tr><td>result->data->buttons[0].button_id</td><td>int</td><td>当前互动新闻“段”中，当前按钮：ID</td></tr>
<tr><td>result->data->buttons[0].word_id</td><td>int</td><td>当前互动新闻“段”中，当前按钮：对就的词条id，button_type==3时有效</td></tr>
<tr><td>result->data->buttons[0].button_content</td><td>string</td><td>当前互动新闻“段”中，当前按钮：按钮标题</td></tr>
<tr><td>result->data->buttons[0].button_order</td><td>int</td><td>当前互动新闻“段”中，当前按钮：按钮显示位置顺序</td></tr>
<tr><td>result->data->buttons[0].button_type</td><td>int</td><td>当前互动新闻“段”中，当前按钮：按钮类型：0 继续， 1 换篇 ， 2 全部 ，3 词条，4 自定义， 5 弹幕 ，6 跳转</td></tr>
<tr><td>result->data->buttons[0].word_content</td><td>string</td><td>当前互动新闻“段”中，当前按钮：自定议内容，button_type==4时有效</td></tr>
<tr><td>result->data->buttons[0].jump_order</td><td>int</td><td>当前互动新闻“段”中，当前按钮：跳转目标“段”id，button_type==6时有效</td></tr>
<tr><td>result->data->buttons[0].button_pic</td><td>string</td><td>当前互动新闻“段”中，当前按钮：按钮图片地址</td></tr>
<tr><td>result->data->news->content_pool_id</td><td>int</td><td>当前互动新闻“段”：新闻内容id</td></tr>
<tr><td>result->data->news->news_id</td><td>int</td><td>当前互动新闻“段”：新闻id</td></tr>
<tr><td>result->data->news->order</td><td>int</td><td>当前互动新闻“段”：段id</td></tr>
<tr><td>result->data->news->inner_content</td><td>map</td><td>当前“段”所对应的子协议类型，可以是协议：2049，2050，2170，2180，2190</td></tr>
</table>


###24. 可扩展表格协议。支持动态扩展列数。版本号1.38及以下不支持该条协议

24.1 数据结构
```
/**
 * code = 2061(TableEx)
 */
{
    "answered": 1,
    "method": 1001,
    "power": 2,
    "result": {
        "answered": 1,
        "code": 2061,
        "data": {
            "msg": "2061协议，表格列数不固定，最多有5个，支持点击",
            "title": ["排名", "球队", "场次", "积分"],
            "values": [
                {
                    "value": [1, "曼城", 29, 78],
                    "entity": "曼城",  // 没有url时，发送273协议，msg取entity
                    "entity_id": 0  // 没有url时，发送273协议，entity_id取entity
                    "url": "xxx"  //有url时，跳转至url对应地址
                },
                {
                    "value": [2, "曼联", 29, 62],
                    "entity": "曼联",
                    "entity_id": 1
                    "url": "xxx"
                }
            ],
            "type": 1
        },
        "seq": "d292fb72-4ea2-11e8-abd9-e7c9954edd99",
        "ssid": "0",
        "sub_code": 0
    },
    "status": 1
}
```
24.2 字段说明
