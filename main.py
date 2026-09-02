import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8706022254:AAHiD3Lr3neC05K12pBiOOuMLXetsqD3Xh8"

# Channel IDs (-100 ke sath)
CHANNELS = [
    -1004468058339,
    -1003917354701
]

# Invite Links
CHANNEL_LINKS = [
    "https://t.me/+7_UwpkqH8pRlNzBl",
    "https://t.me/+bgqFJHKtqZEzMTVl"
]

FILE_OR_LINK = "https://youtube.com/@techcrazyraj0?si=e3piAwbdz3W809n4"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def check_membership(user_id, context):
    """Strict verification system"""
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            logger.info(f"User {user_id} status in {channel}: {member.status}")
            
            # Sirf Valid Members ko pass hone dega
            if member.status not in ['creator', 'administrator', 'member']:
                return False
        except Exception as e:
            logger.error(f"Verification error for channel {channel}: {e}")
            # Agar Bot channel me admin nahi hai ya check fail hota hai toh block rakho
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    is_joined = await check_membership(user_id, context)
    
    if is_joined:
        await update.message.reply_text(
            f"✅ Verification Successful!\n\nYe rahi aapki file/link:\n{FILE_OR_LINK}"
        )
    else:
        keyboard = []
        for idx, link in enumerate(CHANNEL_LINKS, start=1):
            keyboard.append([InlineKeyboardButton(f"📢 Join Channel {idx}", url=link)])
        
        keyboard.append([InlineKeyboardButton("🔄 Verify / Try Again", callback_data="check_join")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚠️ Kripya pehle niche diye gaye dono channels join karein. Iske bina link nahi milega:",
            reply_markup=reply_markup
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_join":
        user_id = query.from_user.id
        is_joined = await check_membership(user_id, context)
        
        if is_joined:
            await query.edit_message_text(
                f"✅ Verification Successful!\n\nYe raha aapka link:\n{FILE_OR_LINK}"
            )
        else:
            await query.answer("❌ Aapne dono channels join nahi kiye hain!", show_alert=True)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    print(">>> BOT IS LIVE <<<")
    app.run_polling()

if __name__ == '__main__':
    main()
  
