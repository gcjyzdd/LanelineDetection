import numpy as np
import cv2
import glob
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle


# Test undistortion on an image
img = mpimg.imread('./post_calib/0000.jpg')
img_size = (img.shape[1], img.shape[0])

# Ideal parameters
mtx = np.array([[  1125.0,   0.00000000e+00,   480],
       [  0.00000000e+00,   1125.0,   360],
       [  0.00000000e+00,   0.00000000e+00,   1.00000000e+00]])
print(mtx)
dist = np.array([[0.0, 0, 0, 0, 0]])
print(dist)

plt.figure(figsize=(20,10))
plt.imshow(img)
plt.show()

height = img.shape[0]
width = img.shape[1]

print(height, width)

ew = 338
v2 = 434.25
u2 = 331.25

Width = width+2*ew

IM = np.zeros((height, width+2*ew,3), np.uint8)
for i in range(width):
    IM[:, ew+i, :] = img[:,i,:]

plt.figure(figsize=(20,10))
plt.imshow(IM)
plt.show()


from detector import Detector, print_prof_data

dist_pickle = pickle.load( open( "cam_pickle.p", "rb" ) )
mtx = dist_pickle["mtx"]
dist = dist_pickle["dist"]
M = dist_pickle["M"]
Minv = dist_pickle["Minv"]

detector = Detector(mtx=mtx, dist=dist, M=M, Minv=Minv, sx_thresh=(20,100), s_thresh=(170,255))
# Set number of buffers
detector.LeftLine.N = 5
detector.RightLine.N = 5
# Parameters of Kalman filter. KF is not adoppted here and forget those parameters
q=[10, 10, 20]
R=[1, 1, 1]
detector.setKF_PR(q, R)
# Set margins
detector.setMargin(60)
# Set color transforms
detector.setBinaryFun(flag=5)
# Turn off Kalman filter
detector.switchKF(False)


bin_warp = detector.detectStraight(IM)

plt.figure(figsize=(20,10))
plt.imshow(bin_warp, cmap='gray')
plt.show()


def draw_lines(img, lines, color=[255, 0, 0], thickness=2):
    """
    NOTE: this is the function you might want to use as a starting point once you want to
    average/extrapolate the line segments you detect to map out the full
    extent of the lane (going from the result shown in raw-lines-example.mp4
    to that shown in P1_example.mp4).

    Think about things like separating line segments by their
    slope ((y2-y1)/(x2-x1)) to decide which segments are part of the left
    line vs. the right line.  Then, you can average the position of each of
    the lines and extrapolate to the top and bottom of the lane.

    This function draws `lines` with `color` and `thickness`.
    Lines are drawn on the image inplace (mutates the image).
    If you want to make the lines semi-transparent, think about combining
    this function with the weighted_img() function below
    """
    line_image = np.copy(img) * 0  # creating a blank to draw lines on

    # Iterate over the output "lines" and draw lines on the blank
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_image


def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.

    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    line_img = draw_lines(line_img, lines)
    return line_img


# Define the Hough transform parameters
# Make a blank the same size as our image to draw on
rho = 1 # distance resolution in pixels of the Hough grid
theta = np.pi/180 # angular resolution in radians of the Hough grid
threshold = 5     # minimum number of votes (intersections in Hough grid cell)
min_line_len = 20 #minimum number of pixels making up a line
max_line_gap = 5    # maximum gap in pixels between connectable line segments

bin_warp = bin_warp*255
lines = hough_lines(bin_warp, rho, theta, threshold, min_line_len, max_line_gap)

color_edges = np.dstack((bin_warp, bin_warp, bin_warp))

# Draw the lines on the edge image
combo = cv2.addWeighted(color_edges, 0.8, lines, 1, 0)
plt.figure(figsize=(20,10))
plt.imshow(combo)
plt.show()
