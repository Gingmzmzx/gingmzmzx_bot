import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json
import telegram

token_my = "2078185217:AAHCa03JgL-1argZgffjTW0sVA1DxPgRvOY"

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

fnm = 1
flag = 1
notice = '欢迎使用本bot。\n在这里，你可以寻求在线客服的帮助，也可以给我留言，还有更多功能有待开发。\n欢迎关注我的频道： https://t.me/gingmzmzx_bot_notice'

# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )
    update.message.reply_text(notice)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(notice)

    
def sbr(update: Update, context: CallbackContext) -> None:
    global fnm
    update.message.reply_text('请输入要留言的内容：')
    fnm = 2


def sba(update: Update, context: CallbackContext) -> None:
    global flag
    update.message.reply_text('请输入要查询的关键词：')
    flag = 2


def echo(update: Update, context: CallbackContext) -> None:
    global fnm, flag
    if fnm == 2:
        fnm = 1
        print(fnm)
        order = update.message.text
        update.message.reply_text('收到，正在提交......')
        url = 'http://tgbot.xzy.center/insertOrUpdate'
        if requests.post(url, data={'question': order, 'answer': '还没有回复'}).content:
            update.message.reply_text('留言成功~！')
        
    elif flag == 2:
        flag = 1
        print(flag)
        question = update.message.text
        print(question)
        update.message.reply_text('正在获取答案......')
        answer = requests.post('http://tgbot.xzy.center/getAnswerByQuestion', data={'question': question}).content
        print(answer)
        update.message.reply_text(answer)
        
    else:
        f = open("notice.txt","r",encoding="utf-8")
        data  = f.read()
        if str(data) != '':
            update.message.reply_text(str(data))
        f.close()


def tikucount(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('查询中，请稍后。。。')
    # 以下为GET请求
    url = 'https://tiku.xzy.center/tableCount'
    content = requests.get(url).content
    
    update.message.reply_text('题库题目总条数为：'+str(content))


def getcount(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('查询中，请稍后。。。')
    # 以下为GET请求
    url = 'http://tgbot.xzy.center/tableCount'
    content = requests.get(url).content
        
    update.message.reply_text('问答总条数为：'+str(content))


def aboutme(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('关于我：\r\n @gingmzmzx 是自动学习Pro（自动学习强国）原作者\r\n维护着一个很烂的纯自己写的小网站： https://xzy.center\r\n还没上高中，是个学生党\r\n有空的时候可以接一些活干\r\n欢迎与我取得联系！')
    
def set_notice(update: Update, context: CallbackContext) -> None:
    if update.message.chat_id == 1887516351:
        mt = update.message.text
        mt_list = mt.split()
        if mt_list[-1] == '/notice':
            update.message.reply_text('指令格式错误！')
        else:
            f = open("notice.txt","w",encoding="utf-8")
            if mt_list[1] == 'none':
                content = ''
            else:
                content = mt_list[1]
            f.write(content)
            f.close()
            update.message.reply_text('修改成功！')
    else:
        update.message.reply_text('没有权限，再乱发我要报告 @gingmzmzx 了！')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(token_my)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("sbr", sbr))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("tikucount", tikucount))
    dispatcher.add_handler(CommandHandler("getcount", getcount))
    dispatcher.add_handler(CommandHandler("sba", sba))
    dispatcher.add_handler(CommandHandler("aboutme", aboutme))
    dispatcher.add_handler(CommandHandler("notice", set_notice))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()