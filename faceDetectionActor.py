# This is an facedetection with Meidapipe python actor
#
# Make sure the class name matches the filename! (without the .py file extension)
# https://medium.com/mlearning-ai/detecting-face-at-30-fps-on-cpu-on-mediapipe-python-dda264e26f20

import sys 
import cv2
import struct
from pythonosc.osc_message_builder import OscMessageBuilder
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

mp_face_detection = mp.solutions.face_detection

'''
    Facedetection OSC message structure
    label: /face
    arguments:
    0: float: boundingbox xmin
    1: float: boundingbox ymin
    2: float: boundingbox width
    3: float: boundingbox height
    4: float: right eye x
    5: float: right eye y
    6: float: left eye x
    7: float: left eye y
    8: float: nose x
    9: float: nose y
    10: float: mouth x
    11: float: mouth y
    12: flaot right ear x
    13: flaot right ear y
    14: flaot left ear x
    15: flaot left ear y


'''

class faceDetectionActor(object):
    def __init__(self, *args, **kwargs):
        self.cap = cv2.VideoCapture(0)
        self.timeout = 50        # Use this timeout value for when you need recurring handleTimer events
                                    # Set to -1 to wait infinite (default)
        
        self.detector = mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) 

    def handleApi(self, command, *args, **kwargs):
        print("The API command is {} and its arguments is {}".format(command, args))
        return None

    def handleSocket(self, address, data, *args, **kwargs):
        print("The osc address is {} and its data is {}".format(address, data))
        return ("/myreturnaddress", ["hello", 3, 2, 1])

    def handleTimer(self, *args, **kwargs):
        # This is a timed event, use it as you need
        #with mp_pose.Pose( min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        if ( self.cap.isOpened() ):
            success, image = self.cap.read()
            if not success:
              print("Ignoring empty camera frame.")
              # If loading a video, use 'break' instead of 'continue'.
              return None

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.detector.process(image)

            if results.detections:
                '''
                for face in results.detections:
                    data = face.location_data
                    bbox = data.relative_bounding_box
                    print(bbox)
                '''
                # FOR NOW We JUST tAKE THE FIRST FACE
                face = results.detections[0]
                data = face.location_data
                bbox = data.relative_bounding_box
                
                m = OscMessageBuilder("/face")
                m.add_arg(bbox.xmin)
                m.add_arg(bbox.ymin)
                m.add_arg(bbox.width)
                m.add_arg(bbox.height)

                for id,lm in enumerate(data.relative_keypoints):
                    m.add_arg(lm.x)
                    m.add_arg(lm.y)

                # set timeout to 0 to go as quick as possible if there is data
                self.timeout = 0   

                # Run from Main
                if __name__ == '__main__':
                    return m.build()
                # Run from gazebo
                else:
                    return m.build().dgram

        # take it easy because we have nothing to do.
        self.timeout = 50
        return None

    def handleCustomSocket(self, *args, **kwargs):
        # We'll explain this in the future
        return ("/myreturnaddress", ["hello", "world"])

    def handleStop(self, *args, **kwargs):
        # We are shutting down
        self.cap.release()
        print("Bye bye from {}".format(args[1]))


# is only used when tunning stand alone
# meaning outside of gazebo
if __name__ == "__main__":
    import time
    from pythonosc import udp_client

    # Create OSC client
    OSCport = 1234
    OSCaddress = '127.0.0.1'
    #client = udp_client.SimpleUDPClient(OSCaddress, OSCport) # local debug 
    client = udp_client.UDPClient(OSCaddress, OSCport) # local debug 

    fd = faceDetectionActor()
    while True:
        ts = time.time()
        fd = faceDetectionActor()
        oscM = fd.handleTimer()

        # send over OSC
        if oscM:
            client.send(oscM)
    

