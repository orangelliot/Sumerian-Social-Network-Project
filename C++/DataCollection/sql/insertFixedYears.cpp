// Insert Fixed Years
// May 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o insertFixedYears.out insertFixedYears.cpp -lmysqlcppconn

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <bits/stdc++.h>

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
    state->execute("DROP TABLE IF EXISTS rawyearsfixed");
    state->execute("CREATE TABLE rawyearsfixed(year varchar(255) not null, tabid char(128) not null);");
    //state->execute("CREATE TABLE rawyearsfixed(year varchar(255) not null, tabid char(128) not null, FOREIGN KEY (tabid) REFERENCES tabids (tabid));");
    delete state;

    prepState = connect->prepareStatement("INSERT INTO rawyearsfixed(year, tabid) VALUES(?,?)");

    ifstream file;
    file.open("../../../Dataset/Output/years_formatted.csv");

    char c;
    string year = "";
    string tablet = "";
    for(int x = 0; x < 11; x++){
        file.get(c);
    }
    bool swtch = 0;
    while(file.good()){
        file.get(c);
        string s(1, c);

        if(c == ','){
            swtch = 1;
            year.erase(year.begin());
            year.erase(year.end()-1);
        }
        else if(c == '\n'){
            swtch = 0;
            if(tablet[0] == '\n'){
              tablet.erase(tablet.begin());
            }

            prepState->setString(1, year);
            prepState->setString(2, tablet);
            prepState->execute();

            year = "";
            tablet = "";
        }

        if(swtch == 0 && c != '\n'){
            year = year + s;
        }
        else if(c != ','){
            tablet = tablet + s;
        }
    }

    file.close();

    delete prepState;
    delete connect;
    return 0;
}
