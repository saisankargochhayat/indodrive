"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
import picamera
import cv2
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')
a = 1
# create socket and bind host
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.100', 8000))
connection = client_socket.makefile('wb')


try:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)      # pi camera resolution
        camera.framerate = 10               # 10 frames/sec
        # give 2 secs for camera to initilize
        time.sleep(2)
        start = time.time()
        stream = io.BytesIO()

        # send jpeg format video stream
        for foo in camera.capture_continuous(stream, 'bgr', use_video_port=True):
            image = foo.array
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            signs = stop_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in signs:
                print('stop ', w)
                a = a + 1
            connection.write(struct.pack('<L', stream.tell()))
            connection.flush()
            stream.seek(0)
            connection.write(stream.read())
            if time.time() - start > 600:
                break
            stream.seek(0)
            stream.truncate()
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()
