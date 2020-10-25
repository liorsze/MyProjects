
#include <fstream>
#include "../include/json.hpp"
#include "../include/Session.h"
#include "../include/User.h"
#include "../include/Watchable.h"
#include "../include/Action.h"
using json = nlohmann::json;
using namespace std;

//Constructor
Session::Session(const std::string &configFilePath):content(), actionsLog(), userMap(),activeUser() {
    //reading from jason
    std::ifstream i(configFilePath);
    json j;
    i>>j;
    i.close();

    //creat Watchable list
    int id=1;
    for(auto &element : j["movies"].items()){
        string name = element.value()["name"];
        int length = element.value()["length"];
        vector<string> tagsVector;
        for(auto &tags: element.value()["tags"].items()){
            tagsVector.push_back(tags.value());
        }
        content.push_back(new Movie(id,name,length,tagsVector));
        id++;
    }
    for(auto& element : j["tv_series"].items()){
        string name = element.value()["name"];
        int length = element.value()["episode_length"];
        vector<string> tagsVector;
        for(auto &tags: element.value()["tags"].items()){
            tagsVector.push_back(tags.value());
        }
        int season =1;
        for(auto &seasons: element.value()["seasons"].items()){
            int episode = seasons.value();
            for(int k=1; k<=episode; k++){
                content.push_back(new Episode(id,name,length,season,k,tagsVector));
                id++;
            }
            season++;
        }

    }
    //set next id in Episodes;


    User* def(new LengthRecommenderUser("default"));
    userMap[def->getName()]=def;
    activeUser=def;
}
//Copy Constructor
Session::Session( const Session &other):content(), actionsLog(), userMap(),activeUser(){
    this->copy(other);
}
//Move Constructor
Session::Session(Session &&other):content(), actionsLog(), userMap(),activeUser() {
    this->move(other);
    // set null
    setOtherNull(other);
}
//Copy Assignment
Session& Session::operator=(const Session &other) {
    if (this != &other) {
        clean();
        copy(other);
    }
    return *this;
}
//Move Assignment
Session& Session::operator=(Session &&other) {
    if (this != &other) {
        clean();
        this->move(other);
        setOtherNull(other);
    }
    return *this;
}

void Session::deleteUserFromMap(std::string &name) {
    userMap.erase(name);
}

std::vector<BaseAction*>& Session::getActionLog() {
    return actionsLog;
}
User& Session::getActiveUser()  {
    return *activeUser;
}
std::unordered_map<std::string,User*>& Session::getUserMap()  {
    return userMap;
}
void Session::setActiveUser(User* newActiveUser) {
    activeUser=newActiveUser;
}
void Session::start() {
    std::cout<<"SPLFLIX is now on!"<<std::endl;
    std::string input;
    std::getline(std::cin,input);

    while (input.compare("exit")!=0)
    {
        int space = findChar(input,' ');
        if(space==-1){//watchhist,content,exit,log,
            if(input.compare("content")==0){
                //print content
                BaseAction* content=new PrintContentList();
                content->act(*this);
                //add this action to logs
                actionsLog.push_back(content);

            }
            else if(input.compare("watchhist")==0){
                //print whatch history
                BaseAction* hist=new PrintWatchHistory();
                hist->act(*this);
                //add this action to logs
                actionsLog.push_back(hist);

            }
            else if(input.compare("log")==0){
                //log action
                BaseAction* log=new PrintActionsLog();
                log->act(*this);
                //add this action to logs
                actionsLog.push_back(log);
            }
            else{
                //do nothing because we assuming that input is valid
            }
        }
        else{//createuser,changeuser,deleteuser,dupuser,watch,
            std::string action=input.substr(0,space);
            if(action.compare("createuser")==0){
                string nameAlgo = input.substr(space+1);
                //new BaseAction
                BaseAction* createnew = new CreateUser(nameAlgo);
                createnew->act(*this);
                //add this action to logs
                actionsLog.push_back(createnew);


            }
            else if(action.compare("changeuser")==0){
                string username = input.substr(space+1);
                //new BaseAction
                BaseAction* change = new ChangeActiveUser(username);
                change->act(*this);
                //add this action to logs
                actionsLog.push_back(change);


            }
            else if(action.compare("deleteuser")==0){
                string username = input.substr(space+1);
                //new BaseAction
                BaseAction* deleteU = new DeleteUser(username);
                deleteU->act(*this);
                //add this action to logs
                actionsLog.push_back(deleteU);


            }
            else if(action.compare("dupuser")==0){
                string nameSecName = input.substr(space+1);
                //new BaseAction
                BaseAction* dupuser = new DuplicateUser(nameSecName);
                dupuser->act(*this);
                //add this action to logs
                actionsLog.push_back(dupuser);

            }
            else if(action.compare("watch")==0){
                string contentIdStr = input.substr(space+1);
                //new BaseAction
                BaseAction* watch = new Watch(contentIdStr);
                watch->act(*this);
                //add this action to logs
                actionsLog.push_back(watch);
            }
            else{
                //do nothing because we assuming that input is valid
            }
        }
        std::getline(std::cin,input);
    }
    if(input.compare("exit")==0){
        //exit loop
        BaseAction* exit=new Exit();
        exit->act(*this);
        //add this action to logs
        actionsLog.push_back(exit);
    }



}
//Distructor
Session::~Session() {
    clean();
}
void Session::clean() {
    activeUser= nullptr;
    for(auto &users : userMap){
        delete users.second;
    }
    for (auto &cont: content) {
        delete cont;
    }
    for (auto &logs: actionsLog) {
        delete logs;
    }

    userMap.clear();
    actionsLog.clear();
    content.clear();
}
void Session::copy(const Session &other) {
    for(auto &cont:other.content){
        this->content.push_back(cont->clone());
    }
    for(auto &log : other.actionsLog){
        this->actionsLog.push_back(log->clone());
    }
    for(auto &users : other.userMap){
        this->userMap[users.first]=users.second->clone();
    }
    for(auto &user: userMap){
        if(user.first==(other.activeUser->getName())){
            this->activeUser=user.second;
        }
    }
}
void Session::setOtherNull(Session &other) {
    /// set null
    other.activeUser= nullptr;
    for (auto &cont : other.content) {
        cont = nullptr;
    }
    other.content.clear();
    for (auto &log : other.actionsLog) {
        log = nullptr;
    }
    other.actionsLog.clear();
    for(auto &user: other.userMap){
        user.second = nullptr;
    }
    other.userMap.clear();
}
void Session::move(Session &other) {
    activeUser=other.activeUser;
    for(auto &cont: other.content){
        this->content.push_back(cont);
    }
    for(auto &logs: other.actionsLog){
        this->actionsLog.push_back(logs);
    }
    for(auto &user: other.userMap){
        userMap[user.first]=user.second;
    }
}
int Session::findChar(std::string s, char c) {
    int n = s.length();
    for(int i=0; i<n; i++){
        if ((s.at(i)) == c) {
            return i;
        }
    }
    return -1;
}
void Session::addUserToMap(User *newActiveUser, std::string &newname) {
    userMap[newname]=newActiveUser;
}

const std::vector<Watchable*>& Session::getContent() const {
    return content;
}

