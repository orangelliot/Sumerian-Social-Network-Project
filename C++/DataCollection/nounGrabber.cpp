//g++ -std=c++17 -o nounGrabber.out nounGrabber.cpp

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
  csv.open("../../Dataset/Output/nouns");
  csv << "TabletID\tNoun\tTranslated" << endl;

  string fileName;
  string tabletID;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    fileName = entry.path();
    tabletID = fileName.substr(25,7);

    string noun;
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
        noun = word;
        counter++;
      }
      else if(counter == 2){
        translated = word;
        counter++;
      }
      else if(counter == 3){
        stringID = word;

        if(stringID == "N"){
          csv << tabletID << "\t" << noun << "\t" << translated << endl;
        }

        counter = 0;
      }
    }
    tablet.close();
  }
  csv.close();
}
