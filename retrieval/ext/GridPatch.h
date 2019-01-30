//
//  GridPatch.h
//  MyPro
//
//  Created by 张挺然 on 19/05/2017.
//  Copyright © 2017 张挺然. All rights reserved.
//

#ifndef GridPatch_h
#define GridPatch_h

#include "Patch.h"

class GridPatch : public Patch {
    
protected:
    int _stepX, _stepY;
    int _iWinX, _iWinY;
    
public:
    int _nWinX, _nWinY, _winWidth, _winHeight;
    
    GridPatch(const cv::Mat& im, int nWinX, int nWinY, int winWidth, int winHeight);
    GridPatch(const cv::Mat& im, int nWin, int winSize);
    virtual ~GridPatch();
    
    virtual void begin() override;
    virtual bool next() override;
    virtual void get(int iWinX, int iWinY, cv::Rect& rect) const override;
    cv::Point index() const;
};



////////////////////implementation
using namespace cv;

GridPatch::GridPatch(const Mat& im, int nWinX, int nWinY, int winWidth, int winHeight) : Patch(im), _nWinX(nWinX), _nWinY(nWinY), _winWidth(winWidth), _winHeight(winHeight) {

    _stepX = (_imWidth - _winWidth) / double(_nWinX - 1.0);
    _stepY = (_imHeight - _winHeight) / double(_nWinY - 1.0);

    assert(_stepX > 0 && _stepX < _imWidth);
    assert(_stepY > 0 && _stepY < _imHeight);

    begin();
}

GridPatch::GridPatch(const Mat& im, int nWin, int winSize) : GridPatch(im, nWin, nWin, winSize, winSize) {

    // do nothing here
}

GridPatch::~GridPatch() {

    // do nothing here
}

void GridPatch::begin() {

    _iWinX = 0;
    _iWinY = 1;
    _rect = Rect(0, 0, _winWidth, _winHeight);
}

bool GridPatch::next() {

    if (_iWinX >= _nWinX && _iWinY >= _nWinY)
        return false;

    if (_iWinX < _nWinX) {			// next column
        _iWinX++;
    }
    else if (_iWinX == _nWinX) {	// next row
        _iWinX = 1;
        _iWinY++;
    }

    Point idx = index();
    get(idx.x, idx.y, _rect);
    return true;
}

void GridPatch::get(int iWinX, int iWinY, cv::Rect& rect) const {

    assert(iWinX >= 0 && iWinX < _nWinX);
    assert(iWinY >= 0 && iWinY < _nWinY);

    rect.x = iWinX * _stepX;
    rect.y = iWinY * _stepY;
    rect.width = _winWidth;
    rect.height = _winHeight;
}

Point GridPatch::index() const {

    return Point(_iWinX - 1, _iWinY - 1);
}


#endif /* GridPatch_h */
