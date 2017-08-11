from multiprocessing import Queue

from chatlog.chatlog import *
from util.util import *


# TODO: Fix view message
class Interface:
    def __init__(self, send_callback=None, contact=[]):
        self.log = Chatlog(contact=contact)
        self.login = False
        self.contact_queue = Queue()
        if isCallable(send_callback):
            self.send = send_callback

    def view_msg(self, arg):
        if str(arg).isnumeric():
            for msg in self.log.get_msg_by_id(arg):
                print('%s:\n\t%s\n' % (msg['name'], msg['content']))
        else:
            id_list = self.log.get_id_by_name(arg)
            if len(id_list) == 0:
                print('Error: No such user\n')
            elif len(id_list) > 1:
                print('Error: %s is ambiguous, several related ids found:\n' % arg,
                      id_list,
                      '\n')
            else:
                print(self.log.get_msg_by_id(id_list[0]))

    def send_msg(self, data, dst, crypt=False):
        if not str(dst).isnumeric():
            dst = self.log.get_id_by_name(dst)
            if len(dst) == 0:
                print('Error: No such user\n')
                return False
            elif len(dst) > 1:
                print('Error: %s is ambiguous, several related ids found:\n' % dst,
                      dst,
                      '\n')
                return False
            else:
                dst = dst[0]
        if crypt:
            data = decode(self.log.fer.encrypt(encode(data)))
        try:
            return self.send(data, dst)
        except AttributeError:
            print('Error: No valid callback inserted')
            return False


    def main_loop(self):
        self.log.contact = self.contact_queue.get()
        print('Got %s contacts' % len(self.log.contact))
        while True:
            choice = input('''
                Input:\n
                1-view message\n
                2-send message\n
                3-view contacts\n
                4-exit:\n
                ''')
            if choice == '1':
                arg = input('Input uid or name:')
                self.view_msg(arg)
            elif choice == '2':
                data = input('Input message to send:')
                dst = input('Input destiny:')
                while True:
                    _crypt = input('Encrypt?(y/n):')
                    if _crypt.lower() == 'y':
                        _crypt = True
                        break
                    elif _crypt.lower() == 'n':
                        _crypt = False
                        break
                    else:
                        print('Invalid input\n')
                if not self.send_msg(data, dst, crypt=_crypt):
                    print('Error: Message not sent')
            elif choice == '3':
                self.log.print_contacts()
            elif choice == '4':
                quit(0)
            else:
                print('Error: Invalid input')

                # TODO: Implement image, voice and video
