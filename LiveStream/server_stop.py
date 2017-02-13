import threading
import SocketServer
import cv2
import numpy as np
import math
stop_cascade = cv2.CascadeClassifier('stop_sign.xml')


class VideoStreamHandler(SocketServer.StreamRequestHandler):

    def handle(self):

        stream_bytes = ' '
        a = 1
        try:
            while True:
                stream_bytes += self.rfile.read(1024)
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype="uint8"), 1)

                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    signs = stop_cascade.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in signs:
                        cv2.rectangle(
                            image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        roi_gray = gray[y:y + h, x:x + w]
                        roi_color = image[y:y + h, x:x + w]
                        # print('stop :' + str(a))

                        # print "w : " + str(w)+ "h: " +str(h)
                        if (w > 120):
                            print ("Stop the bot : ") + str(a)
                            a = a + 1
#                    cv2.imshow('image', image)
                    cv2.waitKey(30)
        finally:
            print ("Connection closed on thread 1")


def server_thread(host, port):
    server = SocketServer.TCPServer((host, port), VideoStreamHandler)
    server.serve_forever()

video_thread = threading.Thread(target=server_thread('192.168.43.232', 8001))
video_thread.start()
