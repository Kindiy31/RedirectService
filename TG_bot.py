import telebot
import config
from channel_moderator import ChannelModerator
from logger_config import logger

bot = telebot.TeleBot(config.TOKEN)
bot.parse_mode = "HTML"

moderator = ChannelModerator(bot=bot, chat_id=config.chat_id)

@bot.message_handler(content_types=['text'])
def other_messages(message):
    logger.info(f"Get new message and delete after: {message}")
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    except Exception as e:
        logger.error(f"Error delete message: {e}")

@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def new_chat_members_handler(message):
    logger.info(f"Get new message and delete after: {message}")
    try:
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    except Exception as e:
        logger.error(f"Error delete message: {e}")

