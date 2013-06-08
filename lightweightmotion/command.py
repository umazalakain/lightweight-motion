"""lightweight-motion

Lightweight motion detection, ready for your RPY!

Usage:
    lightweightmotion [options] usb <device> <output-directory>
    lightweightmotion [options] http <url> <output-directory> [--type=<type>]
    lightweightmotion (-h | --help)
    lightweightmotion --version

Arguments:
    <device>                    Input video device ID (normally 0)
    <url>                       Input video device url (like http://your.cam/videostream.cgi)
    <output-directory>          Directory in witch to output events

Options:
    -t --type (foscam)          HTTP camera type [default: foscam]
    -u --user <user>            HTTP basic auth user
    -p --password <password>    HTTP basic auth password
    --threshold <rate>          Difference to consider a pixel as changed [default: 0.2]
    --sensitivity <rate>        Quantity of pixels to consider that there has been movement [default: 0.2]
    --stretch <seconds>         [default: 10]
"""

from docopt import docopt

from lightweightmotion.camera import FoscamHTTPCamera, USBCamera
from lightweightmotion.environment import Environment


def command(args):
    if args['usb']:
        device = int(args['<device>'])
        camera = USBCamera(device)

    elif args['http']:
        url = args['<url>']
        user = args['--user']
        password = args['--password']
        if args['--type'] == 'foscam':
            HTTPCamera = FoscamHTTPCamera
        camera = HTTPCamera(url, user, password)

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
