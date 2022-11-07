// Basket Tablets
// April 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o basketTablets.out basketTablets.cpp

#include <stdlib.h>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream tablet;
  ofstream csv;
  csv.open("basketTablets.csv");
  csv << "FileName,TabletID" << endl;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    string word;
    string fileName;
    string tabletID;
    while(tablet >> word){
      if(word == "pisan-dub-ba"){
        fileName = entry.path();
        fileName = fileName.substr(25,37);
        tabletID = fileName.substr(0,7);
        csv << fileName << "," << tabletID << endl;
        break;
      }
    }

    tablet.close();
  }

  csv.close();
}
