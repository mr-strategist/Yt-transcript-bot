import os
import nltk
nltk.download('punkt')

# Bot Configuration
BOT_TOKEN = os.environ['BOT_TOKEN']
ADMIN_ID = int(os.environ.get('ADMIN_ID', '123456789'))
BIN_CHANNEL = os.environ.get('BIN_CHANNEL', '-100123456789')

# Rate Limiting
MAX_MESSAGES = 10
TIME_WINDOW = 60

# Summary Cache Settings
CACHE_CLEAR_INTERVAL = 3600  # Clear cache every hour
MAX_SUMMARY_LENGTH = 4000  # Maximum summary length for Telegram 