import json
from agent.agent.settings import *
from socket import gethostname
from sys import platform
from agent.lib.decorators import Request
from pycle import State

fetch = Request('127.0.0.1', port=8000)
state = State(state_file)


def register():
    data = {
        "name" : gethostname(),
        "os" : platform,
    }
    @fetch('/api/agents/', proto="POST", data=data)
    def handle(resp):
        resp_json = json.loads(resp)
        data['id'] = resp_json['id']
        state.update(data)
        print state.dump()
    handle()