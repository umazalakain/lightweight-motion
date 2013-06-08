lightweight-motion
==================

Lightweight RPY-ready motion detection for USB and HTTP(S) cameras!


    Usage:
        lightweight-motion [options] usb <device> <output-directory>
        lightweight-motion [options] http <url> <output-directory> [--type=<type>]
        lightweight-motion (-h | --help)
        lightweight-motion --version

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
