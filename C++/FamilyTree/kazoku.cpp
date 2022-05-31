//g++ -std=c++17 -o kazoku.out kazoku.cpp

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
  csv.open("Data/Kazoku");
  csv << "TabletID\tName\tRelation\tTo\tNameTag\tRelationTag\tToTag" << endl;

  string fileName;
  string tabletID;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    fileName = entry.path();
    tabletID = fileName.substr(25,7);

    string name = "NULL";
    string relation = "NULL";
    string to = "NULL";

    string nameTag = "NULL";
    string relationTag = "NULL";
    string toTag = "NULL";

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
        to = word;
        counter++;
      }
      else if(counter == 2){
        if(word != "KA[flour"){
          counter++;
        }
      }
      else if(counter == 3){
        toTag = word;
        if(relation == "dumu" || relation == "dumu-munus" || relation == "dam" || relation == "ama" || relation == "nin" || relation == "e2-gi4-a"){
          csv << tabletID << "\t" << name << "\t" << relation << "\t" << to << "\t" << nameTag << "\t" << relationTag << "\t" << toTag << endl;
        }

        name = relation;
        relation = to;
        nameTag = relationTag;
        relationTag = toTag;

        counter = 0;
      }
    }
    tablet.close();
  }
  csv.close();
}
