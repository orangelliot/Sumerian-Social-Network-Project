//g++ -std=c++17 -o InsertAmbigTablets.out InsertAmbigTablets.cpp -lmysqlcppconn

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

using namespace std;
namespace fs = std::filesystem;

const string server = "sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com";
const string username = "root";
string password;

int main(){
  sql::Driver *driver;
  sql::Connection *connect;
  sql::Statement *state;
  sql::PreparedStatement *prepState;

  cout << "Password: ";
  cin >> password;

  try{
    driver = get_driver_instance();
    connect = driver->connect(server, username, password);
  }
  catch(sql::SQLException e){
    cout << "Could not connect to server. Error message: " << e.what() << endl;
    exit(1);
  }

  connect->setSchema("sumerianDB");

  state = connect->createStatement();
  state->execute("DROP TABLE IF EXISTS ambigtablets");
  state->execute("CREATE TABLE ambigtablets(count varchar(255) not null, tabid char(128) not null, FOREIGN KEY (tabid) REFERENCES tabids (tabid));");
  delete state;

  prepState = connect->prepareStatement("INSERT INTO ambigtablets(count, tabid) VALUES(?,?)");

  ifstream file;
  file.open("../../../Dataset/Output/ambigYears");

  string counter = "name";
  string word;
  while(file >> word){
    if(word.substr(0,1) == "P"){
      prepState->setString(1, counter);
      prepState->setString(2, word);
    }
  }

  file.close();

  delete prepState;
  delete connect;
  return 0;
}
