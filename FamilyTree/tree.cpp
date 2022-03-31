#include <stdlib.h>
#include <string>
#include <vector>
#include <iostream>

using namespace std;

class Person{
  //Constructors
  protected:
    string name;
    char sex;
    vector <Person> parents;
    vector <Person> children;
  public:
    Person(string name, char sex){
      this-> name = name;
      this-> sex = sex;
    }

    //Setters
    void setName(string name){
      this-> name = name;
    }
    void setSex(char sex){
      this-> sex = sex;
    }
    void addParents(Person parent){
      this-> parents.push_back(parent);
    }
    void addChildren(Person child){
      this-> children.push_back(child);
    }

    //Getters
    string getName(){
      return name;
    }
    char getSex(){
      return sex;
    }
    vector <Person> getParents(){
      return parents;
    }
    vector <Person> getChildren(){
      return children;
    }
};

int main(int argc, char *argv[]){

}
