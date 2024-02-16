# This is an example python actor
#
# Make sure the class name matches the filename! (without the .py file extension)


import sys 
import cv2
import time
from datetime import datetime
import struct
from pythonosc.osc_message_builder import OscMessageBuilder
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import numpy as np

VisionRunningMode = mp.tasks.vision.RunningMode

# mediapipe 0.10 on python 3.9 on osx: https://github.com/google/mediapipe/issues/4512 / https://github.com/AnyLifeZLB/FaceVerificationSDK/blob/main/install_newest_mediapipe_on_macos.md

class skeletonActor(object):
    def __init__(self, *args, **kwargs):
        self.cap = cv2.VideoCapture(0)
        self.timeout = 50        # Use this timeout value for when you need recurring handleTimer events
                                    # Set to -1 to wait infinite (default)
        self.count = 0;
        
        base_options = python.BaseOptions(model_asset_path='pose_landmarker.task')
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=VisionRunningMode.VIDEO,
            output_segmentation_masks=True,num_poses=1,
            min_pose_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.detector = vision.PoseLandmarker.create_from_options(options)

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
            
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
           
            # Timestemp
            # https://mediapipe.readthedocs.io/en/latest/getting_started/python_framework.html
            # https://github.com/google/mediapipe/blob/master/mediapipe/framework/timestamp.h
            # The documentation suggets to use: mp.Timestamp.from_seconds(time.time()).value
            # but we use a simple coutner otherwise we get the error/warning: 
            # one_euro_filter.cc:31] New timestamp is equal or less than the last one.
            detection_result = self.detector.detect_for_video(mp_image, mp.Timestamp.from_seconds(self.count).value)
            #detection_result = self.detector.detect_async(mp_image, mp.Timestamp.from_seconds(time.time()).value)
            

            # check if we have landmarks
            if detection_result.pose_landmarks and len(detection_result.pose_landmarks):

                # Each pose has 32 landmarks with normalized x/y/z/visiblilty
                m = OscMessageBuilder("/pose")

                # Loop through The poses (in settings right no limit is 1)
                for pose_id, pose in enumerate(detection_result.pose_landmarks):
                    #print(f"Pose {pose_id}: ({pose})")
                    # Loop through the landmarks
                    for landmark_id, landmark in enumerate(pose):
                        #print(f"Landmark {landmark_id + 1}:")
                        '''
                        print(f"  x: {landmark2.x}")
                        print(f"  y: {landmark2.y}")
                        print(f"  z: {landmark2.z}")
                        print(f"  Visibility: {landmark2.visibility}")
                        print(f"  Presence: {landmark2.presence}")
                        print()
                        '''
                        m.add_arg(landmark_id)
                        m.add_arg(landmark.x)
                        m.add_arg(landmark.y)
                        m.add_arg(landmark.z)
                        m.add_arg(landmark.visibility)
               
                # set timeout to 0 to go as quick as possible if there is data
                self.timeout = 0   

                self.count += 1

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
    OSCport = 6200
    OSCaddress = '127.0.0.1'
    #client = udp_client.SimpleUDPClient(OSCaddress, OSCport) # local debug 
    client = udp_client.UDPClient(OSCaddress, OSCport) # local debug 

    sk = skeletonActor()
    while True:
        ts = time.time()
        oscM = sk.handleTimer()
       
        # send over OSC
        if oscM:
            client.send(oscM)

