import requests


class ChannelModerator:
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id
        try:
            self.chat = self.bot.get_chat(self.chat_id)
            self.title = self.chat.title
        except:
            pass

    def create_invite_link(self):
        invite_link = self.bot.create_chat_invite_link(chat_id=self.chat_id, member_limit=1)
        if invite_link:
            invite_link = invite_link.invite_link
        return invite_link

    def check_link(self, invite_link):
        link_result = requests.get(invite_link).text
        if self.title in link_result:
            return False
        else:
            return True

