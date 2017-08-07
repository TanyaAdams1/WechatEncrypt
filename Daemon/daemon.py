from multiprocessing import Process

from NGUI.interface import Interface
from chatlog.chatlog import Chatlog
from util.util import MyWXBot


class Daemon:
    def __init__(self):
        self.bot = MyWXBot(logincallback=self._init)
        self.bot.DEBUG = True
        self.interface = Interface(send_callback=self.bot.send_msg_by_uid)
        self.bot.add_callback(Chatlog.is_plain_text, self.interface.log.add_msg)
        self.bot_process = Process(target=self.bot.run)
        self.bot_process.start()
        self.interface.main_loop()

    def _init(self):
        self.interface.contact_queue.put(self.bot.contact_list
                                         + self.bot.group_list)
