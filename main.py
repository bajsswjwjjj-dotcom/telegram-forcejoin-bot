import os
import logging
import asyncio
from aiohttp import web
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- BOT CONFIGURATION ---
BOT_TOKEN = "8706022254:AAHiD3Lr3neC05K12pBiOOuMLXetsqD3Xh8"

# Channel Links
CHANNEL_LINKS = [
    "https://t.me/+7_UwpkqH8pRlNzBl",
    "https://t.me/+bgqFJHKtqZEzMTVl"
]

# Destination Link / File
FILE_OR_LINK = "https://www.youtube.com/live/OChxZeq0HUo?si=8e53zv2TbX9nYTly"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for idx, link in enumerate(CHANNEL_LINKS, start=1):
        keyboard.append([InlineKeyboardButton(f"📢 Join Channel {idx}", url=link)])
    
    # Direct Verify Callback
    keyboard.append([InlineKeyboardButton("🔄 Verify / Get Link", callback_data="get_link")])
    
    await update.message.reply_text(
        "⚠️ Kripya pehle dono channels join karein, uske baad 'Verify / Get Link' button par click karein:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    if query.data == "get_link":
        # Direct Link Access when user taps Verify
        await query.answer("✅ Success!")
        await query.edit_message_text(
            f"✅ Verification Successful!\n\n"
            f"Aapki File / Link yeh rahi:\n👉 {FILE_OR_LINK}"
        )

# Web Server for Render Keep-Alive
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
        
