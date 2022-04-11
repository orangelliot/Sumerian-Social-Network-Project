#include <stdlib.h>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
  ofstream csv;
  csv.open("Tree.csv");

  csv << "TabletID" << endl;

  string path = "../../Dataset/Translated";
  for(auto & entry : fs::directory_iterator(path)){

  }

  csv.close();
}
