from telebot import TeleBot
from config import BOT_TOKEN, CACHE_CLEAR_INTERVAL
from handlers.admin import register_admin_handlers
from handlers.commands import register_command_handlers
from handlers.callbacks import register_callback_handlers
from handlers.youtube import register_youtube_handlers
from utils.summarizer import clear_summary_cache
from keep_alive import keep_alive
import threading
import time

def cache_cleaner():
    """Periodically clear the summary cache to prevent memory buildup"""
    while True:
        time.sleep(CACHE_CLEAR_INTERVAL)
        clear_summary_cache()
        print("Summary cache cleared")

def main():
    # Initialize bot
    bot = TeleBot(BOT_TOKEN)
    
    # Register all handlers
    register_admin_handlers(bot)
    register_command_handlers(bot)
    register_callback_handlers(bot)
    register_youtube_handlers(bot)
    
    # Start cache cleaner in background
    threading.Thread(target=cache_cleaner, daemon=True).start()
    
    # Start keep alive server
    keep_alive()
    
    # Start bot
    print("Bot started...")
    bot.infinity_polling()

if __name__ == "__main__":
    main()
