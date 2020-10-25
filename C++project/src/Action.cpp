//
// Created by liorsze@wincs.cs.bgu.ac.il on 20/11/2019.
//
#include <string>
#include <vector>
#include <iostream>
#include <unordered_map>
#include "../include/Session.h"
#include "../include/User.h"
#include "../include/Action.h"
#include "../include/Watchable.h"

void BaseAction::act(Session &sess) {}
BaseAction::~BaseAction() {}
BaseAction::BaseAction():username(" "),errorMsg("noError") ,status(PENDING){}
BaseAction::BaseAction(std::string &username):username(username),errorMsg("noError"),status(PENDING){}
std::string BaseAction::getUserName() const {
    return username;
}
ActionStatus BaseAction::getStatus() const {
    return status;
}
void BaseAction::complete() {
    status = COMPLETED;
}
void BaseAction::error(const std::string &errorM) {
    this->errorMsg=errorM;
    status = ERROR;
}
std::string BaseAction::getErrorMsg() const {
    return errorMsg;
}
void BaseAction::setStatus(ActionStatus x) {
    status=x;
}
void BaseAction::setErrorMsg(std::string &&errorM) {
    this->errorMsg=errorM;
}
int BaseAction::findChar(std::string s, char c) {
    int x = s.length();
    for(int i=0; i<x; i++){
        if ((s.at(i)) == c) {
            return i;
        }
    }
    return -1;
}

CreateUser::CreateUser(std::string nameAlgo):BaseAction(nameAlgo){}
void CreateUser::act(Session &sess) {
    std::string nameAndAlgo=getUserName();
    std:: string name;
    std:: string algo;
    int space=findChar(getUserName(),' ');
    name=nameAndAlgo.substr(0,space);
    algo=nameAndAlgo.substr(space+1);
    // check name
    bool found = false;
    for(auto it = sess.getUserMap().begin(); it!=sess.getUserMap().end() && !found; it++)
    {
        if(it->first==name){
            found =true;
            setStatus(ERROR);
            setErrorMsg("User "+name+" already exit!");
            std::string error = "Error - "+getErrorMsg();
            std::cout<<error<<std::endl;

        }
    }
    if(!found){
        //check algo
        if ("len" == algo){
            User* newlen (new LengthRecommenderUser(name));
            sess.getUserMap()[name]=newlen;
            complete();
        }
        else if (algo=="rer") {
            User* newrer (new RerunRecommenderUser(name));
            sess.getUserMap()[name]=newrer;
            complete();
        }
        else if (algo=="gen")
        {
            User* newgen (new GenreRecommenderUser(name));
            sess.getUserMap()[name]=newgen;
            complete();
        }
        else{
            //put error!!!!
            setStatus(ERROR);
            setErrorMsg("Three letter code is invalid");
            std::string error = "Error - "+getErrorMsg();
            std::cout<<error<<std::endl;
        }
    }

}
std::string CreateUser::toString() const {
    std::string output = "CreateUser ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;

}
BaseAction* CreateUser::clone() {
    return new CreateUser(*this);
}

ChangeActiveUser::ChangeActiveUser(std::string username):BaseAction(username) {}
void ChangeActiveUser::act(Session &sess) {
    bool found = false;
    for(auto it = sess.getUserMap().begin(); it!=sess.getUserMap().end() && !found; it++)
    {
        if(it->first.compare(getUserName())==0){
            sess.setActiveUser(it->second);
            found =true;
            complete();
        }
    }
    if(!found){
        setStatus(ERROR);
        setErrorMsg("User "+getUserName()+" does not exit!");
        std::string error = "Error - "+getErrorMsg();
        std::cout<<error<<std::endl;
    }

}
std::string ChangeActiveUser::toString() const {
    std::string output = "ChangeActiveUser ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* ChangeActiveUser::clone() {
    return new ChangeActiveUser(*this);
}

DeleteUser::DeleteUser(std::string username):BaseAction(username) {

}
void DeleteUser::act(Session &sess) {
    bool found = false;
    User *u;
    for(auto &users : sess.getUserMap()){
        std::string name = getUserName();
        if(users.first ==name){
            u=users.second;
            //need to delete it from user map
            sess.deleteUserFromMap(name);
            //detele pointer
            delete u;
            found =true;
            complete();
            break;
        }
    }
    u= nullptr;
    if(!found){
        setStatus(ERROR);
        setErrorMsg("User "+getUserName()+" does not exit!");
        std::string error = "Error - "+getErrorMsg();
        std::cout<<error<<std::endl;
    }
}
std::string DeleteUser::toString() const {
    std::string output = "DeleteUser ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* DeleteUser::clone() {
    return new DeleteUser(*this);
}


DuplicateUser::DuplicateUser(std::string nameSecName):BaseAction(nameSecName) {}
void DuplicateUser::act(Session &sess) {
     std::string nameAndAlgo=getUserName();
     std:: string origName;
     std:: string newName;
     int space=findChar(getUserName(),' ');
     origName=nameAndAlgo.substr(0,space);
     newName=nameAndAlgo.substr(space+1);

     // check names - original exist
     User* origin;
     bool foundOrigin = false;
     for(auto it = sess.getUserMap().begin(); it!=sess.getUserMap().end() && !foundOrigin; it++)
     {
         if(it->first.compare(origName)==0){
             foundOrigin = true;
             origin = it->second;
         }
     }
     if(!foundOrigin){
         setStatus(ERROR);
         setErrorMsg("User "+origName+" does not exit!");
         std::string error = "Error - "+getErrorMsg();
         std::cout<<error<<std::endl;
     }
     //check if new name exist
     bool foundNew = false;
     for(auto it = sess.getUserMap().begin(); it!=sess.getUserMap().end() && !foundNew &&foundOrigin; it++)
     {
         if(it->first.compare(newName)==0){
             foundNew =true;
             setStatus(ERROR);
             setErrorMsg("User "+newName+" already exit!");
             std::string error = "Error - "+getErrorMsg();
             std::cout<<error<<std::endl;

         }
     }
     //if all users are good, lets duplicate them
     if(foundOrigin && !foundNew){
         User* newDup(origin->dupUs(newName));
         sess.addUserToMap(newDup,newName);
         origin = nullptr;
         complete();
     }


     //delete pointer
      origin = nullptr;

 }
std::string DuplicateUser::toString() const {
    std::string output = "DuplicateUser ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* DuplicateUser::clone() {
    return new DuplicateUser(*this);
}

void PrintContentList::act(Session &sess) {
    int x = sess.getContent().size();
    for (int i = 0; i < x; ++i) {
        std::string temp;
        temp= std::to_string(sess.getContent().at(i)->getId())+". "+sess.getContent().at(i)->toString()+" "+std::to_string(sess.getContent().at(i)->getLength())+" minutes [";
        int z = sess.getContent().at(i)->getTags().size();
        for (int j = 0; j <z ; ++j) {
            temp=temp+sess.getContent().at(i)->getTags().at(j)+", ";
        }
        temp=temp.substr(0,temp.size()-2)+"]";
        std::cout<<temp<<std::endl;
    }
    complete();
}
std::string PrintContentList::toString() const {
    std::string output = "PrintContentList ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* PrintContentList::clone() {
    return new PrintContentList(*this);
}

void PrintWatchHistory::act(Session &sess) {
    std::string firstLine = "Watch history for "+sess.getActiveUser().getName();
    sess.getActiveUser().printHist();
    complete();
}
std::string PrintWatchHistory::toString() const {
    std::string output = "PrintWatchHistory ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* PrintWatchHistory::clone() {
    return new PrintWatchHistory(*this);
}

Watch::Watch(std::string contentIdStr):BaseAction(contentIdStr){}
void Watch::act(Session &sess) {
    User &active =sess.getActiveUser();
    std::string num = getUserName();
    int contentId= std::stoi(num)-1;
    //commit the Watching
    //print that whatching;
    std::string output;
    output = "Watching "+sess.getContent().at(contentId)->toString();
    std::cout<<output<<std::endl;
    //add to users history
    active.addHist((sess.getContent().at(contentId)->clone()));
    complete();

    //Recommend to the user
    std::string recom;

    //did the user saw now Episode or Movie??
    if(sess.getContent().at(contentId)->getNextWatchable(sess)!= nullptr){
        //Put Next Episode
        Watchable *recommended =sess.getContent().at(contentId)->getNextWatchable(sess);
        recom = "We recommend watching "+recommended->toString()+", continue watching? [y/n]";
        std::cout<<recom<<std::endl;
        std::string input;
        std::cin>>input;
        if(input=="y"){
            //commit users command to see next
            BaseAction *next = new Watch(std::to_string(recommended->getId()));
            next->act(sess);
            //add to log
            sess.getActionLog().push_back(next);
        }
        recommended= nullptr;
    }else{ //==null
        Watchable *recommended =active.getRecommendation(sess);
        recom = "We recommend watching "+recommended->toString()+", continue watching? [y/n]";
        std::cout<<recom<<std::endl;

        std::string input;
        std::cin>>input;
        if(input=="y"){
            //increase I
            active.increaseI();
            //commit users command to see next
            BaseAction *next = new Watch(std::to_string(recommended->getId()));
            next->act(sess);
            //add to log
            sess.getActionLog().push_back(next);
        }
        recommended= nullptr;
    }

}
std::string Watch::toString() const {
    std::string output = "Watch ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* Watch::clone() {
    return new Watch(*this);
}

void PrintActionsLog::act(Session &sess) {
    for (int i = sess.getActionLog().size()-1; i >=0 ; i--) {
        std::cout<<sess.getActionLog().at(i)->toString()<<std::endl;
    }
    complete();
}
std::string PrintActionsLog::toString() const {
    std::string output = "PrintActionsLog ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* PrintActionsLog::clone() {
    return new PrintActionsLog(*this);
}

void Exit::act(Session &sess) {
    complete();
}
std::string Exit::toString() const {
    std::string output = "Exit ";
    if(getStatus()==COMPLETED){
        output = output+"COMPLETED";
    }else if(getStatus()==PENDING){
        output = output+"PENDING";
    }
    else{
        output = output+"ERROR: "+this->getErrorMsg();
    }
    return output;
}
BaseAction* Exit::clone() {
    return new Exit(*this);
}
