// Insert Nouns Thread
// July 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -pthread -o insertNounsThread.out insertNounsThread.cpp -lmysqlcppconn

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <vector>

#include <pthread.h>
#include <semaphore.h>

#include <cppconn/driver.h>
#include <cppconn/exception.h>
#include <cppconn/resultset.h>
#include <cppconn/prepared_statement.h>

using namespace std;
namespace fs = std::filesystem;

class DB_instance{
  public:
    string tabid;
    string raw;
    string translated;
    DB_instance(string a, string b, string c){
      tabid = a;
      raw = b;
      translated = c;
    }
};

const string server = "sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com";
const string username = "root";
string password;

sem_t buf_empty;
sem_t buf_full;
int buffersize = 2500;
vector<DB_instance> buffer;
pthread_mutex_t mutex;
int threadno = 5;
int finished = 0;

void *reading(void *arg){
  ifstream file;
  file.open("../../../Dataset/Output/nouns");

  string word;
  string tabid = "NULL";
  string raw = "NULL";
  string translated = "NULL";
  int counter = 0;

  while(file >> word){
    if(counter == 0){
      tabid = word;
      counter++;
    }
    else if(counter == 1){
      raw = word;
      counter++;
    }
    else if(counter == 2){
      translated = word;

      sem_wait(&buf_empty);
      pthread_mutex_lock(&mutex);

      buffer.push_back(DB_instance(tabid, raw, translated));
      tabid = "NULL";
      raw = "NULL";
      translated = "NULL";
      counter = 0;

      pthread_mutex_unlock(&mutex);
      sem_post(&buf_full);
    }
  }

  finished = 1;
  file.close();
  return 0;
}

void *writing(void *arg){
  sql::PreparedStatement *statement = (sql::PreparedStatement*)arg;

  while(finished == 0 || buffer.empty() == 0){
    sem_wait(&buf_full);
    pthread_mutex_lock(&mutex);

    statement->setString(1, buffer.begin()->tabid);
    statement->setString(2, buffer.begin()->raw);
    statement->setString(3, buffer.begin()->translated);
    statement->execute();
    buffer.erase(buffer.begin());

    pthread_mutex_unlock(&mutex);
    sem_post(&buf_empty);
  }

  return 0;
}

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
  state->execute("DROP TABLE IF EXISTS nouns");
  state->execute("CREATE TABLE nouns(tabid char(128) not null, "
                                    "raw varchar(255) not null, "
                                    "translated varchar(255) not null, "
                                    "FOREIGN KEY (tabid) REFERENCES tabids (tabid));");
  delete state;

  prepState = connect->prepareStatement("INSERT INTO nouns(tabid, raw, translated) VALUES(?,?,?)");

  pthread_t reader, writer[threadno];
  pthread_mutex_init(&mutex, NULL);
  sem_init(&buf_empty,0,buffersize);
  sem_init(&buf_full,0,0);

  if(pthread_create(&reader, NULL, &reading, NULL)){
    cout << "Error creating reader thread" << endl;
    exit(-1);
  }

  for(int x = 0; x < threadno; x++){
    if(pthread_create(&writer[x], NULL, &writing, prepState)){
      cout << "Error creating writer thread" << endl;
      exit(-1);
    }
  }

  if(pthread_join(reader, NULL)){
    cout << "Error joining reader thread" << endl;
  }

  //pthread_cancel not the best solution but it works
  for(int x = 0; x < threadno; x++){
    /*if(pthread_join(writer[x], NULL)){
      cout << "Error joining writer thread" << endl;
    }
    else{
      cout << "Thread " << x << endl;
    }*/
    if(pthread_cancel(writer[x]) != ESRCH){
      cout << "Thread " << x << "destroyed" << endl;
    }
  }

  pthread_mutex_destroy(&mutex);
  sem_destroy(&buf_empty);
  sem_destroy(&buf_full);

  delete prepState;
  delete connect;
  return 0;
}
