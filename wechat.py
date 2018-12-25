import itchat
from itchat.content import *


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print('text   %s' % msg)
    # itchat.send('hello', msg['FromUserName'])

    msg.user.send(u'@\u2005I received: %s' % (msg.text))

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    print('bbbb:   %s' % msg)
    msg.download(msg.fileName)
    itchat.send('@%s@%s' % (
        'img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),
        msg['ToUserName'])
    return '%s received' % msg['Type']

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('Nice to meet you!')

itchat.auto_login(hotReload=True, enableCmdQR=2)



itchat.run()