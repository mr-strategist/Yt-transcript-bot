from telebot import TeleBot
from config import ADMIN_ID
from utils.storage import AUTHORIZED_USERS, user_stats

def register_admin_handlers(bot: TeleBot):
    @bot.message_handler(commands=['adduser'])
    def add_user(message):
        if message.from_user.id != ADMIN_ID:
            return
        
        try:
            user_id = int(message.text.split()[1])
            AUTHORIZED_USERS.add(user_id)
            bot.reply_to(message, f"✅ User {user_id} has been authorized")
        except:
            bot.reply_to(message, "❌ Usage: /adduser <user_id>")

    @bot.message_handler(commands=['removeuser'])
    def remove_user(message):
        if message.from_user.id != ADMIN_ID:
            return
        
        try:
            user_id = int(message.text.split()[1])
            if user_id == ADMIN_ID:
                bot.reply_to(message, "❌ Cannot remove admin user")
                return
            
            AUTHORIZED_USERS.discard(user_id)
            bot.reply_to(message, f"✅ User {user_id} has been removed")
        except:
            bot.reply_to(message, "❌ Usage: /removeuser <user_id>")

    @bot.message_handler(commands=['listusers'])
    def list_users(message):
        if message.from_user.id != ADMIN_ID:
            return
        
        users_list = "\n".join([f"- {uid}" for uid in AUTHORIZED_USERS])
        bot.reply_to(message, f"Authorized Users:\n{users_list}")

    @bot.message_handler(commands=['stats'])
    def show_stats(message):
        if message.from_user.id != ADMIN_ID:
            return
        
        stats = f"📊 Bot Statistics:\n"
        stats += f"Total Users: {len(AUTHORIZED_USERS)}\n"
        stats += f"Total Requests: {sum(u['requests'] for u in user_stats.values())}\n"
        bot.reply_to(message, stats) 
