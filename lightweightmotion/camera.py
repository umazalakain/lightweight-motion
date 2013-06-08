import Image
import numpy
import requests
import re
from operator import sub
from StringIO import StringIO
from itertools import chain


class Camera(object):
    def __init__(self):
        self.width, self.height = next(self.frames()).size

    def frames(self):
        raise NotImplemented()

    def motion(self, threshold, sensitivity, stretch=0):
        while True:
            for frame in self.event(threshold, sensitivity, stretch):
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
        buffers = prev_frame.load(), next_frame.load()
        changed_pixels = 0
        for x in xrange(self.width):
            for y in xrange(self.height):
                # only compare the green channel
                pixels = ( b[x,y][1] for b in buffers )
                if abs(sub(*pixels)) > threshold:
                    changed_pixels += 1
                    if changed_pixels > sensitivity:
                        return True
        return False


class HTTPCamera(Camera):
    chunk_size = 1024

    def __init__(self, url, auth=None):
        self.capture = requests.get(url, auth=auth, stream=True)
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
                        yield Image.open(StringIO(frame))
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
        import cv2
        self.capture = cv2.VideoCapture(device)
        super(USBCamera, self).__init__()

    def frames(self):
        while True:
            _, f = self.capture.read()
            yield Image.fromarray(numpy.uint8(f))
