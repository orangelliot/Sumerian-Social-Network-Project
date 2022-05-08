//g++ -std=c++17 -o AmbigYearGrabber.out AmbigYearGrabber.cpp -lmysqlcppconn

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
  sql::PreparedStatement *prepState;
  sql::ResultSet *result;

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

  prepState = connect->prepareStatement("SELECT * FROM rawyears;");
  result = prepState->executeQuery();

  ofstream abbrev;
  abbrev.open("../../../Dataset/Output/AmbiguousYears/abbrev");

  abbrev << "TabletID\tYearName" << endl;

  string tabletID;
  string yearName;
  while(result->next()){
    tabletID = result->getString(2);
    yearName = result->getString(1);

    if(yearName == "mu sza3-asz-ru-um{ki} ba-hul"){
      abbrev << tabletID << "\t" << yearName << endl;
    }
  }

  abbrev.close();

  delete result;
  delete prepState;
  delete connect;
  return 0;
}
