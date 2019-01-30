//
//  handler.cpp
//  MyPro
//
//  Created by 张挺然 on 19/05/2017.
//  Copyright © 2017 张挺然. All rights reserved.
//

#include <pybind11/pybind11.h>
#include <stdio.h>
#include <memory>
#include <string>
#include <vector>
#include "retrieval.h"

using namespace std;
namespace py = pybind11;


template<typename T, typename... Args>
std::unique_ptr<T> make_unique(Args&&... args)
{
    return std::unique_ptr<T>(new T(std::forward<Args>(args)...));
}


class Retriever{
public:
    unique_ptr<Indexer> indexerPtr;
    vector<pair<string, double> > result;

    Retriever(){}

    void initIdx(){
        indexerPtr = make_unique<Indexer>();
    }

    void load(string filePath){
        indexerPtr = make_unique<Indexer>();
        indexerPtr->read(filePath);
    }

    void insert(string imagePath, string imageName){
        if(indexerPtr == nullptr)
            initIdx();
        insert_image(imagePath, imageName, *indexerPtr);
    }

    void save(string imagePath){
        if(indexerPtr == nullptr)
            initIdx();
        indexerPtr->write(imagePath);
    }

    void retrieve_sketch(string imagePath, string imageName){
        if(indexerPtr == nullptr)
            initIdx();
        result = retrieve_image(imagePath, *indexerPtr);
    }

    int getResultSize(){
        return result.size();
    }

    string getResultKey(int i){
        return result[i].first;
    }

    int getResultVal(int i){
        return result[i].second;
    }
};


PYBIND11_PLUGIN(cpphandler) {
    py::module m("cpphandler", "pybind11 cpp handler plugin");

    py::class_<Retriever>(m, "Retriever")
        .def(py::init())
        .def("initIdx", &Retriever::initIdx)
        .def("load", &Retriever::load)
        .def("insert", &Retriever::insert)
        .def("save", &Retriever::save)
        .def("retrieve_sketch", &Retriever::retrieve_sketch)
        .def("getResultSize", &Retriever::getResultSize)
        .def("getResultKey", &Retriever::getResultKey)
        .def("getResultVal", &Retriever::getResultVal);


    return m.ptr();

}


