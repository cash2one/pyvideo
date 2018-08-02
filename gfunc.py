import jieba

'''
分词
'''
def participle(str):
    seg_list = jieba.cut(str)  # 默认是精确模式
    print(seg_list)
    return seg_list
