import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- FAKE WEB SERVER FOR RENDER PORT CHECK ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running Alive!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

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
            logging.error(f"Error channel {channel}: {e}")
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_joined = await check_membership(user_id, context)
    
    if is_joined:
        await update.message.reply_text(f"✅ Verification Successful!\n\nLink:\n{FILE_OR_LINK}")
    else:
        keyboard = []
        for idx, link in enumerate(CHANNEL_LINKS, start=1):
            keyboard.append([InlineKeyboardButton(f"📢 Join Channel {idx}", url=link)])
        keyboard.append([InlineKeyboardButton("🔄 Verify / Try Again", callback_data="check_join")])
        
        await update.message.reply_text(
            "⚠️ Kripya pehle niche diye gaye dono channels join karein:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_join":
        user_id = query.from_user.id
        is_joined = await check_membership(user_id, context)
        
        if is_joined:
            await query.edit_message_text(f"✅ Verification Successful!\n\nLink:\n{FILE_OR_LINK}")
        else:
            await query.answer("❌ Aapne dono channels join nahi kiye hain!", show_alert=True)

def main():
    # Start web server in background thread for Render
    threading.Thread(target=run_web_server, daemon=True).start()
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print(">>> BOT IS LIVE <<<")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
