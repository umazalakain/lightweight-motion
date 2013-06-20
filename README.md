lightweight-motion
==================

Lightweight RPY-ready motion detection for USB and HTTP(S) cameras!


    Usage:
        lightweight-motion [options] usb <device> [--directory <output-dir>] [--window] [--stream]
        lightweight-motion [options] foscam <url> [--directory <output-dir>] [--window] [--stream]
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
        -w --window                 Watch the camera stream and detected motion in a window
        -s --stream                 Stream the camera over HTTP

    Movement detection:
        --threshold <rate>          Per pixel change rate to consider a pixel as changed [default: 0.1]
        --sensitivity <rate>        Overall pixel change rate to consider that there has been movement [default: 0.1]

    Event recording:
        --before <frames>           Frame quantity to record before movement is detected [default: 10]
        --after <frames>            Frame quantity to record after movement is detected [default: 10]
