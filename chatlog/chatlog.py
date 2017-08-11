import os
from base64 import urlsafe_b64encode
from configparser import ConfigParser, NoSectionError, NoOptionError
from multiprocessing import Lock

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

import chatlog
from util.util import *

DEFAULT_PASWD = '12345678'
DEFAULT_SALT = b'SALT'


class Chatlog:
    def __init__(self, contact=[]) -> chatlog:
        self.msg_lock = Lock()
        self.log = {}
        self.contact = contact
        temp_pwd = os.path.join(os.getcwd(), 'temp')
        conf_path = os.path.join(temp_pwd, 'config.ini')
        if not os.path.exists(conf_path):
            open(conf_path, 'w')
        conf = ConfigParser()
        conf.read(conf_path)

        try:
            salt = str.encode(conf.get(section='chatlog', option='salt'))
            password = conf.get(section='chatlog', option='password')
        except NoSectionError:
            f = open(conf_path, 'w+')
            conf.add_section('chatlog')
            salt = DEFAULT_SALT
            password = DEFAULT_PASWD
            conf.set('chatlog', 'salt', value=str(salt))
            conf.set('chatlog', 'password', value=DEFAULT_PASWD)
            conf.write(f)
            f.close()
        except NoOptionError:
            f = open(conf_path, 'w+')
            salt = DEFAULT_SALT
            password = DEFAULT_PASWD
            conf.set(section='chatlog', option='salt', value=str(salt))
            conf.set(section='chatlog', option='password', value=DEFAULT_PASWD)
            conf.write(f)
            f.close()
        except Exception as e:
            pass
        finally:
            self.fer = Fernet(urlsafe_b64encode(Scrypt(
                salt=salt,
                length=32,
                n=2 ** 14,
                r=8,
                p=1,
                backend=default_backend()
            ).derive(str.encode(password))))
            self.encrypt = True

    @staticmethod
    def is_plain_text(msg):
        try:
            if not msg['msg_type_id'] == 2:
                if msg['content']['type'] == 0:
                    return True
        except:
            return False
        return False

    def add_msg(self, msg):
        try:
            msg['content']['data'] = self.fer.decrypt(str.encode(
                msg['content']['data']
            ))
        except:
            pass
        self.msg_lock.acquire()
        if not msg['user']['id'] in self.log:
            self.log[msg['user']['id']] = ''
        if msg['msg_type_id'] == 3:
            self.log[msg['user']['id']] += 'Name:%s\n%s\n' \
                                           % (msg['content']['user']['name'],
                                              msg['content']['data'])
        elif msg['msg_type_id'] == 4:
            self.log[msg['user']['id']] += 'Name:%s\n%s\n' \
                                           % (msg['user']['name'],
                                              msg['content']['data'])
        elif msg['msg_type_id'] == 1:
            pass
        # TODO: Fix this
        self.msg_lock.release()

    def get_msg_by_id(self, id):
        flag = False
        for contact in self.contact:
            if id == contact['UserName']:
                flag = True
                break
        if not flag:
            id = self.get_id_by_name(id)
        self.msg_lock.acquire()
        try:
            result = self.log[id]
        except:
            result = 'None.\n'
        self.msg_lock.release()
        return result

    def get_id_by_name(self, name):
        result = []
        for contact in self.contact:
            if 'RemarkName' in contact and contact['RemarkName'] == name:
                result.append(contact['UserName'])
            elif 'NickName' in contact and contact['NickName'] == name:
                result.append(contact['UserName'])
            elif 'DisplayName' in contact and contact['DisplayName'] == name:
                result.append(contact['UserName'])
        return result

    def print_contacts(self):
        for contact in self.contact:
            print('Nickname:', contact['NickName'], '\nRemarkName:', contact['RemarkName'])
