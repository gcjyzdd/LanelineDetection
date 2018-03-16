#include <stdio.h>
#include <iostream>

#include <opencv2/core/core.hpp>        // Basic OpenCV structures (cv::Mat, Scalar)
#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>

using namespace cv;
using namespace std;

int main(int argc, char **argv)
{
	cout <<"Usage: ./extractFrames video ext_width path/to/save/images\n"<<endl;
	if(argc<4)        
		cout<<"Please specify the input video, desired extend width, and the path to save the video!"<<endl;
	char fname[50]=".";
	size_t ew;
	if(argc>3)
	{
		sprintf(fname,"%s",argv[3]);
		istringstream ss(argv[2]);
		if (!(ss >> ew))
			cerr << "Invalid number " << argv[1] << '\n';

		cout<<"extend width = "<<ew<<endl;
	}     

	const char* vidname = argv[1];
	VideoCapture cap(vidname);
//    cap.open;
	if(!cap.isOpened())
	{
		cout<<"Oops, cannot open the video "<<argv[1]<<"."<<endl;
		return -1;
	}   

	int w = cap.get(CV_CAP_PROP_FRAME_WIDTH);
	int h = cap.get(CV_CAP_PROP_FRAME_HEIGHT);

	Mat img;
	int ind=0;
	char path[100];
	// black
	Mat IMG = Mat::zeros(h,w+2*ew, CV_8UC3);
	// white
	//Mat IMG = Mat::ones(h,w+2*ew, CV_8UC3);
	//IMG = Scalar(0, 255, 0);

	sprintf(path,"%s/extendedOutput.avi",fname);
	VideoWriter video(path,CV_FOURCC('M','J','P','G'),30, 
		Size(w+2*ew,h),true);
	if(!video.isOpened())
	{
		cout<<"Oops, cannot write the video "<<argv[1]<<"."<<endl;
		return -1;
	}   
	/*
	Copy ROI: http://answers.opencv.org/question/79889/copy-small-part-of-mat-to-another/
	*/
	Rect srcRect(Point(0, 0), Size(w, h)); //select the 2nd row
	Rect dstRect(Point(ew,0), srcRect.size() ); //destination in (3,5), size same as srcRect

	while(cap.read(img))
	{
		img(srcRect).copyTo(IMG(dstRect));
		video.write(IMG);
		ind++;
	}

	return 0;
}
