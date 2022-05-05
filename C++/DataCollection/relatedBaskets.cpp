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
string matchChecker(string name);

int main(int argc, char *argv[]){
  basketNames();
  relatedNames();
}

void basketNames(){
  ifstream tablet;
  ofstream csv;
  csv.open("../../Dataset/Output/RelatedBaskets/BasketPersonalNames");
  csv << "TabletID\tPersonalName\tTranslated" << endl;

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

          csv << tabletID << "\t" << personalName << "\t" << translated << endl;
        }

        counter = 0;
      }
    }
    tablet.close();
  }
  csv.close();
}

void relatedNames(){
  ifstream tablet;
  ofstream csv;
  csv.open("../../DataSet/Output/RelatedBaskets/MatchedBaskets.csv");
  csv << "TabletID,MatchID" << endl;

  string path = "../../Dataset/Translated/";
  for(auto & entry : fs::directory_iterator(path)){
    tablet.open(entry.path().c_str());

    cout << entry.path() << endl;

    string word;
    string fileName;
    string tabletID;

    string lineID;
    string personalName;
    string translated;
    string stringID;

    string matchID;

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
        counter++;
      }
      else if(counter == 3){
        stringID = word;

        if(stringID == "PN"){
          if(personalName != "..."){
            ifstream matchfile;
            string path1 = "../../Dataset/Output/RelatedBaskets/BasketPersonalNames";
            matchfile.open(path1);

            string fileName2;
            string tabletID2;

            string word2;
            int count = 0;
            while(matchfile >> word2){
              if(count == 0){
                tabletID2 = word2;
                count++;
              }
              else if(count == 1){
                if(word2 == personalName){
                  fileName2 = entry.path();
                  matchID = fileName.substr(0,7);

                  csv << matchID << "," << tabletID << endl;
                }
                count++;
              }
              else if(count == 2){
                count = 0;
              }
            }

            matchfile.close();
          }
        }

        counter = 0;
      }
    } //END OF WHILE
    tablet.close();
  }

  csv.close();
}
