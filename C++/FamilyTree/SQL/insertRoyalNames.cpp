//g++ -std=c++17 -o insertRoyalNames.out insertRoyalNames.cpp -lmysqlcppconn

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
  state->execute("DROP TABLE IF EXISTS Royal_Names");
  state->execute("CREATE TABLE Royal_Names(tabid char(128) not null, "
                                        "royalName varchar(255) not null, "
                                        "FOREIGN KEY (tabid) REFERENCES tabids (tabid));");
  delete state;

  prepState = connect->prepareStatement("INSERT INTO Royal_Names(tabid, royalName) VALUES(?,?)");

  ifstream file;
  file.open("../Data/RoyalNames");

  string word;
  int counter = 0;
  for(int x = 0; x < 2; x++){
    file >> word;
  }

  while(file >> word){
    if(counter == 0){
      prepState->setString(1, word);
      counter++;
    }
    else if(counter == 1){
      prepState->setString(2, word);
      prepState->execute();
      counter = 0;
    }
  }

  file.close();

  delete prepState;
  delete connect;
  return 0;
}
