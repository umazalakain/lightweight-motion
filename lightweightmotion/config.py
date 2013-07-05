import os


class Config(object):
    home_config = os.path.join(os.environ['HOME'], 
            '.config/lightweightmotion/config.py')

    def get(self, arg_key, config_key):
        return self.args[arg_key] or self.config.get(config_key, None)

    @classmethod
    def load(cls, args, config_file=None):
        config = cls()
        config.args = args

        if config_file is None
            config_file = self.home_config
        loaded = {}
        execfile(config_file, {}, loaded)
        config.config = loaded
        return config

    @property
    def DEVICE(self):
        if self.args['<device'>]:
            try:
                device = int(self.args['<device>'])
            except ValueError:
                return None
        else:
            device = self.config.get('DEVICE', None)
        return device

    @property
    def URL(self):
        if self.DEVICE is None:
            url = self.args['<device>'] or self.config.get('URL', None)
            if url is None:
                raise

    @property
    def STREAM(self):
        host, port = self.get('--stream', 'STREAM').split(':')
        port = int(port)
        return host, port

    @property
    def WINDOW(self):
        return self.get('--window', 'WINDOW')

    @property
    def MOVEMENT_THRESHOLD(self):
        threshold = self.get('--threshold', 'MOVEMENT_THRESHOLD')
        return float(threshold)

    @property
    def MOVEMENT_SENSITIVITY(self):
        sensitivity = self.get('--sensitivity', 'MOVEMENT_SENSITIVITY')
        return float(sensitivity)

    @property
    def EVENT_DIR(self):
        return self.get('--directory', 'EVENT_DIR')

    @property
    def EVENT_BEFORE(self):
        return self.get('--before', 'EVENT_BEFORE')

    @property
    def EVENT_AFTER(self):
        return self.get('--after', 'EVENT_AFTER')

    @property
    def DEBUG(self):
        return self.get('--verbose', 'DEBUG')
