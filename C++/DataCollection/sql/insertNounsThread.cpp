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

const string server = "sumerian-social-network.clzdkdgg3zul.us-west-2.rds.amazonaws.com";
const string username = "root";
string password;

sem_t buf_empty;
sem_t buf_full;
int buffersize = 1000;
vector<vector<string>> buffer(buffersize);
pthread_mutex_t mutex;

void *reading(void *arg){
  ifstream file;
  file.open("../../../Dataset/Output/nouns");

  vector<string> instance;
  string word;
  int counter = 0;

  while(file >> word){
    if(counter == 0){
      instance.push_back(word);
      counter++;
    }
    else if(counter == 1){
      instance.push_back(word);
      counter++;
    }
    else if(counter == 2){
      instance.push_back(word);

      sem_wait(&buf_empty);
      pthread_mutex_lock(&mutex);

      buffer.push_back(instance);
      instance.clear();
      counter = 0;

      pthread_mutex_unlock(&mutex);
      sem_post(&buf_full);
    }
  }

  file.close();
  return 0;
}

void *writing(void *arg){
  sql::PreparedStatement *statement = (sql::PreparedStatement*)arg;

  while(1){
    sem_wait(&buf_full);
    pthread_mutex_lock(&mutex);

    statement->setString(1, buffer[0][0]);
    statement->setString(2, buffer[0][1]);
    statement->setString(3, buffer[0][2]);
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

  pthread_t reader, writer;
  pthread_mutex_init(&mutex, NULL);
  sem_init(&buf_empty,0,buffersize);
  sem_init(&buf_full,0,0);

  if(pthread_create(&reader, NULL, &reading, NULL)){
    cout << "Error creating reader thread" << endl;
    exit(-1);
  }

  if(pthread_create(&writer, NULL, &writing, prepState)){
    cout << "Error creating writer thread" << endl;
    exit(-1);
  }

  if(pthread_join(reader, NULL)){
    cout << "Error joining reader thread" << endl;
  }

  if(pthread_join(writer, NULL)){
    cout << "Error joining writer thread" << endl;
  }

  pthread_mutex_destroy(&mutex);
  sem_destroy(&buf_empty);
  sem_destroy(&buf_full);

  delete prepState;
  delete connect;
  return 0;
}
