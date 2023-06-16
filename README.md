# PoseTrackActor

This repo contains skeletonActor.py flie which can be uses to run in Gazebo as Actor. poseTrack.gzs is a simple stage in which the actor is implemented.

## Mediapipe
This actor uses the [mediapipe library](https://developers.google.com/mediapipe) So you need to refrence to where this library is installed on your system. We advise to use a Python virtual environment for this. See for more information about Python virtual environment [here](https://docs.python.org/3/library/venv.html)

You can then reference to the library at the beginning of the python script as follows:

```
import sys 
sys.path.append("path_to_venv/lib/python3.11/site-packages")
```

## Processing

![Screenshot](img/screenshot01.png)


In the processing directory you can find oscRecieveGazeboPose which parses the OSC data send out by the pyhton actor to visualise the data.


