import cv2
import Image
import numpy
from operator import sub


class Camera(object):
    def frames(self):
        raise NotImplemented()

    def motion(self, threshold, sensitivity, stretch=0):
        frames = self.frames()
        prev_frame = next(frames)
        from_last = 0
        for frame in frames:
            if from_last > 0:
                from_last -= 1
                yield frame
            else:
                changed_pixels = self.changed_pixels(prev_frame, frame, threshold)
                if changed_pixels > sensitivity:
                    from_last = stretch
                    yield frame
            prev_frame = frame

    def changed_pixels(self, prev_frame, next_frame, threshold):
        width, height = prev_frame.size
        buffers = prev_frame.load(), next_frame.load()
        changed_pixels = 0
        for x in xrange(width):
            for y in xrange(height):
                pixels = ( b[x,y][1] for b in buffers )
                if abs(sub(*pixels)) > threshold:
                    changed_pixels += 1
        return changed_pixels


class HTTPCamera(Camera):
    def __init__(self, host, port, path, user, password):
        pass

    def frames(self):
        while True:
            yield


class USBCamera(Camera):
    def __init__(self, device):
        self.capture = cv2.VideoCapture(device)

    def frames(self):
        while True:
            _, f = self.capture.read()
            yield Image.fromarray(numpy.uint8(f))
