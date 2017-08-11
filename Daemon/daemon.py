from threading import Thread

from NGUI.interface import Interface
from chatlog.chatlog import Chatlog
from util.util import MyWXBot


class Daemon:
    def __init__(self):
        self.bot = MyWXBot(logincallback=self._init)
        self.bot.DEBUG = True
        self.interface = Interface(send_callback=self.bot.send_msg_by_uid)
        self.bot.add_callback(Chatlog.is_plain_text, self.interface.log.add_msg)
        self.bot_thread = Thread(target=self.bot.run)
        self.bot_thread.start()
        self.interface.main_loop()

    def _init(self):
        self.interface.contact_queue.put(self.bot.full_member_list)
