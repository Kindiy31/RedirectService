import telebot
import config
from channel_moderator import ChannelModerator

bot = telebot.TeleBot(config.TOKEN)
bot.parse_mode = "HTML"

moderator = ChannelModerator(bot=bot, chat_id=config.chat_id)
link = moderator.create_invite_link()


@bot.message_handler(content_types=['new_chat_members'])
def new_chat_members_handler(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
