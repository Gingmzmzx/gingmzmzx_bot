import time
import requests
import telepot
import json
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open
from telepot.namedtuple import ReplyKeyboardMarkup

flag = 1
fnm = 1

def handle(msg):
    global fnm
    global flag
    print(fnm)
    
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    
    if msg['text'] == '/start' or msg['text'] == '/help' or msg['text'] == '/help@gingmzmzx_bot':
        bot.sendMessage(chat_id, '欢迎使用本bot。\n在这里，你可以寻求在线客服的帮助，也可以给我留言，还有更多功能有待开发。\n欢迎关注我的频道： https://t.me/gingmzmzx_bot_notice')
    elif msg['text'] == '/sbr':
        if fnm == 1:
            bot.sendMessage(chat_id, '请输入要留言的内容：')
            fnm = 2
            #print(fnm)
    elif fnm == 2:
        print(fnm)
        order = msg['text']
        bot.sendMessage(chat_id, '收到，正在提交......')
        url = 'http://tgbot.xzy.center/insertOrUpdate'
        if requests.post(url, data={'question': order, 'answer': '还没有回复'}).content:
            bot.sendMessage(chat_id, '留言成功！')
        fnm = 1
        
    elif msg['text'] == '/getcount':
        bot.sendMessage(chat_id, '正在查询，请稍后......')
        # 以下为GET请求
        url = 'http://tgbot.xzy.center/tableCount'
        content = requests.get(url).content
        bot.sendMessage(chat_id, '问答总条数为：'+str(content))
        
    elif msg['text'] == '/tikucount' or msg['text'] == '/tikucount@gingmzmzx_bot':
        bot.sendMessage(chat_id, '正在查询，请稍后......')
        # 以下为GET请求
        url = 'https://tiku.xzy.center/tableCount'
        content = requests.get(url).content
        bot.sendMessage(chat_id, '题库题目总条数为：'+str(content))
        
    elif msg['text'] == '/sba':
        if flag == 1:
            bot.sendMessage(chat_id, '请输入要问的内容：')
            flag = 2
            #print(fnm)
    elif flag == 2:
        print(fnm)
        order = msg['text']
        bot.sendMessage(chat_id, '正在获取答案......')
        url = 'http://tgbot.xzy.center/getAnswerByQuestion'
        answer = requests.post(url, data={'question': order}).content
        
        bot.sendMessage(chat_id, answer)
        
        flag = 1
        
    else:
        bot.sendMessage(chat_id, '功能正在开发，请等待。awa')

TOKEN = '2078185217:AAFQ3isACEsbaTjEg_F_3SSqRpOGfSekWEc'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)
