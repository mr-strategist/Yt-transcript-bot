import os
from telebot import TeleBot
from utils.decorators import auth_required, check_rate_limit
from utils.helpers import extract_video_id, get_video_info
from utils.storage import user_transcripts, user_languages, user_formats, update_stats
from youtube_transcript_api import YouTubeTranscriptApi

def register_youtube_handlers(bot: TeleBot):
    @bot.message_handler(func=lambda message: 
        message.text and (
            'youtube.com' in message.text.lower() or 
            'youtu.be' in message.text.lower()
        )
    )
    @auth_required
    def handle_youtube_link(message):
        user_id = message.from_user.id
        
        if not check_rate_limit(user_id):
            bot.reply_to(message, "⚠️ Rate limit exceeded. Please wait a minute.")
            return
        
        try:
            processing_msg = bot.reply_to(message, "Processing your request... ⏳")
            
            video_id = extract_video_id(message.text)
            if not video_id:
                bot.edit_message_text(
                    "Please send a valid YouTube video link. 🔍", 
                    message.chat.id, 
                    processing_msg.message_id
                )
                return

            # Get video info and send it
            video_info = get_video_info(video_id)
            if video_info:
                bot.send_message(message.chat.id, video_info)

            # Get and process transcript
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            transcript_text = ""
            for text in transcript:
                transcript_text += text['text'] + "\n"

            # Store transcript
            user_transcripts[user_id] = transcript_text
            update_stats(user_id)

            # Save and send transcript file
            filename = f"transcript_{video_id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(transcript_text)

            with open(filename, "rb") as f:
                bot.send_document(
                    message.chat.id, 
                    document=f,
                    caption="📝 Here's your transcript!"
                )

            # Delete processing message and file
            bot.delete_message(message.chat.id, processing_msg.message_id)
            os.remove(filename)

            # Send menu message
            menu_text = """
*Available Actions:* 🎯

Type these commands:
1\. `/search word` \- Find specific text
2\. `/summary` \- Get key points
3\. `/language` \- Change language
4\. `/format` \- Change format

*Current Settings:*
• Language: `{}`
• Format: `{}`

*Examples:*
• `/search hello`
• `/summary`
• `/language`
""".format(
    user_languages.get(user_id, 'EN'),
    user_formats.get(user_id, 'text')
)
            try:
                bot.send_message(
                    message.chat.id, 
                    menu_text, 
                    parse_mode='MarkdownV2'
                )
            except Exception:
                # Fallback to plain text if markdown fails
                simple_menu = """
Available Actions 🎯

Type these commands:
1. /search word - Find specific text
2. /summary - Get key points
3. /language - Change language
4. /format - Change format

Type /help for more information
"""
                bot.send_message(message.chat.id, simple_menu)

        except Exception as e:
            try:
                bot.delete_message(message.chat.id, processing_msg.message_id)
            except:
                pass
                
            error_text = """
❌ Error processing video

Please check:
• Video exists
• Has subtitles/CC
• Link is correct

Try another video or contact @MR_STRATEGIST for help.
"""
            bot.send_message(message.chat.id, error_text)

    # Handler for non-command messages that aren't YouTube links
    @bot.message_handler(func=lambda message: 
        message.text and not message.text.startswith('/') and
        'youtube.com' not in message.text.lower() and 
        'youtu.be' not in message.text.lower()
    )
    @auth_required
    def handle_other_messages(message):
        bot.reply_to(message, "Please send a YouTube video link or use available commands.") 