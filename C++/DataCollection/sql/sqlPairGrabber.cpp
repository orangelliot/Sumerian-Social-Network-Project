// SQL Query
// May 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o sqlPairGrabber.out sqlPairGrabber.cpp -lmysqlcppconn

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

    prepState = connect->prepareStatement("SELECT * FROM;");
    result = prepState->executeQuery();

    ifstream file;
    csv.open("../../../Dataset/Output/AllPairs");
    csv << "Pair1,Pair2,Count" << endl;
    

    int count = 0;
    while(result->next()){
        if(count < 2){
            cout << result << "," end; 
        }
        else{
            cout << result << endl;
        }
    }

    csv.close();

    delete result;
    delete prepState;
    delete connect;
    return 0;
}
