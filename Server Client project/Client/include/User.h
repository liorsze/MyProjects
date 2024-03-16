//
// Created by liorsze@wincs.cs.bgu.ac.il on 07/01/2020.
//

#ifndef BOOST_ECHO_CLIENT_USER_H
#define BOOST_ECHO_CLIENT_USER_H

#include <string>
#include <map>
#include <list>
#include <vector>
#include <mutex>
#include "Book.h"

using namespace std;


class User{
private:
    //username
    string username;
    //password
    string password;
    //map genre - id
    map<string,int> genreMap;
    //list book
    vector<Book*> genreBook;
    //reciept id - message
    map<int,string> recieptMap;
    //books wish to borow
    vector<string> wishToBorrow;

    mutex bookLock;
public:
    User(string &username,string &password);

    ~User();

    const map<string,int> &getMap() const;

    const string &getUsername() const;

    void setUsername(const string &username);

    const string &getPassword() const;

    void setPassword(const string &password);

    void joinGenre(string genre, int subsId);

    void addReciept(int recieptid,string message);

    void exitGenre(string genre);

    int getSubsId(string genre);

    string receiptResult(int recieptId);

    void addBook(Book *book);

    string getBookOwner(string bookname);

    void removeBook(string bookname);

    string allBooksByGenre(string genre);

    bool hasBook(string bookname, string genre);

    void addWishToBorow(string bookname);

    void dontWantToBorrowAnymore(string bookname);

    bool ifIwantToBorowThisBook(string bookname);

    void setBookNewCurrentUser(string username,string bookname,string genre);
};

#endif //BOOST_ECHO_CLIENT_USER_H
