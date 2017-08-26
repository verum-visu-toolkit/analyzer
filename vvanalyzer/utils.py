class Noop:
    def __init__(self):
        pass

    def noop(*args, **kw):
        pass

    def __getattr__(self, _):
        return self.noop


class Utils:
    def __init__(self):
        self.pbar = Noop()

    @property
    def pbar(self):
        return self.pbar

    @pbar.setter
    def pbar(self, pbar):
        self.pbar = pbar
