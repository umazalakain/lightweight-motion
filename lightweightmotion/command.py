"""lightweight-motion

Lightweight motion detection, ready for your RPY!

Usage:
    lightweight-motion [options] usb <device> [--directory <output-dir>] [--stream <host:port>] [--window]
    lightweight-motion [options] foscam <url> [--directory <output-dir>] [--stream <host:port>] [--window]
    lightweight-motion (-h | --help)
    lightweight-motion --version

Arguments:
    <device>                    Input video device ID (normally 0)
    <url>                       Input video device url (ex: http://your.cam/videostream.cgi)

Inputs:
    -u --user <user>            HTTP basic auth user
    -p --password <password>    HTTP basic auth password

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

from lightweightmotion.camera import FoscamHTTPCamera, USBCamera
from lightweightmotion.outputs import EventDirectory, HTTPStream, Window


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

    outputs = []

    if args['--directory']:
        before = int(args['--before'])
        after = int(args['--after'])
        events = camera.events(threshold, sensitivity, before, after)
        outputs.append(EventDirectory(events, args['--directory']))

    if args['--stream']:
        host, port = args['--stream'].split(':')
        port = int(port)
        frames = camera.frames()
        outputs.append(HTTPStream(frames, host, port))

    if args['--window']:
        frames = camera.frames()
        outputs.append(Window(frames))

    for output in outputs:
        process = Process(target=output.run)
        process.start()


def main():
    args = docopt(__doc__, version='0.1')
    command(args)

if __name__ == '__main__':
    main()
