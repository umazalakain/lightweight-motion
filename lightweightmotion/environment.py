import os
from datetime import datetime


class Environment(object):
    def __init__(self, store_path, prefix='capture'):
        self.store_path = store_path
        self.prefix = prefix

    @property
    def available_space(self):
        st = os.statvfs(self.store_path)
        return st.f_bavail * st.f_frsize

    def make_space(self, reservation):
        if self.available_space < reservation:
            for filename in sorted(os.listdir(self.store_path)):
                if filename.startswith(self.prefix):
                    os.remove(filename)
                    print('Deleted {} to avoid filling disk'.format(filename))
                    if self.available_space > reservation:
                        return

    def save_frame(self, frame):
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        filename = '{prefix}-{now}.jpg'.format(prefix=self.prefix, now=now)
        filename = os.path.join(self.store_path, filename)
        frame.save(filename)
