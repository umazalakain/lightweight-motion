class Config(dict):
    def _get_stream(self, string):
        host, port = string.split(':')
        port = int(port)
        return host, port

    def _get_movement_threshold(self, string):
        return float(string)

    def _get_movement_sensitivity(self, string):
        return float(string)


class ArgsConfig(Config):
    @property
    def DEVICE(self):
        try:
            return int(self['<device>'])
        except ValueError:
            return None

    @property
    def URL(self):
        if self.DEVICE is None:
            return self['<device>']

    @property
    def STREAM(self):
        return self._get_stream(self['--stream'])

    @property
    def WINDOW(self):
        return self['--window']

    @property
    def MOVEMENT_THRESHOLD(self):
        return self._get_movement_threshold(self['--threshold'])

    @property
    def MOVEMENT_SENSITIVITY(self):
        return self._get_movement_sensitivity(self['--sensitivity'])

    @property
    def EVENT_DIR(self):
        return self['--directory']

    @property
    def EVENT_BEFORE(self):
        return self['--before']

    @property
    def EVENT_AFTER(self):
        return self['--after']

    @property
    def DEBUG(self):
        return self['--verbose']


class FileConfig(Config):
    def __init__(self, config_file):
        execfile(config_file, {}, self)

    def __getattr__(self, name):
        return self[name]

    @property
    def STREAM(self):
        return self._get_stream(self['STREAM'])

    @property
    def MOVEMENT_THRESHOLD(self):
        return self._get_movement_threshold(self['MOVEMENT_THRESHOLD'])

    @property
    def MOVEMENT_SENSITIVITY(self):
        return self._get_movement_sensitivity(self['MOVEMENT_SENSITIVITY'])
