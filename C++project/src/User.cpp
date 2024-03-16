//
// Created by liorsze@wincs.cs.bgu.ac.il on 20/11/2019.
//

#include <string>
#include <vector>
#include <math.h>
#include <unordered_map>
#include <algorithm>
#include "../include/User.h"
#include "../include/Session.h"
#include "../include/Watchable.h"

User::User(const std::string &name):history(), name(name) {}
//copy constructor
User::User(const User &other):history(), name(other.name){//&

    for(auto cont:other.history) {
        this->history.push_back(cont->clone());
    }
}
//move constructor
User::User(User &&other):history(), name(other.name){
    for(auto &hist: other.history){
        this->history.push_back(hist);
        hist= nullptr;
    }
}
//assignment operator
User& User::operator=(const User &other) {
    if (this != &other) {
        for(auto &hist: history){
            delete hist;
        }
        history.clear();
        for(auto &hist: other.history){
            history.push_back(hist->clone());
        }
    }
    return *this;
}
//move assignment operator
User& User::operator=(User &&other) {
    if (this != &other) {
        for(auto &hist: history){
            hist= nullptr;
        }
        history.clear();
        for(auto &hist: other.history){
            history.push_back(hist);
        }
        for(auto &hist: other.history){
            hist= nullptr;
        }
        other.history.clear();
    }
    return *this;
}

std::vector<Watchable*> User::get_history() const {
    return history;}
std::string User::getName() const { return name;}
void User::addHist(Watchable* wat) {
    history.push_back(wat);
}
void User::printHist() {
    int id =1;
    for(auto h : history){
        std::cout << id<<". "<<h->toString()<<std::endl;
        id++;
    }
}
User::~User() {
for(auto &h: history)
   delete h;
history.clear();
}



LengthRecommenderUser::LengthRecommenderUser(const std::string &name):User(name) {}
Watchable* LengthRecommenderUser::getRecommendation(Session &s) {
    //find avg content length
    long avg = 0;
    for (auto & i : history) {
        avg = avg + i->getLength();
    }
    avg = avg /( history.size());

    //find similar lengh content
    double distance = INFINITY;
    Watchable *found;
    for(auto content: s.getContent()){
        int len=content->getLength();
        //check if this content in watch history
        bool sawThisMovie = false;
        for(auto hist : history){
            if(hist->toString() == content->toString()){
                sawThisMovie = true;
            }
        }
        if(abs(avg-len)<distance && !sawThisMovie){
            distance=abs(avg-len);
            found=content;
        }
    }
    return found;
}
User* LengthRecommenderUser::clone() {
    return new LengthRecommenderUser(*this);
}
User* LengthRecommenderUser::dupUs(std::string &newName) {
    User* dup =new LengthRecommenderUser(newName);
    for(auto cont: history) {
        dup->addHist(cont->clone());
    }

    return dup;
}
void LengthRecommenderUser::setI(int &i) {}
void LengthRecommenderUser::increaseI() {}


RerunRecommenderUser::RerunRecommenderUser(const std::string& name):User(name),i(0){};
Watchable* RerunRecommenderUser::getRecommendation(Session &s) {
        int ret = i;
        return history[ret%(history.size())];
}
User* RerunRecommenderUser::clone() {
    return new RerunRecommenderUser(*this);
}
User* RerunRecommenderUser::dupUs(std::string &newName) {
    User* dup =new RerunRecommenderUser(newName);
    dup->setI(this->i);
    for(auto cont: history) {
        dup->addHist(cont->clone());
    }

    return dup;
}
void RerunRecommenderUser::setI(int &i) {
    this->i=i;
}
void RerunRecommenderUser::increaseI() {i++;}


GenreRecommenderUser::GenreRecommenderUser(const std::string& name):User(name){};
Watchable* GenreRecommenderUser::getRecommendation(Session &s) {


    //creating a vector of all types of genres
    std:: vector<std::string> tagsname;
    for (auto c:s.getContent()){
        for (const auto tInc: c->getTags())
        {
            bool flag= false;
            for (const auto &t: tagsname)
            {
                if (tInc==t)
                    flag= true;
            }
            if(!flag)
                tagsname.push_back(tInc);
        }
    }
    // sorting the string vector
    std::sort(tagsname.begin(),tagsname.end());
    //counter Array - init with 0
    std::vector<int> countVec;
    for(auto t : tagsname){
        countVec.push_back(0);
    }

   //count how many times some tag watched
    for (auto watched :history){
        for (const auto& gen: watched->getTags())
        {
            bool found= false;
            int x=tagsname.size();
            for (int i = 0; i < x && !found; ++i) {
                if (gen==tagsname.at(i))
                {
                    found=true;
                    countVec.at(i)++;
                }
            }
        }
    }
    //find the most watched category
    int max =0;
    int maxI=0;
    int a = countVec.size();
    for(int i=0; i<a;i++) {
        if (countVec.at(i) > max) {
            max = countVec.at(i);
            maxI = i;
        }
    }
    //find siutable reccomendation for movie
    std::string maxGengre;
    bool foundRec = false;
    while(!foundRec){
        maxGengre=tagsname.at(maxI);
        //find in content whatchable with ,axgenreI
            for(auto cont: s.getContent()){
                bool alredyWatched= false;
                for(auto h : history){
                    if(cont->toString()==h->toString()){
                        alredyWatched=true;
                    }
                }
                if(!alredyWatched){
                    int b=cont->getTags().size();
                    for(int i=0; i<b; i++){
                        if(maxGengre==cont->getTags().at(i)){
                            foundRec=true;
                            return cont;
                        }
                    }
                }
            }
            //if we havent found with this tag no movie, lets take next Max Genre.
            countVec.at(maxI)=0;
            max=0;
            maxI=0;
            int d =countVec.size();
            for(int i=0; i<d;i++) {
                if (countVec.at(i) > max) {
                    max = countVec.at(i);
                    maxI = i;
                }
            }
    }
    return nullptr;
}
User* GenreRecommenderUser::clone() {
    return new GenreRecommenderUser(*this);
}
User* GenreRecommenderUser::dupUs(std::string &newName) {
    User* dup =new GenreRecommenderUser(newName);
    for(auto cont: history) {
        dup->addHist(cont->clone());
    }

    return dup;
}
void GenreRecommenderUser::setI(int &i) {}
void GenreRecommenderUser::increaseI() {}
