from multiprocessing import Lock

import chatlog


class Chatlog:
    def __init__(self, contact=[]) -> chatlog:
        self.lock = Lock()
        self.log = []
        self.contact = contact

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
        if (Chatlog.is_plain_text(msg)):
            self.lock.acquire()
            self.log.append(msg)
            self.lock.release()

    def get_msg_by_id(self, id):
        result = []
        self.lock.acquire()
        for msg in self.log:
            if msg['user']['id'] == str(id):
                if msg['msg_type_id'] == 3:
                    result.append({'name': msg['content']['user']['name'],
                                   'content': msg['content']['data']})
                else:
                    result.append({'name': msg['user']['name']})
        self.lock.release()
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
            print(contact)
