import gspread
import threading
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Filters

spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1WG-3T6qynsVvBjtEZ20SiqCe-gjIZvim9TSw_Z6Iv5k/edit#gid=0'
spreadsheet_url2 = 'https://docs.google.com/spreadsheets/d/1p8n1Jlvfpyp_6cUBfEsK6MMl6Pv1xJJwz9ZECUlkHBA/edit#gid=0'
worksheet_name = 'Master File'

gc = gspread.service_account(filename='D:\partners\par.json')
sh = gc.open_by_url(spreadsheet_url)
sh2 = gc.open_by_url(spreadsheet_url2)
worksheet = sh.worksheet(worksheet_name)
worksheet2 = sh2.sheet1 

telegram_token = '5693743508:AAH6qlkX_Eag7Oy0ae56R8cDQYNGG9jp8Vw'
updater = Updater(token=telegram_token, use_context=True)
dispatcher = updater.dispatcher


def search_value(update, context):
    search_query = update.message.text.strip()
    found = False
    
    # إرسال رسالة الانتظار
    context.bot.send_message(chat_id=update.message.chat_id, text="جاري البحث، يرجى الانتظار...")
    
    for cell in worksheet.range('P:P'):
        if cell.value == search_query or cell.value[-10:] == search_query[-10:]:
            found = True
            break
    
    if found:
        update.message.reply_text("تم التحقق بنجاح ✅ ويمكنك التمتع بالخصومات")
        worksheet2.append_row([update.message.text]) 
    else:
        update.message.reply_text("⚠️عذرا هذا الخصم لا يشملك يمكنك اعادة المحاولة والتحقق من رقم هاتفك المسجل في تطبيق بلي⚠️")
    
search_handler = MessageHandler(Filters.text & (~Filters.command), search_value)
dispatcher.add_handler(search_handler)

def start(update, context):
    
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('D:\partners\Welcome.jpg', 'rb'))
    context.bot.send_message(chat_id=update.message.chat_id, text="مرحبا كابتن بلي الغالي💙, لطفا ارسل رقم الهاتف المسجل في تطبيق كابتن بلي للتحقق من الخصم الخاص بك 📱")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
