

class Error(Exception):
    pass

class BeaconCommandNotFound(Error):
    def __init__(self):
        self.message = "No command found"


