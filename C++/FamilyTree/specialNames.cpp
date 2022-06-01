//g++ -std=c++17 -o specialNames.out specialNames.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream tablet;
  ofstream r;
  ofstream d;
  r.open("Data/RoyalNames");
  d.open("Data/DivineNames");

  r << "TabletID\tRoyalName" << endl;
  d << "TabletID\tDivineNames" << endl;

  string fileName;
  string tabletID;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    fileName = entry.path();
    tabletID = fileName.substr(25,7);

    string name;
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
        name = word;
        counter++;
      }
      else if(counter == 2){
        if(word != "KA[flour"){
          counter++;
        }
      }
      else if(counter == 3){
        stringID = word;

        if(stringID == "RN"){
          r << tabletID << "\t" << name << endl;
        }
        else if(stringID == "DN"){
          d << tabletID << "\t" << name << endl;
        }

        counter = 0;
      }
    }
    tablet.close();
  }
  r.close();
  d.close();
}
