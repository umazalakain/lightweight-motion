import logging
import os
from datetime import datetime


class Environment(object):
    def __init__(self, store_path, prefix='capture'):
        self.store_path = store_path
        self.prefix = prefix
        if not os.path.isdir(self.store_path):
            logging.warning('Directory {} does not exist'.format(self.store_path))
            os.mkdir(self.store_path)
            logging.info('Directory {} created'.format(self.store_path))

    @property
    def available_space(self):
        st = os.statvfs(self.store_path)
        return st.f_bavail * st.f_frsize

    def make_space(self, reservation):
        if self.available_space < reservation:
            logging.warning('No free space available, proceeding to making space')
            for dirname in sorted(os.listdir(self.store_path)):
                if dirname.startswith(self.prefix):
                    os.rmdir(dirname)
                    logging.info('Deleted directory {} to avoid filling disk'.format(dirname))
                    if self.available_space > reservation:
                        logging.info('Free space now available')
                        return

    def save_event(self, event):
        dirname = os.path.join(self.store_path, self.capture_filename())
        os.mkdir(dirname)
        logging.info('Saving movement event in {}'.format(dirname))
        for frame in event:
            self.make_space(40 * 1024**2)
            filename = '{}.jpg'.format(self.capture_filename())
            filename = os.path.join(dirname, filename)
            frame.save(filename)
            logging.debug('Saved frame {}'.format(filename))

    def capture_filename(self):
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')
        return '{}-{}'.format(self.prefix, now)
