
# GazeboOsc Mediapipe Python actors

This repo contains Gazebosc Python actors you can run from Gazebosc to use Mediapipe functionlaity such as:  
- pose tracking 
- face tracking

### Mediapipe
This actor uses the [mediapipe library](https://developers.google.com/mediapipe) So you need to refrence to where this library is installed on your system. We advise to use a Python virtual environment for this. See for more information about Python virtual environment [here](https://docs.python.org/3/library/venv.html)

## Getting Started

### Install Gazebo
To install Gazebo on your computer go here: 
https://pong.hku.nl/~buildbot/gazebosc/

Click on "Last modified" to sort the files on date and download the last version of Gazebo for your computer Windows/OSX/Linux.

### Install Mediapipe Python actors

#### Download the actors
- Switch to branch mediapip0.10.9
- Download this repo by clicking on "<> Code" and then "Download Zip"
- Unzip the zip

#### Install python virtual environment with Mediapipe
To use the mediapipe actors you first need to install a Python Virtual Environment where you then install mediapipe.

Open a terminal and use the Python included with Gazebo to make a python virtual environment somewhere on your computer. This means you first need the path to the Python excecutable inside of Gazebo.  

**Attention when doing this on macOS first do this in the terminal**  
`export SYSTEM_VERSION_COMPAT=0`

Read [here](https://github.com/AnyLifeZLB/FaceVerificationSDK/blob/main/install_newest_mediapipe_on_macos.md) why.
1. Open a terminal and go to the directory where you want to install the Python vVirtual environment
*for example:*
`cd ~/Documents/`

2. Make a Python Virtual Environment (Following is a example for macOS):  
`/Applications/gazebosc.app/Contents/Resources/python/bin/python3.9 -m venv myvenv`  

3. Then activate the python virutal environment:  
`source myvenv/bin/activate`  

5. Go to the Mediapipe actors folder in the terminal:  
*(your path might be different)*  
`cd Documents/PoseTrackActor-mediapipe0.10.9`  

6. Then install all the requirements for the actors:  
`pip install -r requirements.txt`  

7. Then copy or symbolic link the: `myvenv/lib/python3.9/site-packages` directory to the folder with the actors  

- how to make symbolic link on macOS [here](https://www.howtogeek.com/297721/how-to-create-and-use-symbolic-links-aka-symlinks-on-a-mac/)
- primer on Python venv [here](https://realpython.com/python-virtual-environments-a-primer/)


#### Run actors from Gazebo
- Open GazeboOsc
- From whithin GazeboOsc click "file" and then "load" and navigate to the folder you just downloaded and open "poseTrack.gzs"  
- This will open the stage with the python actor and it wil start running the actor  
*The first time the actor will probably not load*  
- Click on the python actor in te textfiled and hit enter to reload the python file  

## Pose Tracking

Mediapipe documentatiopn [here](https://developers.google.com/mediapipe/solutions/vision/pose_landmarker)
You need to also download the pose_landmarker.task file from the above URL

The MediaPipe Pose Landmarker task lets you detect landmarks of human bodies in an image or video. You can use this task to identify key body locations, analyze posture, and categorize movements. 

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

### Pose tracking Processing Example

In the processing directory you can find oscRecieveGazeboPose which parses the OSC data send out by the pyhton actor to visualise the data.

![Screenshot Processing](img/screenshot01.png)


### Pose tracking Isadora Example

In the isadora directory you can find skeletonVisualiser.izz which parses the OSC data send out by the pyhton actor to visualise the data.
The file is subdivided in different scenes creaed as a tutorial to showcase how you can use the data.

![Screenshot Isadora](img/screenshotIsadora.jpg)


## Face tracking

Mediapipe documentatiopn [here](https://developers.google.com/mediapipe/solutions/vision/face_detector)

The MediaPipe Face Detector task lets you detect faces in an image or video. You can use this task to locate faces and facial features within a frame. This task uses a machine learning (ML) model that works with single images or a continuous stream of images


### OSC message structure

The OSC message send out by the face detection actor starts with the label "/face".
The message has a length of 16 values and consists of 12 landmarks. The first four numbers are the xmin, ymin and width, height of the face boundingbox. For each landmark thes message structure is "ff" meaning two values of type float. These represent the x and y position of the landmark.

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
    12: float right ear x
    13: float right ear y
    14: float left ear x
    15: float left ear y

### Face tracking Processing Example

In the processing directory you can find oscRecieveGazeboPose which parses the OSC data send out by the pyhton actor to visualise the data.

![Screenshot Processing](img/faceDetectionProcessing.jpg)

### Face tracking Isadora Example

In the isadora directory you can find faceDetectionVisualiser.izz which parses the OSC data send out by the pyhton actor to visualise the data.
The file is subdivided in different scenes creaed as a tutorial to showcase how you can use the data.

![Screenshot Isadora](img/faceDetectionIsadora.jpg)



