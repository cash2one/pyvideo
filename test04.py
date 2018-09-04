import time
text= '检查视频是否上传成功..'

print(text, end='\r')
for i in range(0, 10):
    text=text+'.'
    print(text, end='\r')
    if i == 9:
        print('')
    time.sleep(1)


