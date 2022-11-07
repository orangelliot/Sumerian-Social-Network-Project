// Copy Translated Tablets
// April 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o copyTranslatedBaskets.out copyTranslatedBaskets.cpp

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

  string fromPath = "../../Dataset/Translated/";
  string toPath = "../../Dataset/TranslatedBasketTablets/";
  string fileName;

  while(getline(csv, fileName)){

    if(fileName.substr(fileName.length() - 15, fileName.length() - 16) == ".conll"){
      fileName = fileName.substr(0, 13);
      fromPath = fromPath + fileName;
      toPath = toPath + fileName.substr(0,7) + "basket" + fileName.substr(7, 13);

      std::filesystem::copy_file(fromPath, toPath);

      fromPath = "../../Dataset/Translated/";
      toPath = "../../Dataset/TranslatedBasketTablets/";
    }
  }

  csv.close();
}
