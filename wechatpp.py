#coding=utf8
import itchat
from itchat.content import *

# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
from tuling import get_response

@itchat.msg_register('Text')
def text_reply(msg):

    print(msg['Text'])
    # test 'Nice to meet you 🤝! \n' +
    # msg.user.send('Nice to meet you! \n' +get_response(msg['Text']) or u'收到：' + msg['Text'])
    return get_response(msg['Text']) or u'收到：' + msg['Text']

@itchat.msg_register(['Picture', 'Recording', 'Attachment', 'Video'])
def atta_reply(msg):
    return ({ 'Picture': u'图片', 'Recording': u'录音',
        'Attachment': u'附件', 'Video': u'视频', }.get(msg['Type']) +
        u'已接受, 稍后查看😊 🤝') # download function is: msg['Text'](msg['FileName'])


@itchat.msg_register(['Map', 'Card', 'Note', 'Sharing'])
def mm_reply(msg):
    if msg['Type'] == 'Map':
        return u'非常感谢，位置分享，稍后查看'
    elif msg['Type'] == 'Sharing':
        return u'非常感谢，分享的：' + msg['Text']
    elif msg['Type'] == 'Note':
        return u'非常感谢，分享的：' + msg['Text']
    elif msg['Type'] == 'Card':
        return u'非常感谢，分享的：' + msg['Text']['Alias']

@itchat.msg_register('Text', isGroupChat = True)
def group_reply(msg):
    if msg['isAt']:
        return u'@%s\u2005%s' % (msg['ActualNickName'],
            get_response(msg['Text']) or u'收到：' + msg['Text'])

@itchat.msg_register('Friends')
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'Hello '+ msg['RecommendInfo']['NickName'] + '\n' 
        + 'Nice to meet you', 
        msg['RecommendInfo']['UserName'])

itchat.auto_login(hotReload=True, enableCmdQR=2)


itchat.run()