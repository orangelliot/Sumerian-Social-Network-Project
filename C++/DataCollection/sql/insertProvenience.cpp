//g++ -std=c++17 -o insertProvenience.out insertProvenience.cpp -lmysqlcppconn

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <sstream>

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
  state->execute("DROP TABLE IF EXISTS proveniences");
  state->execute("CREATE TABLE proveniences(tabid char(128) not null, provenience varchar(255) not null, FOREIGN KEY (tabid) REFERENCES tabids (tabid));");
  delete state;

  prepState = connect->prepareStatement("INSERT INTO proveniences(tabid, provenience) VALUES(?,?)");

  fstream file("../../../Dataset/Output/provenience.csv", ios::in);

  string line;
  string word;

  if(file.is_open()){
    getline(file, line);
    while(getline(file, line)){
      stringstream str(line);

      int counter = 1;
      while(getline(str, word, ',')){
        if(word.length() == 1){
          word = "___";
        }
        prepState->setString(counter, word);
        counter++;
      }
      prepState->execute();
      counter = 1;
    }
  }

  delete prepState;
  delete connect;
  return 0;
}
