import logging
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = "8766697654:AAFn2EbH-mkHwwzpn0_f9Rjsi6L2scVV5Fc"
GURUH_ID = -1001568505976
topic_ids = {}
logging.basicConfig(level=logging.INFO)

def viloyat_topish(matn):
    m = matn.lower()
    if "toshkent" in m: return "toshkent"
    if "samarqand" in m: return "samarqand"
    if "namangan" in m: return "namangan"
    if "andijon" in m: return "andijon"
    if "farg" in m or "fargona" in m: return "fargona"
    if "xorazm" in m: return "xorazm"
    if "qashqa" in m: return "qashqadaryo"
    if "surxon" in m: return "surxondaryo"
    if "jizzax" in m: return "jizzax"
    if "sirdaryo" in m: return "sirdaryo"
    if "navoiy" in m: return "navoiy"
    if "buxoro" in m: return "buxoro"
    if "qoraqalp" in m: return "qoraqalpogiston"
    return None

async def xabar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    matn = update.message.text or update.message.caption or ""
    if not matn: return
    thread_id = update.message.message_thread_id
    viloyat = viloyat_topish(matn)
    if thread_id and viloyat:
        topic_ids[viloyat] = thread_id
    if not viloyat: return
    if viloyat not in topic_ids or not topic_ids[viloyat]: return
    try:
        await context.bot.send_message(chat_id=GURUH_ID, text=f"📦 YUK ELONI\n\n{matn}", message_thread_id=topic_ids[viloyat])
    except Exception as e:
        logging.error(f"Xato: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Logistmen bot ishga tushdi!")

async def setid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Format: /setid viloyat raqam")
        return
    topic_ids[args[0].lower()] = int(args[1])
    await update.message.reply_text(f"{args[0]} = {args[1]} saqlandi!")

async def getid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tid = update.message.message_thread_id
    await update.message.reply_text(f"Topic ID: {tid}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("setid", setid))
    app.add_handler(CommandHandler("getid", getid))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, xabar))
    app.run_polling()

if name == "main":
    main()
