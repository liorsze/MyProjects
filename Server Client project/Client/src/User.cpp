//
// Created by liorsze@wincs.cs.bgu.ac.il on 07/01/2020.
//

#include <iostream>
#include "../include/User.h"

User::User(string &username, string &password) :username(username),password(password),genreMap(),genreBook(),recieptMap(),wishToBorrow(),bookLock(){}

User::~User() {

    genreMap.clear();
    recieptMap.clear();
    wishToBorrow.clear();
    for (auto &b: genreBook) {
        delete b;
    }
    genreBook.clear();
}

const string &User::getUsername() const {
    return username;
}

void User::setUsername(const string &username) {
    User::username = username;
}

const string &User::getPassword() const {
    return password;
}

void User::setPassword(const string &password) {
    User::password = password;
}

void User::addReciept(int recieptid, string message) {
    recieptMap[recieptid]=message;
}

void User::joinGenre(string genre, int subsId) {
    genreMap[genre]=subsId;
}

void User::exitGenre(string genre) {
    genreMap.erase(genre);
}

int User::getSubsId(string genre) {
    return genreMap.find(genre)->second;
}

string User::receiptResult(int recieptId) {
    return recieptMap.find(recieptId)->second;
}

void User::addBook(Book *book) {
    std::lock_guard<mutex> lockGuard(bookLock);
    genreBook.push_back(book);
}
string User::getBookOwner(string bookname) {
    std::lock_guard<mutex> lockGuard(bookLock);
    for(auto book : genreBook){
        if(book->getBookname()==bookname){
            return book->getOwner();
        }
    }
    return "-";
}

void User::removeBook(string bookname) {
    std::lock_guard<mutex> lockGuard(bookLock);
    vector<Book*>::iterator it=genreBook.begin();
    for(auto book : genreBook){
        if(book->getBookname()==bookname){
            genreBook.erase(it);
            delete book;
            break;
        }
        it++;
    }
}

string User::allBooksByGenre(string genre) {
    std::lock_guard<mutex> lockGuard(bookLock);
    string ret="";
    for(auto b: genreBook){
        if(b->getGenre()==genre && b->getCurrentusername()==username){
            string bname=(b->getBookname()).substr(1);
            ret=ret+bname+",";
        }
    }
    if(ret.size()>0){
        ret=ret.substr(0,ret.size()-1);
    }
    return ret;
}

bool User::hasBook(string bookname, string genre) {
    std::lock_guard<mutex> lockGuard(bookLock);
    for(auto b: genreBook){
        if(b->getBookname()==bookname && b->getCurrentusername()==username && b->getGenre()==genre){
            return true;
        }
    }
    return false;
}

void User::addWishToBorow(string bookname) {
    std::lock_guard<mutex> lockGuard(bookLock);
    wishToBorrow.push_back(bookname);
}

void User::dontWantToBorrowAnymore(string bookname) {
    std::lock_guard<mutex> lockGuard(bookLock);
    vector<string>::iterator it=wishToBorrow.begin();
    for(auto book : wishToBorrow){
        if(book==bookname){
            wishToBorrow.erase(it);
            break;
        }
        it++;
    }
}

bool User::ifIwantToBorowThisBook(string bookname) {
    std::lock_guard<mutex> lockGuard(bookLock);
    for(auto b: wishToBorrow){
        if(b==bookname){
            return true;
        }
    }
    return false;
}

void User::setBookNewCurrentUser(string username,string bookname, string genre) {
    std::lock_guard<mutex> lockGuard(bookLock);
    for(auto &b: genreBook){
        if(b->getBookname()==bookname && b->getGenre()==genre){
            b->setCurrentusername(username);
            break;
        }
    }
}
const map<string,int>& User::getMap() const {
    return genreMap;
}
