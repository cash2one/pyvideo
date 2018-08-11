import jieba
import os
import sys
from config import *
import random
import json
'''
分词
'''
def participle(str):
    # 自定义分词
    jieba.load_userdict('Source/userdict.txt')

    seg_list = jieba.cut(str)  # 默认是精确模式
    res_list = []
    # todo 删除一个词的
    for seg in seg_list:
        if len(seg) > 1:
                
            # TODO 特殊处理 徐老师来巡山
            if seg.find(u'徐老师来巡山') != -1:
                res_list.append('英雄联盟')
            res_list.append(seg) 
    
    return res_list

def classFromTags(tags):
    # 动漫 3 3327083625 810359132 3056371919
    return ['', '', '']
    for item in Comic33:
        if tags.find(item) != -1:
            return ['动漫', '动漫', ''] # 3327083625
    for item in Comic81:
        if tags.find(item) != -1:
            return ['动漫', '动漫', '']  # 810359132
    for item in Comic30:
        if tags.find(item) != -1:
            return ['动漫', '动漫', ''] # 3056371919

    # 游戏 3 1194332304 2030657847 3216598385
    for item in Gamecj_cf:
        if tags.find(item) != -1:
            return ['游戏', '游戏', ''] # 1194332304

    for item in Gamelol:
        if tags.find(item) != -1:
            return ['游戏', '游戏', ''] # 2030657847

    for item in Gamewz:
        if tags.find(item) != -1:
            # 随机   
            flag = random.choice('ab')
            qq = '2030657847'
            if flag == 'a':
                qq = '2030657847'
            elif flag == 'b':
                qq = '3216598385'
            return ['游戏', '游戏', '']

    for item in Variety:
        if tags.find(item) != -1:
            return ['综艺', '栏目', ''] # 1325049637
    
    for item in Teleplay:
        if tags.find(item) != -1:
            return ['电视剧', '连续剧', '']

    for item in Movie:
        if tags.find(item) != -1:
            return ['电影', '电影剪辑', ''] # 169964440
        
    # 分类 分类 qq
    return ['', '', '']
def createDir(dir):
    # if sys.version_info.major >= 3: # if the interpreter version is 3.X, use 'input',
    #     input_func = input          # otherwise use 'raw_input'
    # else:
    #     input_func = raw_input
    if os.path.exists(dir):
        pass
    else:
        os.makedirs(dir)  # Creates a new dir for the given name

def writeJsonFile(data, name, dirname='Source'):
    # 默认写入Source
    submit = './'+dirname+'/'+name+'.json'
    try:
        with open(submit, 'w') as f:
            json.dump(data, f)
            f.close()
    except Exception as e:
        pass

def readJsonFile(name, dirname='Source'):
    json_filename = './Source/'+name+'.json'
    try:
        with open(json_filename) as f:
            pop_data = json.load(f)
            f.close()
            return pop_data  
    except Exception as e:
        return None
         



