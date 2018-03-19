#!/bin/bash

make extendVideo
./extendVideo post_calib_compress.mp4 338 .

make

mkdir output
mkdir post_calib

./extractFrames post_calib_compress.mp4 ./post_calib

