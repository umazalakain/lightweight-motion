import logging
import re
import requests
import cv2
from operator import sub
from collections import deque
from itertools import takewhile, islice, chain


class Camera(object):
    def __init__(self):
        self.height, self.width, depth = next(self.frames()).shape
        logging.info('First frame gathered successfully')
        logging.debug('Device width: {} Device height: {}'.format(
            self.width, self.height))

    def frames(self):
        raise NotImplemented()

    def filter(self, threshold, sensitivity):
        for frame, moved in self.detect(threshold, sensitivity):
            if moved:
                yield frame

    def events(self, threshold, sensitivity, b_frames=0, a_frames=0):
        detected = self.detect(threshold, sensitivity)
        while True:
            # store the latest non-motion frames in a fixed-length queue
            before = takewhile(lambda e: not e[1], detected)
            before = iter(deque(before, b_frames))
            # get the actual motion
            motion = takewhile(lambda e: e[1], detected)
            # get some more frames
            after = islice(detected, a_frames)
            # chain it all
            event = chain(before, motion, after)
            # get only the actual frames
            event = ( e[0] for e in event )
            yield event

    def watch(self, threshold, sensitivity):
        radius = min(self.width, self.height) / 20
        position = (self.width-radius, radius)
        for frame, motion in self.detect(threshold, sensitivity):
            if motion:
                frame = frame.copy()
                cv2.circle(frame, position, radius, (0, 0, 255), -1)
            yield frame

    def detect(self, threshold, sensitivity):
        frames = self.frames()
        prev_frame = next(frames)
        for frame in frames:
            changed = self.has_changed(prev_frame, frame, threshold, sensitivity)
            yield (frame, changed)
            prev_frame = frame

    def has_changed(self, prev_frame, next_frame, threshold, sensitivity):
        threshold *= 255
        sensitivity *= (self.width * self.height)
        difference = cv2.absdiff(prev_frame, next_frame).flatten()
        difference = difference[difference>threshold]
        return len(difference) > sensitivity



class HTTPCamera(Camera):
    chunk_size = 1024

    def __init__(self, url, auth=None):
        self.capture = requests.get(url, auth=auth, stream=True)
        logging.info('HTTP camera opened at {}'.format(url))
        super(HTTPCamera, self).__init__()

    def frames(self):
        buffer = ''
        while True:
            buffer += self.capture.iter_content(self.chunk_size)
            frames = self.split_content(buffer)
            frames, buffer = frames[:-1], frames[-1]
            for frame in frames:
                if frame:
                    try:
                        yield cv2.decode(frame)
                    except IOError:
                        pass

    def split_content(self, buffer):
        raise NotImplemented()


class FoscamHTTPCamera(HTTPCamera):
    separator = re.compile('--ipcamera\r\nContent-Type: image/jpeg\r\n'
                            'Content-Length: \d+?\r\n\r\n')

    def split_content(self, buffer):
        return self.separator.split(buffer)


class USBCamera(Camera):
    def __init__(self, device):
        self.capture = cv2.VideoCapture(device)
        logging.info('USB camera opened at {}'.format(device))
        super(USBCamera, self).__init__()

    def frames(self):
        while True:
            _, frame = self.capture.read()
            yield frame
