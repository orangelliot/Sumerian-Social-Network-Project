//g++ -std=c++17 -o ambigYears.out ambigYears.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream tablet;
  ofstream shulgi;
  ofstream amar;
  ofstream abbreviated;

  shulgi.open("../../Dataset/Output/AmbiguousYears/shulgi.csv");
  amar.open("../../Dataset/Output/AmbiguousYears/amar-suen.csv");
  abbreviated.open("../../Dataset/Output/AmbiguousYears/abbreviated.csv");

  shulgi << "TabletID,YearName" << endl;
  amar << "TabletID,YearName" << endl;
  abbreviated << "TabletID,YearName" << endl;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    string word;
    string fileName;
    string tabletID;
    while(tablet >> word){
      if(word == "mu lugal-e sa-as-ru-umki mu-hul"){
        fileName = entry.path();
        fileName = fileName.substr(25,37);
        tabletID = fileName.substr(0,7);
        shulgi << tabletID << "," << word << endl;
        break;
      }
      else if(word == "mu damar-dsuen lugal-e ša-aš-ru-umki a-ra2 2(diš)-kam u3 šu-ru-ud-hu-umki mu-hul"){
        fileName = entry.path();
        fileName = fileName.substr(25,37);
        tabletID = fileName.substr(0,7);
        amar << tabletID << "," << word << endl;
        break;
      }
      else if(word == "mu ša-aš-ru-umki ba-hul" || word == "mu sa-as-ru-umki ba-hul"){
        fileName = entry.path();
        fileName = fileName.substr(25,37);
        tabletID = fileName.substr(0,7);
        abbreviated << tabletID << "," << word << endl;
        break;
      }
    }

    tablet.close();
  }

  abbreviated.close();
  amar.close();
  shulgi.close();
}
