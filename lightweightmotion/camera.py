from __future__ import division
import numpy as np
import logging
import re
import requests
import cv2
from operator import sub
from collections import deque
from itertools import takewhile, islice, chain


class Camera(object):
    def __init__(self):
        self._frames = None

    def __enter__(self):
        self.height, self.width, depth = next(self.frames()).shape
        self.resolution = self.height * self.width
        logging.info('First frame gathered successfully')
        logging.debug('Device width: {} Device height: {}'.format(
            self.width, self.height))
        return self

    def __exit__(self, type, value, traceback):
        pass

    def frames(self):
        if self._frames is None:
            self._frames = self.get_frames()
        return self._frames

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
            logging.info('New event detected')
            yield event

    def watch(self, threshold, sensitivity):
        radius = min(self.width, self.height) // 20
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
        # get the absolute diff between the two frames
        changed = cv2.absdiff(prev_frame, next_frame)
        # get the rgb mean value
        changed = np.mean(changed, 2)
        # count the pixels that are greather than the threshold
        changed = len(changed[changed > threshold*255])
        # compute the change rate
        change_rate = changed / self.resolution
        logging.debug('{} pixels changed ({}/1)'.format(changed, change_rate))
        if change_rate > sensitivity:
            logging.info('Motion detected')
            return True
        return False


class HTTPCamera(Camera):
    """Reads frames from HTTP and reconnects constantly."""
    chunk_size = 1024

    def __init__(self, url, auth=None):
        self.url = url
        self.auth = auth
        super(HTTPCamera, self).__init__()

    def __enter__(self):
        self.capture = self.get_camera()
        logging.info('HTTP camera opened at {}'.format(self.url))
        return super(HTTPCamera, self).__enter__()

    def __exit__(self, type, value, traceback):
        self.capture.close()

    def get_camera(self, retry=True):
        """
        Reconnects with remote HTTP cam. If retry, blocks until connected.
        """
        while True:
            try:
                return requests.get(self.url, auth=self.auth, stream=True)
            except requests.exceptions.ConnectionError:
                if not retry:
                    raise

    def get_frames(self):
        """
        Frame generator that reconnects endlessly to the remote cam.
        Chunks are accumulated until a full frame is constructed, the frame is
        loaded into a np array and decoded by OpenCV.
        """
        while True:
            buffer = ''
            for chunk in self.capture.iter_content(self.chunk_size):
                buffer += chunk
                frames = self.split_content(buffer)
                frames, buffer = frames[:-1], frames[-1]
                for frame in frames:
                    frame = np.fromstring(frame, dtype='uint8')
                    frame = cv2.imdecode(frame, 1)
                    if frame is not None:
                        yield frame
            self.capture = self.get_camera()

    def split_content(self, buffer):
        raise NotImplemented()


class FoscamHTTPCamera(HTTPCamera):
    separator = re.compile('--ipcamera\r\nContent-Type: image/jpeg\r\n'
                            'Content-Length: \d+?\r\n\r\n')

    def split_content(self, buffer):
        return self.separator.split(buffer)


class USBCamera(Camera):
    """Reads frames from a local USB device."""

    def __init__(self, device_idx=None):
        self.idx = device_idx
        super(USBCamera, self).__init__()

    def __enter__(self):
        self.capture, self.idx = self.get_camera(self.idx)
        logging.info('USB camera {} opened'.format(self.idx))
        return super(USBCamera, self).__enter__()

    def __exit__(self, type, value, traceback):
        self.capture.release()

    def get_frames(self):
        """Frame generator."""
        while True:
            _, frame = self.capture.read()
            yield frame

    def get_camera(self, device_idx=None):
        """
        Get the camera if only one, raise an exception otherwise.
        """
        if device_idx is None:
            cameras = list(self.get_connected_cameras())
            if len(cameras) == 1:
                return cameras[0]
            else:
                indexes = ', '.join([ str(idx) for cam, idx in cameras ])
                raise OSError('Multiple cameras: {}'.format(indexes))
        else:
            return cv2.VideoCapture(device_idx), device_idx

    def get_connected_cameras(self):
        """
        Iterator of connected cameras.
        Returns (cv2.VideoCapture, camera_index) tuples.
        """
        for idx in range(10):
            camera = cv2.VideoCapture(idx)
            if camera.isOpened():
                yield camera, idx
