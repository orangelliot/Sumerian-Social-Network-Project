//g++ -std=c++17 -o relatedBaskets.out relatedBaskets.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

void basketNames();
void relatedNames();

int main(int argc, char *argv[]){
  basketNames();
  relatedNames();
}

void basketNames(){
  ifstream tablet;
  ofstream csv;
  csv.open("../../Dataset/Output/RelatedBaskets/BasketPersonalNames.csv");
  csv << "TabletID,PersonalName,Translated" << endl;

  string path = "../../Dataset/TranslatedBasketTablets/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    string word;
    string fileName;
    string tabletID;

    string lineID;
    string personalName;
    string translated;
    string stringID;

    for(int x = 0; x < 9; x++){
      tablet >> word;
    }

    int counter = 0;
    while(tablet >> word){
      if(counter == 0){
        counter++;
      }
      else if(counter == 1){
        personalName = word;
        counter++;
      }
      else if(counter == 2){
        translated = word;
        counter++;
      }
      else if(counter == 3){
        stringID = word;

        if(stringID == "PN"){
          fileName = entry.path();
          tabletID = fileName.substr(38,7);

          csv << tabletID << "," << personalName << "," << translated << endl;
        }

        counter = 0;
      }
    }
    tablet.close();
  }
  csv.close();
}

void relatedNames(){

}
