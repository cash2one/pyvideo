import dbfunc
from config import PlatformType
import MainTencent

# try:
# except Exception as e:
#     import MainVideos


class global_data(object):
    # 上传平台
    UploaderPlatform = PlatformType.kandian.value
    # 上传者
    UploaderArray = []
    # 展示的视频
    Videos = []


# 更新上传平台 上传者
def updateUploaderPlatform(platform):
    global_data.UploaderPlatform = platform
    global_data.UploaderArray = dbfunc.getUploader(global_data.UploaderPlatform)
    # 更新其他组件 todo
    try:
        MainTencent.TencentWidget().updateUploader()

    except Exception as e:
        print(e)

# 更新上传者
def updateUploaderArray():
    global_data.UploaderArray = dbfunc.getUploader(global_data.UploaderPlatform)
