# PoseTrackActor

This repo contains skeletonActor.py flie which can be uses to run in Gazebo as Actor. poseTrack.gzs is a simple stage in which the actor is implemented.

## Mediapipe
This actor uses the [mediapipe library](https://developers.google.com/mediapipe) So you need to refrence to where this library is installed on your system. We advise to use a Python virtual environment for this. See for more information about Python virtual environment [here](https://docs.python.org/3/library/venv.html)

You can then reference to the library at the beginning of the python script as follows:

```
import sys 
sys.path.append("path_to_venv/lib/python3.11/site-packages")
```

### OSC message structure

The OSC message send out by the skeletonActor starts with the label "/pose".
The message has a length of 165 values and consists of 32 landmarks. For eacht landmark thes message structure is "hdddd" meaning one value of type long and four values of type double. These represent the ID of the landmark, the x position, the y position, the z position and the visibility. 

So the format is:

	h, d, d, d, d
	id, x, y, z, visibility

#### The landmark IDs:

0 - nose
1 - left eye (inner)
2 - left eye
3 - left eye (outer)
4 - right eye (inner)
5 - right eye
6 - right eye (outer)
7 - left ear
8 - right ear
9 - mouth (left)
10 - mouth (right)
11 - left shoulder
12 - right shoulder
13 - left elbow
14 - right elbow
15 - left wrist
16 - right wrist
17 - left pinky
18 - right pinky
19 - left index
20 - right index
21 - left thumb
22 - right thumb
23 - left hip
24 - right hip
25 - left knee
26 - right knee
27 - left ankle
28 - right ankle
29 - left heel
30 - right heel
31 - left foot index
32 - right foot index

Landmark image

![Landmark](img/pose_landmarks_index.png)


Source: [link](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)

## Processing

![Screenshot](img/screenshot01.png)


In the processing directory you can find oscRecieveGazeboPose which parses the OSC data send out by the pyhton actor to visualise the data.


