from telebot import TeleBot
from utils.decorators import auth_required
from utils.storage import user_languages, user_formats, user_transcripts
from utils.summarizer import generate_summary
from nltk.tokenize import sent_tokenize
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_command_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    @auth_required
    def send_welcome(message):
        welcome_text = """
🎥 *YouTube Transcript Bot*
_Developed by @MR\_STRATEGIST_

Simply send me any YouTube video link and I'll:
• Extract the transcript
• Provide options for format and language
• Allow you to search and summarize

*Available Commands:*
• /start \- Show this welcome message
• /help \- Show help information
• /search \- Search in transcript
• /summary \- Get summary
• /language \- Change language
• /format \- Change format

Send a YouTube link to get started\! 🚀
"""
        bot.reply_to(message, welcome_text, parse_mode='MarkdownV2')

    @bot.message_handler(commands=['help'])
    @auth_required
    def help_command(message):
        help_text = """
📚 *How to Use This Bot*

*1\. Get Transcript*
• Send any YouTube video link
• Works with regular videos and shorts
• Example: `youtube\.com/watch?v=xxxxx`

*2\. Available Commands*
• /start \- Welcome message
• /help \- Show this help
• /search \- Search in transcript
• /summary \- Get summary
• /language \- Change language
• /format \- Change format

*3\. Tips*
• Process video first before using commands
• Use buttons below transcript for quick access
• Only works with videos having subtitles/CC

Need Help? Contact: @MR\_STRATEGIST
"""
        bot.reply_to(message, help_text, parse_mode='MarkdownV2')

    @bot.message_handler(commands=['language'])
    @auth_required
    def set_language(message):
        langs = """
🌍 Available Languages:
/en - English
/es - Spanish
/hi - Hindi
/fr - French
/de - German

Usage: Just send the command for your preferred language
"""
        bot.reply_to(message, langs)

    @bot.message_handler(commands=['format'])
    @auth_required
    def set_format(message):
        formats = """
⚙️ Transcript Formats:
/text - Plain text
/time - With timestamps
/para - Paragraph format

Current format will be saved for your next requests.
"""
        bot.reply_to(message, formats)

    @bot.message_handler(commands=['search'])
    @auth_required
    def search_transcript(message):
        user_id = message.from_user.id
        if user_id not in user_transcripts:
            bot.reply_to(message, "⚠️ Please process a video first using its YouTube link")
            return
            
        try:
            query = message.text.split(' ', 1)[1]
            transcript_text = user_transcripts[user_id]
            matches = [line for line in transcript_text.split('\n') if query.lower() in line.lower()]
            if matches:
                result = f"🔍 Found {len(matches)} matches for '{query}':\n\n" + '\n'.join(matches[:10])
                if len(matches) > 10:
                    result += "\n\n(Showing first 10 matches)"
            else:
                result = f"No matches found for '{query}'"
            bot.reply_to(message, result)
        except IndexError:
            bot.reply_to(message, "Usage: /search <word or phrase>")

    @bot.message_handler(commands=['summary'])
    @auth_required
    def get_summary(message):
        user_id = message.from_user.id
        if user_id not in user_transcripts:
            bot.reply_to(message, "⚠️ Please process a video first using its YouTube link")
            return
            
        try:
            transcript_text = user_transcripts[user_id]
            
            # Send processing message
            processing_msg = bot.reply_to(message, "Generating summary... ⏳")
            
            # Generate summary using BART
            summary = generate_summary(transcript_text)
            
            if summary:
                summary_text = "📝 AI-Generated Summary:\n\n" + summary
                
                # Ensure we don't exceed Telegram's message length limit
                if len(summary_text) > 4000:
                    summary_text = summary_text[:3997] + "..."
                    
                # Delete processing message and send summary
                bot.delete_message(message.chat.id, processing_msg.message_id)
                bot.reply_to(message, summary_text)
            else:
                bot.edit_message_text(
                    "❌ Failed to generate summary. Please try again.",
                    message.chat.id,
                    processing_msg.message_id
                )
                
        except Exception as e:
            bot.reply_to(message, f"Error generating summary: {str(e)}")

    @bot.message_handler(commands=['en', 'es', 'hi', 'fr', 'de'])
    @auth_required
    def set_language_command(message):
        user_id = message.from_user.id
        lang = message.text[1:]  # Remove the '/'
        user_languages[user_id] = lang.upper()
        bot.reply_to(message, f"✅ Language set to: {lang.upper()}")

    @bot.message_handler(commands=['text', 'time', 'para'])
    @auth_required
    def set_format_command(message):
        user_id = message.from_user.id
        format_type = message.text[1:]  # Remove the '/'
        user_formats[user_id] = format_type
        bot.reply_to(message, f"✅ Format set to: {format_type}") 