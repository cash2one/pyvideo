from enum import Enum

# 平台
PLATFORM = 'WIN'  # MAC WIN

# 平台
TencentPlatform = 'tencent'
KuaishouPlatform = 'kuaishou'

KandianPlatform = 'kandian'
QierhaoPlatform = 'qierhao'

Headers = {
    'user_agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
}

VPlusBaseUrl = 'http://v.qq.com/vplus/'

# video 状态
VideoStatus = ['未发布', '今天', '待发布', '已发布']
# 枚举
class VideoStatus(Enum):
    unpublisthed = 1
    tody         = 2
    waitpublish  = 3
    published    = 4

StatusArray = [
    {'name': '未发布', 'status': VideoStatus.unpublisthed},
    {'name': '今天', 'status': VideoStatus.tody},
    {'name': '待发布', 'status': VideoStatus.waitpublish},
    {'name': '已发布', 'status': VideoStatus.published}
]


account = '2030657847'

pwdDic = {
    '1194332304': 'mima1325049637', # 绝地求生 cf 王者荣耀 lol
    '1325049637': 'henry123',   # 电视剧 综艺
    '169964440': 'mima1325049637',  # 电影
    '2030657847': 'mima1325049637',  # lol + 王者荣耀
    '3056371919': 'mima1194332304',  # 搞笑 绝地求生 动漫
    '3216598385': 'mima1325049637',  # 王者荣耀
    '3327083625': 'mima1325049637',  # 动漫
    '810359132': 'huang1325049637',  # 游戏动漫
}

# url
LoginURL = 'https://kandian.mp.qq.com/vpage/login'

PubVideoURL = 'https://kandian.mp.qq.com/page/video#video_pub'

# 动漫
Comic33 = [
    '盛世妆娘',
    '魔道祖师',
    '武庚纪',
    '秦时明月',
    '狐妖小红娘',
    '火影忍者',
    '博人传',
    '海贼王',
    '刺客伍六七',
    '天行九歌',
    '骨傲天',
    '我在皇宫当巨巨',
]

Comic81 = [
    '蜡笔小新',
    '爆笑虫子',
    '禽兽超人',
    '搞笑小动画', 
    '王者荣耀动漫',
    '峡谷重案组',
    '搞笑动画',
    '吃鸡大作战',
    '火线传奇',
    '非人哉',
]

Comic30 = [
    '一禅小和尚',
    '哆啦A梦',
    '猫和老鼠',
    '憨豆先生动画版'
]

# 游戏
Gamelol = [
    '徐老师来巡山',
    'LOL',
    'lol',
    '英雄联盟',
    '小学生炸了'
]

Gamewz = [
    '王者荣耀',
]

Gamecj = [
    '绝地求生',
    '刺激战场',
]

Gamecj_cf = [
    '绝地求生',
    '刺激战场',
    'CF手游',
    '穿越火线',
]

Games = [
    '徐老师来巡山',
    'LOL',
    'lol',
    '英雄联盟',
    '王者荣耀',
    '绝地求生',
    '刺激战场',
    'CF手游',
    '穿越火线',
]

# Variety 综艺
Variety = [
    '中餐厅',
    '明日之子'
]

# teleplay 电视剧
Teleplay = [
    '扶摇',
    '甜蜜暴击',
    '流星花园',
    '香蜜沉沉烬如霜',
    '香蜜沉沉',
    '延禧攻略',
    '楚乔传',
    '情深深雨濛濛',
    '爱情公寓',
    '还珠格格',
]

# 电影
Movie = [
    '唐人街探案',
    '唐伯虎点秋香',
    '周星驰',
    '成龙',
    '刘德华',
    '周润发',
    '赌侠',
    '赌圣',
    '林正英',
    '让子弹飞',
    '大话西游',
    '人在囧途'
]


# [创建数据库]

CreateUserSql = """CREATE TABLE user(
        userId int auto_increment primary key,
        name varchar(100),
        pwd varchar(100),
        md5pwd varchar(100),
        pic varchar(100)
        )"""

CreateUploaderSql = """CREATE TABLE uploader(
                id int auto_increment primary key,
                account varchar(50),
                pwd varchar(50),
                fromUserId int(10),
                platform varchar(10)，
                ext varchar(255)
                )"""

CreateAnchorSql = """CREATE TABLE anchor (
        aid int auto_increment primary key, 
        name varchar(100), 
        uin varchar(100),
        intr varchar(255),
        vnum int(10) default 0,
        page int(10) default 1,

        fromUserId varchar(10),
        platform varchar(20)
        )"""

CreateVideosSql = """CREATE TABLE videos (
                id int auto_increment primary key,
                qq varchar(20),
                title varchar(255), 
                url varchar(255), 
                alias varchar(255), 
                tags varchar(255), 
                first_class varchar(10),
                second_class varchar(10),
                platform_create_time varchar(50), 
                create_time DATETIME, 
                publish_time DATETIME, 
                aid varchar(100),
                vid varchar(50),
                pic varchar(255),
                is_exist_local int(1), 
                local_path varchar(255), 
                fromUserId int(10),
                platform varchar(20) )
                """

