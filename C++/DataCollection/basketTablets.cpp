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
  csv << "TabletID" << endl;

  string path = "../../Dataset/Translated";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    string word;
    while(tablet >> word){
      if(word == "pisan-dub-ba"){
        csv << entry.path() << endl;
        break;
      }
    }

    tablet.close();
  }

  csv.close();
}
