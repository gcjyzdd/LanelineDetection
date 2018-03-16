# LanelineDetection

Straight laneline detection using python and opencv

At this moment, only straight lane line is taken into account. Curved laneline may be implemented in the future.


Configuration:

* camera intrinsic matrix
* camera extrinsic matrix
* lane width

## Goals

1. Laneline detection (maybe include road edge)
2. Lane departure warning
3. Lane keeping assisting system


## Methods

1. Calculate ROI of camera images
2. Warp perspective transform applied to ROI such that a bird view is obtained
3. Hough line detection and validity check
4. Decide left and right distance
5. Decide yaw angle of the vehicle
6. Steering angle correction

