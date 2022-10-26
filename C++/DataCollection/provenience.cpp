// Provenience
// June 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o provenience.out provenience.cpp

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  PyObject *pName, *pModule, *pFunction;
  PyObject *pArgs, *pValue;

  Py_Initialize();
  pName = PyUnicode_DecodeFSDefault("../../Python/Temp/webScrape.py");

  pModule = PyImport_Import(pName);
  Py_DECREF(pName);

  if(pModule != NULL){
    pFunction = pyObject_GetAttrString(pModule, getMassProvenience);

    if(pFunction && PyCallable_Check(pFunction)){
      string path = "../../Dataset/Translated/";
      string filename;

      for(auto & entry : fs::directory_iterator(path)){
        tablet.open(entry.path().c_str());

        fileName = entry.path();
        tabletID = fileName.substr(25,7);

        pArgs = fileName;

        pValue = PyObject_CallObject(pFunction, pArgs);

        cout << pValue << endl;

        Py_DECREF(pArgs);
        Py_DECREF(pValue);
      }
    }
  }
  Py_DECREF(pModule);
  Py_DECREF(pFunction);
}
