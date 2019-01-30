//
//  retrieval.h
//  MyPro
//
//  Created by 张挺然 on 19/05/2017.
//  Copyright © 2017 张挺然. All rights reserved.
//

#ifndef retrieval_h
#define retrieval_h

#include "MinHash.h"
#include "SlidingPatch.h"
#include "HOGDescriptor.h"
#include "SaliencyDescriptor.h"
#include "HashIndexer.h"

#define _USE_MATH_DEFINES

#include <math.h>
#include <functional>
#include <iostream>

#define HOG_NUM_CELL		3 // 8
#define HOG_NUM_BIN			9 // 8
#define IMAGE_SCALE			200
#define IMAGE_PATCH_NUM		17
#define IMAGE_PATCH_SIZE	40

typedef ::MinHash64						MinHash;
typedef MinHash::Tuple					Tuple;
typedef MinHash::TupleVector			TupleVector;
typedef ::HashIndexer<MinHash>			Indexer;
typedef ::HashIndexer<MinHash, size_t>	ViewIndexer;
typedef ::HOGDescriptor					PatchDescriptor;
typedef ::SlidingPatch					ImagePatch;

////////////////
cv::Mat formatViewImage(const cv::Mat& image_);
cv::Mat formatDepthImage(const cv::Mat& image);
double computeDepthIoU(const cv::Mat& image1, const cv::Mat& image2);
//double central_angle_dist(const vec2d& v1, const vec2d& v2);

////////////////


cv::Mat load_image(const std::string& imagePath);
void process_image(const cv::Mat& image, const std::function<void(const ImagePatch&, const cv::Mat&, TupleVector&)>& l);

template<typename idx_type>
void insert_image(const cv::Mat& image, const idx_type& imageIdx, HashIndexer<MinHash, idx_type>& hashIndexer)
{
    cv::Mat	image_bw = formatViewImage(image);
    process_image(image_bw, [&imageIdx, &hashIndexer](const ImagePatch& imagePatch, const cv::Mat& featureMat, const TupleVector& tupleVector) {
        PatchInfo pi = PatchInfo(0, imagePatch.index());
        hashIndexer.insert(imageIdx, pi, tupleVector);
    });
}

template<typename idx_type>
void insert_image(const std::string& imagePath, const idx_type& imageIdx, HashIndexer<MinHash, idx_type>& hashIndexer)
{
    cv::Mat image = load_image(imagePath);
    insert_image(image, imageIdx, hashIndexer);
}

template<typename idx_type>
std::vector<std::pair<idx_type, double>> retrieve_image(const std::string& imagePath, HashIndexer<MinHash, idx_type>& hashIndexer)
{
    cv::Mat image = formatViewImage(load_image(imagePath));
    std::vector<std::pair<PatchInfo, TupleVector>> patchVector;
    patchVector.reserve(IMAGE_PATCH_NUM * IMAGE_PATCH_NUM);
    
    SaliencyDescriptor Sal(image);
    
    process_image(image, [&patchVector, &Sal](const ImagePatch& imagePatch, const cv::Mat& featureMat, TupleVector& tupleVector)
                  {
                      PatchInfo info(0, imagePatch.index());
                      cv::Mat saliency;
                      Sal.compute(imagePatch.rect(), saliency);
                      info.iW = 1 - 0.65 * saliency.at<double>(0, 0);
                      
                      patchVector.push_back(std::make_pair<PatchInfo, TupleVector>(std::move(info), move(tupleVector)));
                  });
    
    std::vector<std::pair<idx_type, double>> resultVector = hashIndexer.retrieve(patchVector);
    return resultVector;
}


/////////////////////implementation

#include <stdio.h>
#include "edge_util.h"
#include <fstream>
#include <iomanip>

using namespace cv;
using namespace std;

//
// Helper functions.
//
bool is_feature_valid(const Mat& mat)
{
    double minVal, maxVal;
    minMaxIdx(mat, &minVal, &maxVal);
    return !(minVal == 0 && maxVal == 0);
}

Mat formatViewImage(const Mat& image_)
{
    Mat image = image_;

    if (image.channels() == 3) // to gray image
        cvtColor(image, image, CV_BGR2GRAY);

    assert(image.channels() == 1);
    assert(image.depth() == CV_8U);

    Mat image_bw(image, computeBoundingBox<uchar>(255 - image));	// compute bbox
    image_bw = paddingImage(image_bw, 5);							// padding border
    resize(image_bw, image_bw, Size(IMAGE_SCALE, IMAGE_SCALE));		// resize image

    return image_bw;
}

//
// Main functions.
//
Mat load_image(const string& imagePath)
{
    Mat image;
    image = imread(imagePath, CV_LOAD_IMAGE_GRAYSCALE);

    if (!image.data)
    {
        cerr << "Error: No image data. [" << imagePath << "]" << endl;
        abort();
    }

    return image;
}

void process_image(const Mat& image, const function<void(const ImagePatch&, const Mat&, TupleVector&)>& l)
{
    PatchDescriptor HOG(image, HOG_NUM_CELL, HOG_NUM_CELL, HOG_NUM_BIN);
    ImagePatch imagePatch(HOG, IMAGE_PATCH_NUM, IMAGE_PATCH_SIZE, 5);

    // extract feature
    while (imagePatch.next())
    {
        Mat featureMat;
        HOG.compute(imagePatch.rect(), featureMat);
        if (is_feature_valid(featureMat))
        {
            TupleVector tupleVector = MinHash::Hash(featureMat.ptr<double>(), int_cast_<uint16_t>(featureMat.cols), 0.2);
            l(imagePatch, featureMat, tupleVector);
        }
    }
}


#endif /* retrieval_h */
