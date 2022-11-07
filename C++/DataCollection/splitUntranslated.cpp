// Split Untranslated
// April 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o splitUntranslated.out splitUntranslated.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
int main(int argc, char *argv[]){
  ifstream untranslated;
  ofstream tablet;
  string path = argv[1];
  string dirPath = argv[2];

  untranslated.open(path);

  string line;
  string file;
  while(getline(untranslated, line)){
    if(line.length() > 9 && line.substr(0,2) == "&P"){
      tablet.close();
      file = dirPath + line.substr(1, 7) + ".atf";
      tablet.open(file);
      cout << line.substr(1,7) << "\r";
    }
  }

  cout << '\n';

  tablet.close();
  untranslated.close();
}
