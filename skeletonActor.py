# This is an example python actor
#
# Make sure the class name matches the filename! (without the .py file extension)


import sys 
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


class skeletonActor(object):
    def __init__(self, *args, **kwargs):
        self.cap = cv2.VideoCapture(0)
        self.timeout = 50        # Use this timeout value for when you need recurring handleTimer events
                                    # Set to -1 to wait infinite (default)
        self.pose = mp_pose.Pose( min_detection_confidence=0.5, min_tracking_confidence=0.5)

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
            results = self.pose.process(image)

            # check if we have landmarks
            # This if statement is not so relaible
            #if len(results.pose_landmarks.landmark) != 0:
            if results.pose_landmarks and len(results.pose_landmarks.landmark):

                # Each pose has 32 landmarks with normalized x/y/z/visiblilty
                poseCoords = []
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    #print(id,lm)
                    poseCoords.append(id)
                    poseCoords.append(lm.x)
                    poseCoords.append(lm.y)
                    poseCoords.append(lm.z)
                    poseCoords.append(lm.visibility)

                # set timeout to 0 to go as quick as possible if there is data
                self.timeout = 0   

                # send over OSC
                return ("/pose", poseCoords)

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

if __name__ == "__main__":
    import time
    from pythonosc import udp_client

    # Create OSC client
    OSCport = 6200
    OSCaddress = '127.0.0.1'
    client = udp_client.SimpleUDPClient(OSCaddress, OSCport) # local debug 

    sk = skeletonActor()
    while True:
        ts = time.time()
        oscM = sk.handleTimer()
        #print(oscM)

        timeEnd = time.time()
        dur = timeEnd - ts
        print(dur)
        # send over OSC
        if oscM:
            client.send_message(oscM[0], oscM[1])

        #time.sleep(sk.timeout/1000.)

