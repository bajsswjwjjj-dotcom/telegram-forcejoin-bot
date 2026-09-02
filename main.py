import os
import logging
import asyncio
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- BOT CONFIGURATION ---
BOT_TOKEN = "8706022254:AAHiD3Lr3neC05K12pBiOOuMLXetsqD3Xh8"

CHANNELS = [-1004468058339, -1003917354701]
CHANNEL_LINKS = ["https://t.me/+7_UwpkqH8pRlNzBl", "https://t.me/+bgqFJHKtqZEzMTVl"]
FILE_OR_LINK = "https://youtube.com/@techcrazyraj0?si=e3piAwbdz3W809n4"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def check_membership(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        except Exception as e:
            # ID Mismatch/Telegram API Exception par bypass hoga
            logging.error(f"Channel Bypass triggered for {channel}: {e}")
            pass
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_joined = await check_membership(user_id, context)
    
    if is_joined:
        await update.message.reply_text(f"✅ Verification Successful!\n\nAapki file / link:\n{FILE_OR_LINK}")
    else:
        keyboard = []
        for idx, link in enumerate(CHANNEL_LINKS, start=1):
            keyboard.append([InlineKeyboardButton(f"📢 Join Channel {idx}", url=link)])
        keyboard.append([InlineKeyboardButton("🔄 Verify / Try Again", callback_data="check_join")])
        
        await update.message.reply_text(
            "⚠️ Kripya pehle dono channels join karein, uske baad 'Verify / Try Again' button par click karein:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if query.data == "check_join":
        is_joined = await check_membership(user_id, context)
        
        if is_joined:
            await query.answer("✅ Verification Successful!")
            await query.edit_message_text(f"✅ Verification Successful!\n\nAapki file / link:\n{FILE_OR_LINK}")
        else:
            await query.answer("❌ Mara bacha pahle donon channel Join kar!", show_alert=True)

async def handle_ping(request):
    return web.Response(text="Bot Alive!")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))

    web_app = web.Application()
    web_app.router.add_get('/', handle_ping)
    
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

    await app.initialize()
    await app.start()
    await app.updater.start_polling(drop_pending_updates=True)
    
    print(">>> BOT IS LIVE <<<")
    await asyncio.Event().wait()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
        
