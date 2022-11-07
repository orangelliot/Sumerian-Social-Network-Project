// Copy Untranslated Tablets
// April 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o copyUntranslatedBaskets.out copyUntranslatedBaskets.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream csv;
  csv.open("../../Dataset/basketTablets.csv");

  string fromPath = "../../Dataset/Untranslated/";
  string toPath = "../../Dataset/UntranslatedBasketTablets/";
  string fileName;

  while(getline(csv, fileName)){

    if(fileName.substr(0,1) == "P"){
      fileName = fileName.substr(0, 7);
      fromPath = fromPath + fileName + ".atf";
      toPath = toPath + fileName + "basket" + ".atf";

      std::filesystem::copy_file(fromPath, toPath);

      fromPath = "../../Dataset/Untranslated/";
      toPath = "../../Dataset/UntranslatedBasketTablets/";
    }
  }

  csv.close();
}
