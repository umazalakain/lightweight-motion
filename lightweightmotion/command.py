"""lightweight-motion

Lightweight motion detection, ready for your RPY!

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
from docopt import docopt
from multiprocessing import Process
from purl import URL

from lightweightmotion.config import ArgsConfig, FileConfig
from lightweightmotion.camera import FoscamHTTPCamera, USBCamera
from lightweightmotion.outputs import EventDirectory, HTTPStream, Window


def command(args):
    config_file = args['<config_file>']
    if config_file:
        config = FileConfig(config_file)
    else:
        config = ArgsConfig(args)

    level = logging.ERROR
    if config.DEBUG:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    if config.URL:
        url = URL(config.URL)
        auth = url.username(), url.password()
        if url.username is None and url.password is None:
            auth = None
        url = URL(url.as_string(), username='', password='')
        camera = FoscamHTTPCamera(url.as_string(), auth)
    else:
        camera = USBCamera(config.DEVICE)

    outputs = []

    if config.EVENT_DIR:
        events = camera.events(
                config.MOVEMENT_THRESHOLD, 
                config.MOVEMENT_SENSITIVITY,
                config.EVENT_BEFORE, config.EVENT_AFTER)
        outputs.append(EventDirectory(events, config.EVENT_DIR))

    if config.STREAM:
        frames = camera.watch(
                config.MOVEMENT_THRESHOLD, 
                config.MOVEMENT_SENSITIVITY)
        outputs.append(HTTPStream(frames, *config.STREAM))

    if config.WINDOW:
        frames = camera.watch(
                config.MOVEMENT_THRESHOLD, 
                config.MOVEMENT_SENSITIVITY)
        outputs.append(Window(frames))

    for output in outputs:
        process = Process(target=output.run)
        process.start()


def main():
    args = docopt(__doc__, version='0.1')
    command(args)

if __name__ == '__main__':
    main()
