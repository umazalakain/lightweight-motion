"""lightweight-motion

Lightweight motion detection, ready for your RPY!

Usage:
    lightweight-motion [options] usb <device> (-o <output-dir>|-w)
    lightweight-motion [options] foscam <url> (-o <output-dir>|-w)
    lightweight-motion (-h | --help)
    lightweight-motion --version

Arguments:
    <device>                    Input video device ID (normally 0)
    <url>                       Input video device url (ex: http://your.cam/videostream.cgi)

Options:
    -o --output <output-dir>    Output directory for recorded events
    -w --watch                  Watch the camera stream and detected motion in realtime
    -u --user <user>            HTTP basic auth user
    -p --password <password>    HTTP basic auth password
    --threshold <rate>          Per pixel change rate to consider a pixel as changed [default: 0.1]
    --sensitivity <rate>        Overall pixel change rate to consider that there has been movement [default: 0.1]
    --before <frames>           Frame quantity to record before movement is detected [default: 10]
    --after <frames>            Frame quantity to record after movement is detected [default: 10]
    -v --verbose                Verbose debug output
"""

import cv2
import logging
from docopt import docopt

from lightweightmotion.camera import FoscamHTTPCamera, USBCamera
from lightweightmotion.environment import Environment


def command(args):
    if args['--verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.ERROR)

    if args['usb']:
        device = int(args['<device>'])
        camera = USBCamera(device)

    elif args['foscam']:
        url = args['<url>']
        user = args['--user']
        password = args['--password']
        auth = (user, password)
        if user is None and password is None:
            auth = None
        camera = FoscamHTTPCamera(url, auth)

    threshold = float(args['--threshold'])
    sensitivity = float(args['--sensitivity'])

    if args['--output']:
        before = int(args['--before'])
        after = int(args['--after'])
        environment = Environment(args['--output'])
        for event in camera.events(threshold, sensitivity, before, after):
            environment.save_event(event)

    elif args['--watch']:
        for frame in camera.watch(threshold, sensitivity):
            cv2.imshow('camera', frame)
            if cv2.waitKey(5)==27:
                break


def main():
    args = docopt(__doc__, version='0.1')
    command(args)

if __name__ == '__main__':
    main()
