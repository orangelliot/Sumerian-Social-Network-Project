// Place Grabber
// June 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o placeGrabber.out placeGrabber.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream tablet;
  ofstream csv;
  csv.open("../../Dataset/Output/places");
  csv << "TabletID\tPlace\tTranslated\tTag" << endl;

  string fileName;
  string tabletID;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    fileName = entry.path();
    tabletID = fileName.substr(25,7);

    string place;
    string translated;
    string stringID;

    string word;
    for(int x = 0; x < 9; x++){
      tablet >> word;
    }

    int counter = 0;
    while(tablet >> word){
      if(counter == 0){
        counter++;
      }
      else if(counter == 1){
        place = word;
        counter++;
      }
      else if(counter == 2){
        translated = word;
        if(word != "KA[flour"){
          counter++;
        }
      }
      else if(counter == 3){
        stringID = word;

        if(stringID == "GN" || stringID == "SN" || stringID == "AN" || stringID == "TN" || stringID == "WN" || stringID == "FN" || stringID == "QN"){
          csv << tabletID << "\t" << place << "\t" << translated << "\t" << stringID << endl;
        }

        counter = 0;
      }
    }
    tablet.close();
  }
  csv.close();
}
