//
//  Patch.h
//  MyPro
//
//  Created by 张挺然 on 19/05/2017.
//  Copyright © 2017 张挺然. All rights reserved.
//

#ifndef Patch_h
#define Patch_h

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

class Patch {
    
protected:
    int _imHeight, _imWidth;
    cv::Rect _rect;
    
public:
    Patch(const cv::Mat& im);
    virtual ~Patch();
    
    virtual const cv::Rect& rect() const;
    virtual bool isOverflow(const cv::Rect& rect) const;
    
    virtual void begin() = 0;
    virtual bool next() = 0;
    virtual void get(int iWinX, int iWinY, cv::Rect& rect) const = 0;
};


/////////////////implementation


#include <stdio.h>
#include <cassert>

using namespace cv;

Patch::Patch(const Mat& im) : _imHeight(im.rows), _imWidth(im.cols) {

    // do nothing here
}

Patch::~Patch() {

    // do nothing here
}

bool Patch::isOverflow(const cv::Rect& rect) const {

    return (rect.x < 0 || rect.x >= _imWidth || rect.y < 0 || rect.y >= _imHeight ||
            rect.width < 1 || rect.x + rect.width > _imWidth || rect.height < 1 || rect.y + rect.height > _imHeight);
}

const Rect& Patch::rect() const {

    assert(!isOverflow(_rect));
    return _rect;
}


#endif /* Patch_h */
