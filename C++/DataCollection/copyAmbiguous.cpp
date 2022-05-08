//g++ -std=c++17 -o copyAmbiguous.out copyAmbiguous.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <system_error>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ifstream file;
  file.open("../../Dataset/Output/ambigYears");

  string fromPath = "../../Dataset/Translated/";
  string toPath = "../../Dataset/mu_sza3-asz-ru-um{ki}_ba-hul/";
  string fileName;

  while(getline(file, fileName)){

    if(fileName.substr(0,1) == "P"){
      fileName = fileName.substr(0, 7) + ".conll";
      fromPath = fromPath + fileName;
      toPath = toPath + fileName;

      try{
        std::filesystem::copy_file(fromPath, toPath);
      }
      catch(fs::filesystem_error e){
        cout << "Error Message: " << e.what() << endl;
      }

      fromPath = "../../Dataset/Translated/";
      toPath = "../../Dataset/mu_sza3-asz-ru-um{ki}_ba-hul/";
    }
  }

  file.close();
}
