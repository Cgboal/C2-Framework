

class Error(Exception):
    pass


class BeaconCommandNotFound(Error):
    def __init__(self):
        self.message = "No command found"


class StateLoadFailed(Error):
    def __init__(self):
        self.message = "Agent state load operation failed"
