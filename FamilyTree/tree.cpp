#include <stdlib.h>
#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

class Person{
  //Constructors
  protected:
    string name;
    string profession;
    vector <string> year;
    vector <Person> parents;
    vector <Person> children;
  public:
    Person(string name){
      this-> name = name;
    }

    //Setters
    void setName(string name){
      this-> name = name;
    }
    void setProfession(string profession){
      this-> profession = profession;
    }
    void setYear(string year){
      this-> year.push_back(year);
    }
    void addParents(Person parent){
      this-> parents.push_back(parent);
    }
    void addChildren(Person child){
      this-> children.push_back(child);
    }

    //Getters
    string getName(){
      return this-> name;
    }
    string getProfession(){
      return this-> profession;
    }
    vector <string> getYear(){
      return this-> year;
    }
    vector <Person> getParents(){
      return this-> parents;
    }
    vector <Person> getChildren(){
      return this-> children;
    }
};

vector <Person> makeTree(vector <Person> list){
  string path = "";
  for(auto & entry : fs::directory_iterator(path)){

  }

  return list;
}

void makeCSV(vector <Person> list){
  ofstream csv;
  csv.open("Tree.csv");

  csv << "Name,Profession,Year,Children,Parents" << endl;

  for(Person n : list){

  }

  csv.close();
}

int main(int argc, char *argv[]){
  cout << "Making Tree..." << endl;
  vector <Person> listOfPeople;
  listOfPeople = makeTree(listOfPeople);
  cout << "Finished Tree" << endl;
  
  cout << "Making CSV..." << endl;
  makeCSV(listOfPeople);
  cout << "Finished CSV" << endl;
}
