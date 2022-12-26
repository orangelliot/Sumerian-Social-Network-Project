// Year Editor
// May 2022
// Henry Il
// ---------------
// TODO: Synopsis and comments v below v

//g++ -std=c++17 -o yearEdit.out yearEdit.cpp

#include <stdlib.h>
#include <string>
#include <iostream>
#include <fstream>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

int main(int argc, char *argv[]){
    ifstream unformatted;
    ofstream formatted;

    unformatted.open("../../Dataset/years_unformatted.csv");
    formatted.open("../../Dataset/Output/years_formatted.csv");

    char c;
    int stack = 0;
    while(unformatted.good()){
        unformatted.get(c);

        //curly brackets: Remove brackets keep inside
        //round brackets: delete insides and brackets
        if(c == ',' && stack != 0){
            stack = 0;
            formatted << " \"" << c;
        }
        else if(c == ','){
            stack = 0;
            formatted << c;
        }
        else if(c == '{' || c == '}' || c == 'X' || c == 'x' || c == '.'){
            continue;
        }
        else if(c == '('){
            stack = stack + 1;
        }
        else if(c == ')' && stack > 0){
            stack = stack - 1;
        }
        else if(c == ')'){
            continue;
        }
        else if(stack > 0){
            continue;
        }
        else if(stack == 0){
            formatted << c;
        }
    }

    unformatted.close();
    formatted.close();
}
