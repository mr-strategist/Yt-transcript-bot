from telebot import TeleBot
from utils.storage import user_transcripts, user_languages, user_formats

def register_callback_handlers(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def handle_query(call):
        try:
            user_id = call.from_user.id
            
            if call.data == "cmd_search":
                bot.answer_callback_query(call.id)
                search_msg = """
🔍 *How to Search*
Send: `/search word` to find text
Example: `/search hello`
"""
                bot.send_message(
                    call.message.chat.id,
                    search_msg,
                    parse_mode='MarkdownV2'
                )

            elif call.data == "cmd_summary":
                bot.answer_callback_query(call.id)
                if user_id not in user_transcripts:
                    bot.send_message(call.message.chat.id, "⚠️ No transcript found. Process a video first!")
                    return
                    
                class MockMessage:
                    def __init__(self, chat_id, from_user):
                        self.chat = type('obj', (object,), {'id': chat_id})
                        self.from_user = from_user
                
                mock_msg = MockMessage(call.message.chat.id, call.from_user)
                from handlers.commands import get_summary
                get_summary(mock_msg)

            elif call.data == "cmd_language":
                bot.answer_callback_query(call.id)
                current_lang = user_languages.get(user_id, 'English')
                langs = f"""
🌍 *Available Languages*
• `/en` \- English
• `/es` \- Spanish
• `/hi` \- Hindi
• `/fr` \- French
• `/de` \- German

Current: `{current_lang}`
"""
                bot.send_message(
                    call.message.chat.id,
                    langs,
                    parse_mode='MarkdownV2'
                )

            elif call.data == "cmd_format":
                bot.answer_callback_query(call.id)
                current_format = user_formats.get(user_id, 'text')
                formats = f"""
⚙️ *Available Formats*
• `/text` \- Plain text
• `/time` \- With timestamps
• `/para` \- Paragraph format

Current: `{current_format}`
"""
                bot.send_message(
                    call.message.chat.id,
                    formats,
                    parse_mode='MarkdownV2'
                )

        except Exception as e:
            print(f"Callback error: {e}")
            bot.answer_callback_query(call.id, "An error occurred!") 