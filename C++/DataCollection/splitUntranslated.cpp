//g++ -std=c++17 -o splitUntranslated.out splitUntranslated.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream untranslated;
  ofstream tablet;
  untranslated.open("../../Dataset//ur3_untranslated.atf");

  string path = "../../Dataset/Untranslated/";

  string line;
  string file;
  while(getline(untranslated, line)){
    if(line.length() > 9 && line.substr(0,2) == "&P"){
      tablet.close();
      file = path + line.substr(1, 7) + ".atf";
      tablet.open(file);
    }

    tablet << line << endl;
  }

  tablet.close();
  untranslated.close();
}
