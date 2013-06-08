import os
from datetime import datetime


class Environment(object):
    def __init__(self, store_path, prefix='capture'):
        self.store_path = store_path
        self.prefix = prefix
        if not os.path.isdir(self.store_path):
            os.mkdir(self.store_path)

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

    def save_event(self, event):
        dirname = os.path.join(self.store_path, self.capture_filename())
        os.mkdir(dirname)
        for frame in event:
            self.make_space(40 * 1024**2)
            filename = '{}.jpg'.format(self.capture_filename())
            filename = os.path.join(dirname, filename)
            frame.save(filename)

    def capture_filename(self):
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        return '{}-{}'.format(self.prefix, now)
