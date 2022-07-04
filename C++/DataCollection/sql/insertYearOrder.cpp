//g++ -std=c++17 -o insertYearOrder.out insertYearOrder.cpp -lmysqlcppconn

#include <stdlib.h>
#include <string.h>
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
  state->execute("DROP TABLE IF EXISTS yearsequence");
  state->execute("CREATE TABLE yearsequence(rawyear varchar(255) not null, "
                                      "year varchar(255) not null, "
                                      "sequence varchar(255) not null);");
  delete state;

  prepState = connect->prepareStatement("INSERT INTO yearsequence(rawyear, year, sequence) VALUES(?,?,?)");

  FILE *file;
  file = fopen("../../../Dataset/Output/catalog.csv","r");

  char line[255];
  while(fgets(line, 255, file)){
    char *token = strtok(line, ",");
    prepState->setString(1, token);

    token = strtok(NULL, ",");
    prepState->setString(2, token);

    token = strtok(NULL, ",");
    prepState->setString(3, token);
    prepState->execute();
  }

  fclose(file);

  delete prepState;
  delete connect;
  return 0;
}
