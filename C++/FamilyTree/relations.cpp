//g++ -std=c++17 -o relations.out relations.cpp

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
  csv.open("Data/Relations");
  csv << "TabletID\tRelation" << endl;

  string fileName;
  string tabletID;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    fileName = entry.path();
    tabletID = fileName.substr(25,7);

    string word;
    while(tablet >> word){
      if(word == "dumu" || word == "dumu-munus" || word == "dumu_munus" || word == "dam" || word == "ama"
      || word == "šeš" || word == "nin" || word == "nin9" || word == "mussa" || word == "e2-gi4-a"
      || word == "e-gi-a"){
        csv << tabletID << "\t" << word << endl;
      }
    }
    tablet.close();
  }
  csv.close();
}
