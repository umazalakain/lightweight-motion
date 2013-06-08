"""lightweight-motion

Lightweight motion detection, ready for your RPY!

Usage:
    lightweight-motion [options] usb <device> <output-directory>
    lightweight-motion [options] foscam <url> <output-directory>
    lightweight-motion (-h | --help)
    lightweight-motion --version

Arguments:
    <device>                    Input video device ID (normally 0)
    <url>                       Input video device url (like http://your.cam/videostream.cgi)
    <output-directory>          Directory in witch to output events

Options:
    -u --user <user>            HTTP basic auth user
    -p --password <password>    HTTP basic auth password
    --threshold <rate>          Per pixel change rate to consider a pixel as changed [default: 0.05]
    --sensitivity <rate>        Overall pixel change rate to consider that there has been movement [default: 0.05]
    --stretch <seconds>         How much to time to stretch from last event deactivation [default: 10]
    -v --verbose                Verbose debug output
"""

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

    environment = Environment(args['<output-directory>'])
    threshold = float(args['--threshold'])
    sensitivity = float(args['--sensitivity'])
    stretch = int(args['--stretch'])

    for event in camera.events(threshold, sensitivity, stretch):
        environment.save_event(event)


def main():
    args = docopt(__doc__, version='0.1')
    command(args)

if __name__ == '__main__':
    main()
