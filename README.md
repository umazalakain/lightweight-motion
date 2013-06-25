lightweight-motion
==================

Lightweight RPY-ready motion detection for USB and HTTP(S) cameras!


    Usage:
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
