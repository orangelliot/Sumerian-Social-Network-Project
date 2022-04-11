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
  csv.open("Tree.csv");
  csv << "TabletID" << endl;

  string path = "../../Dataset/Translated";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path());

    string line = "";
    while(getline(tablet, line) != EOF){
      //split string
      //check split for pisan dub-ba
    }

    tablet.close();
  }

  csv.close();
}
