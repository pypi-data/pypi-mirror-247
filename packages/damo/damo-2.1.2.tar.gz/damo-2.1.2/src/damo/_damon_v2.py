
class DamonFsOps:
    def read(self):
        pass

    def write(self):
        pass

class DamonCtx:
    kdamond = None

    def stage(self):
        pass

    def read(self):
        pass

class Kdamond:
    contexts = None
    kdamonds = None

    def __init__(self, contexts):
        self.contexts = contexts

    def stage(self):
        self.kdamonds.fs.stage(self)
    def start(self):
        pass
    def stop(self):
        pass
    def commit(self):
        pass
    def commit_schemes_quota_goals(self):
        pass
    def update_schemes_stats(self):
        pass
    def update_schemes_tried_regions(self):
        pass
    def update_schemes_tried_bytes(self):
        pass
    def clear_schemmes_tried_regions(self):
        pass

class Kdamonds:
    kdamonds = None

    def __init__(self, kdamonds):
        self.kdamonds = kdamonds
        for kdamond in self.kdamonds:
            kdamond.kdamonds = self

    def set_fs(self, fs):
        self.fs = fs

    def stage(self):
        self.fs.stage(self)


kdamonds = Kdamonds()
kdamonds.set_fs(_damon_sysfs)
kdamonds.stage()
kdamonds.kdamonds[1].start()
kdamonds.kdamonds[1].commit()
kdamonds.kdamonds[1].stop()

kdamonds.stage()
