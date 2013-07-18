lightweight-motion
==================

**Lightweight RPY-ready motion detection for USB and HTTP(S) cameras!**


Command line execution
-----------------------

::

    Usage:
        lightweight-motion -c <config_file>
        lightweight-motion [options] <device> [-d <output-dir>] [-s <host:port>] [-w]
        lightweight-motion [options] <url> [-d <output-dir>] [-s <host:port>] [-w]
        lightweight-motion (-h | --help)
        lightweight-motion --version

    Arguments:
        <device>                    Input video device ID (normally 0)
        <url>                       Input video device url (ex: http://user:pass@host/path)

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


Config file syntax
------------------


.. code:: python
    

    # one of the following two must be defined
    DEVICE = 0
    URL = 'http://user:password@host/path'

    # movement detection parameters
    MOVEMENT_THRESHOLD = 0.07
    MOVEMENT_SENSITIVITY = 0.04

    # stream output on HTTP
    STREAM = 'host:port' # None

    # show output in a window
    WINDOW = True # None

    # save movement events in a dir
    EVENT_DIR = 'output' # None

    # frames to save before event takes place
    EVENT_BEFORE = 100

    # frames to save after event takes place
    EVENT_AFTER = 10

    # verbose debug output
    DEBUG = True # False


Requirements
------------

In addition to the requirements denoted in `setup.py`, lightweight-motion requires OpenCV 2.x. If you plan to make use of HTTP cameras, you need OpenCV 2.4 or higher. You can currently find it in debians experimental repos. Sadly, if you are on a Raspberry Pi, you need to `compile it yourself <http://mitchtech.net/raspberry-pi-opencv/>`_.


Note
----

    Currently, the generated output frame stream is split by the active outputs. If HTTP stream, window and event recording outputs are active, each of them will only receive one third of the frames. Because of that, it's strongly encouraged to only use one output.
