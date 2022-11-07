// Lookup
// October 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o lookup.out lookup.cpp

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
  ofstream csv2;
  csv.open("../../Dataset/Output/eren2");
  csv << "TabletID\tWord\tPOS\t" << endl;

  string fileName;
  string tabletID;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    fileName = entry.path();
    tabletID = fileName.substr(25,7);

    string target;
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
        target = word;
        counter++;
      }
      else if(counter == 2){
        counter++;
      }
      else if(counter == 3){
        stringID = word;

        if(target == "eren2"){
          csv << tabletID << "\t" << target << "\t" << stringID << endl;
        }

        counter = 0;
      }
    }
    tablet.close();
  }
  csv.close();
}
