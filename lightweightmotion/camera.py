import logging
import re
import requests
import cv2
from operator import sub
from itertools import chain


class Camera(object):
    def __init__(self):
        self.width, self.height, depth = next(self.frames()).shape
        logging.info('First frame gathered successfully')
        logging.debug('Device width: {} Device height: {}'.format(
            self.width, self.height))

    def frames(self):
        raise NotImplemented()

    def motion(self, threshold, sensitivity, stretch=0):
        while True:
            for frame in self.event(threshold, sensitivity, stretch):
                logging.debug('Motion detected')
                yield frame

    def events(self, threshold, sensitivity, stretch=0):
        while True:
            event = self.event(threshold, sensitivity, stretch)
            try:
                first_frame = next(event)
            except StopIteration:
                pass
            else:
                event = chain([first_frame], self.event(threshold, sensitivity, stretch))
                logging.info('New motion event')
                yield event

    def event(self, threshold, sensitivity, stretch=0):
        frames = self.frames()
        prev_frame = next(frames)
        from_last = 0
        for frame in frames:
            if from_last > 0:
                from_last -= 1
                yield frame
            elif self.has_changed(prev_frame, frame, threshold, sensitivity):
                from_last = stretch
                initial = False
                yield frame
            else:
                raise StopIteration()
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
