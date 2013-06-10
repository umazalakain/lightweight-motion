lightweight-motion
==================

Lightweight RPY-ready motion detection for USB and HTTP(S) cameras!


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
        --threshold <rate>          Per pixel change rate to consider a pixel as changed [default: 0.1]
        --sensitivity <rate>        Overall pixel change rate to consider that there has been movement [default: 0.1]
        --before <frames>           Frame quantity to record before movement is detected [default: 10]
        --after <frames>            Frame quantity to record after movement is detected [default: 10]
        -v --verbose                Verbose debug output
