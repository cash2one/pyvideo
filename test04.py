import time

def run():
    text = '检查视频是否上传成功..'
    print(text, end='\r')
    flag = False
    for i in range(0, 200):
        text=text+'.'
        print(text, end='\r')
        if i == 3 :
            flag = True
            break
        time.sleep(1)
    print('')
    print('视频上传完成')
    return False

run()    


