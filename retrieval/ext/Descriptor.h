//
//  Descriptor.h
//  MyPro
//
//  Created by 张挺然 on 19/05/2017.
//  Copyright © 2017 张挺然. All rights reserved.
//

#ifndef Descriptor_h
#define Descriptor_h

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <stdio.h>

class Descriptor {
    
public:
    const cv::Mat& _im;
    int _imHeight, _imWidth;
    
public:
    Descriptor(const cv::Mat& im);
    virtual ~Descriptor();
    
    virtual void compute(const cv::Rect& position, cv::Mat& H) const = 0;
};


///////////////////implementation
using namespace cv;

Descriptor::Descriptor(const Mat& im) : _im(im) {

    // compute image height & width
    _imHeight = _im.rows;
    _imWidth = _im.cols;
}

Descriptor::~Descriptor() {

    // do nothing here
}

#endif /* Descriptor_h */
