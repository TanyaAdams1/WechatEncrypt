import pyqrcode
from cryptography.fernet import Fernet
from reportlab.lib.validators import isCallable

from wxbot.wxbot import WXBot


def encode(data):
    """
    Encode string to byte in utf-8
    :param data: Byte or str
    :return: Encoded byte data
    :raises: TypeError
    """
    if isinstance(data, bytes):
        return data
    elif isinstance(data, str):
        return str.encode(data)
    else:
        return bytes(data)


def decode(data):
    """
    Decode byte to string in utf-8
    :param data: Byte or str
    :return: Decoded string
    :raises: TypeError
    """
    if isinstance(data, str):
        return data
    elif isinstance(data, bytes):
        return bytes.decode(data)
    else:
        return str(data)


def encrypt(data, key):
    f = Fernet(encode(key))
    return decode(f.encrypt(encode(data)))


def decrypt(data, key):
    f = Fernet(encode(key))
    return decode(f.decrypt(encode(data)))


class MyWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)
        self.callbacks = []
        self.qr_file_path = None

    def add_callback(self, condition, function):
        if isCallable(condition) and isCallable(function):
            self.callbacks.append({condition: function})

    def handle_msg_all(self, msg):
        for callback in self.callbacks:
            if callback[0](msg):
                callback[1](msg)

    def gen_qr_code(self, qr_file_path):
        string = 'https://login.weixin.qq.com/l/' + self.uuid
        qr = pyqrcode.create(string)
        if self.conf['qr'] == 'png':
            qr.png(qr_file_path, scale=8)
            # img = Image.open(qr_file_path)
            # img.show()
        elif self.conf['qr'] == 'tty':
            print(qr.terminal(quiet_zone=1))
        self.qr_file_path = qr_file_path
