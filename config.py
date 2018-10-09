from enum import Enum

# 平台
PLATFORM = 'WIN'  # MAC WIN

if PLATFORM == 'MAC':
    DRIVERPATH = './Source/mac/chromedriver'
    VIDEODIRNAME = '/Users/huangtao/Desktop/Vidos'

elif PLATFORM == 'WIN':
    DRIVERPATH = './Source/win/chromedriver.exe'
    VIDEODIRNAME = 'C:\\Users\\Administrator\\Desktop\\Video'

    
Headers = {
    'user_agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
}

VPlusBaseUrl = 'http://v.qq.com/vplus/'

LOGINQiERHAOURL = 'https://om.qq.com/userAuth/index'

# 腾讯解析地址
BASEURLTENCENTJX = 'http://www.ht9145.com/jx/tencent.php?url='

# 视频存储位置

# 平台
class PlatformType(Enum):
    tencent = 'tencent'
    kuaishou = 'kuaishou'
    kandian = 'kandian'
    qierhao = 'qierhao' 

UploadPlatformData = [
                    {'name': '看点', 'platform': PlatformType.kandian.value},
                    {'name': '企鹅号', 'platform': PlatformType.qierhao.value},
                ]

# 登陆方式
class LoginType(Enum):
    account = 'account'
    qq = 'qq'
    email = 'email'
    other = 'other'

# 枚举 视频状态
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

# 采集类型 最新 所有
class CollectType(Enum):
    latest = 1  # 最新
    allpage = 2    # 所有页面
    alllatest = 3     # 所有账号最新


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

#[v2]
# 视频类型
class VideoType(Enum):
    comic = 1
    movie = 2
    game = 3
    tv = 4


Classly = {
    '3327083625': {'type': VideoType.comic, 'data': [
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
        '西行纪',
    ]},
    '810359132': {'type': VideoType.comic, 'data': [
        '爆笑虫子',
        '搞笑小动画', 
        '王者荣耀动漫',
        '峡谷重案组',
        '搞笑动画',
        '吃鸡大作战',
        '火线传奇',
        '非人哉',
    ]},
    '3056371919': {'type': VideoType.comic, 'data': [
        '一禅小和尚',
        '哆啦A梦',
        '猫和老鼠',
        '憨豆先生动画版'
    ]},
    '1194332304': {'type': VideoType.comic, 'data': [
        '蜡笔小新',
        '卡通盒系列',

    ]},
    '3216598385': {'type': VideoType.comic, 'data': [
        '禽兽超人',
        '兽王争锋',
    ]},

    '2030657847': {'type': VideoType.game, 'data': [
        '徐老师来巡山',
        'LOL',
        'lol',
        '英雄联盟',
        '小学生炸了',
        '王者荣耀',
        '绝地求生',
        '刺激战场',
        'CF手游',
        '穿越火线',

    ]},
    '1325049637': {'type': VideoType.tv, 'data': [
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
        '橙红年代'
    ]},
    '169964440': {'type': VideoType.movie, 'data': [
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
    ]},


}


# [创建数据库]

CreateUserSql = """create table user(
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
                platform varchar(10),
                loginType varchar(10),
                usableNum int(10),
                usedTotal int(10),
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
                platform varchar(20) 
                )"""

