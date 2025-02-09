from collections import defaultdict
from typing import Dict
from datetime import datetime
from config import ADMIN_ID

# User Storage
AUTHORIZED_USERS = {ADMIN_ID}
user_transcripts: Dict[int, str] = {}
user_languages: Dict[int, str] = {'default': 'en'}
user_formats: Dict[int, str] = {'default': 'text'}
user_stats = defaultdict(lambda: {"requests": 0, "last_used": None})
rate_limit_dict = defaultdict(list)

def update_stats(user_id):
    user_stats[user_id]["requests"] += 1
    user_stats[user_id]["last_used"] = datetime.now()

def log_to_channel(bot, BIN_CHANNEL, message):
    try:
        bot.send_message(BIN_CHANNEL, message)
    except Exception as e:
        print(f"Failed to log to channel: {e}") 