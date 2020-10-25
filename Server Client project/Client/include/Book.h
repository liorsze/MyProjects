//
// Created by liorsze@wincs.cs.bgu.ac.il on 07/01/2020.
//

#ifndef BOOST_ECHO_CLIENT_BOOK_H
#define BOOST_ECHO_CLIENT_BOOK_H

#include <string>

using namespace std;

class Book {
private:
    string bookname;
    string genre;
    string owner;
    string currentusername;
public:
    Book(string bookname, string genre, string owner);
    const string &getBookname() const;

    void setBookname(const string &bookname);

    const string &getGenre() const;

    void setGenre(const string &genre);

    const string &getOwner() const;

    void setOwner(const string &owner);

    const string &getCurrentusername() const;

    void setCurrentusername(const string &currentusername);
};


#endif //BOOST_ECHO_CLIENT_BOOK_H
