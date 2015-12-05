"""lightweight-motion

Lightweight motion detection, ready for your RPi!

Usage:
    lightweight-motion -c <config_file>
    lightweight-motion [options] <device> [-d <output-dir>] [-s <host:port>] [-w]
    lightweight-motion [options] <url> [-d <output-dir>] [-s <host:port>] [-w]
    lightweight-motion (-h | --help)
    lightweight-motion --version

Arguments:
    <device>                    Input video device ID (normally 0)
    <url>                       Input video device url (ex: http://user:pass@your.cam/videostream.cgi)

Outputs:
    -d --directory <output-dir> Output directory for recorded events
    -s --stream <host:port>     Stream the camera over HTTP listening on host and port [default: localhost:8080]
    -w --window                 Watch the camera stream and detected motion in a window

Movement detection:
    --threshold <rate>          Per pixel change rate to consider a pixel as changed [default: 0.1]
    --sensitivity <rate>        Overall pixel change rate to consider that there has been movement [default: 0.1]

Event recording:
    --before <frames>           Frame quantity to record before movement is detected [default: 10]
    --after <frames>            Frame quantity to record after movement is detected [default: 10]

Other:
    -v --verbose                Verbose debug output
"""

import logging
import signal
import os
from docopt import docopt
from multiprocessing import Process
from purl import URL
from time import sleep

from lightweightmotion.config import ArgsConfig, FileConfig
from lightweightmotion.camera import FoscamHTTPCamera, USBCamera
from lightweightmotion.outputs import EventDirectory, HTTPStream, Window


class Command(object):
    def __init__(self, args):
        signal.signal(signal.SIGTERM, self.stop)
        self.processes = []
        config_file = args['<config_file>']
        if config_file:
            self.config = FileConfig(config_file)
        else:
            self.config = ArgsConfig(args)

    def setup_logging(self):
        level = logging.ERROR
        if self.config.DEBUG:
            level = logging.DEBUG
        logging.basicConfig(level=level)

    def get_camera(self):
        if self.config.URL:
            url = URL(self.config.URL)
            auth = url.username(), url.password()
            if url.username is None and url.password is None:
                auth = None
            url = URL(url.as_string(), username='', password='')
            return FoscamHTTPCamera(url.as_string(), auth)
        else:
            return USBCamera(self.config.DEVICE)

    def get_outputs(self, camera):
        outputs = []

        if self.config.EVENT_DIR:
            events = camera.events(
                    self.config.MOVEMENT_THRESHOLD,
                    self.config.MOVEMENT_SENSITIVITY,
                    self.config.EVENT_BEFORE, self.config.EVENT_AFTER)
            outputs.append(EventDirectory(events, self.config.EVENT_DIR))

        if self.config.STREAM:
            frames = camera.watch(
                    self.config.MOVEMENT_THRESHOLD,
                    self.config.MOVEMENT_SENSITIVITY)
            outputs.append(HTTPStream(frames, *self.config.STREAM))

        if self.config.WINDOW:
            frames = camera.watch(
                    self.config.MOVEMENT_THRESHOLD,
                    self.config.MOVEMENT_SENSITIVITY)
            outputs.append(Window(frames))

        return outputs

    def run(self):
        self.setup_logging()
        with self.get_camera() as camera:
            outputs = self.get_outputs(camera)

            for output in outputs:
                process = Process(target=output.run)
                process.daemon = True
                process.start()
                self.processes.append(process)

            self.running = True
            try:
                while self.running:
                    sleep(1)
            except KeyboardInterrupt:
                self.stop()

    def stop(self, signal=None, frame=None):
        for process in self.processes:
            process.terminate()
            os.kill(process.pid, 9)
        self.running = False


def main():
    args = docopt(__doc__, version='0.1')
    command = Command(args)
    command.run()

if __name__ == '__main__':
    main()
