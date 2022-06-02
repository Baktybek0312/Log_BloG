
class SetTrigger(object):
    def __init__(self):
        self.set_work = False
        self.set_reload = False
        self.set_refresh = False

    def UpdateSetRefresh(self):
        self.set_refresh = True
        return self.set_refresh

    def UpdateSetWork(self):
        self.set_work = True
        return self.set_work

    def UpdateSetReload(self):
        self.set_reload = True
        return self.set_reload
