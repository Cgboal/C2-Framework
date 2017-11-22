import json
from socket import gethostname
from sys import platform

from agent.agent.settings import *
from .decorators import Request
from .pycle import *

fetch = Request('127.0.0.1', port=8000)
state = State(state_file)


def register():
    data = {
        "name" : gethostname(),
        "os" : platform,
    }

    uuid = state.get_field('uuid')
    if uuid:
        data['uuid'] = uuid
        
    @fetch('/api/agents/', proto="POST", data=data)
    def handle(resp):
        print data
        print resp
        resp_json = json.loads(resp)
        data['uuid'] = resp_json['uuid']
        state.update(data)
        print state.dump()
    handle()