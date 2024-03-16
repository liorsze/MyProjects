//
// Created by liorsze@wincs.cs.bgu.ac.il on 07/01/2020.
//

#include "../include/Book.h"
Book::Book(string bookname, string genre, string owner):bookname(bookname),genre(genre),owner(owner),currentusername(owner){};

const string &Book::getBookname() const {
    return bookname;
}

void Book::setBookname(const string &bookname) {
    Book::bookname = bookname;
}

const string &Book::getGenre() const {
    return genre;
}

void Book::setGenre(const string &genre) {
    Book::genre = genre;
}

const string &Book::getOwner() const {
    return owner;
}

void Book::setOwner(const string &owner) {
    Book::owner = owner;
}

const string &Book::getCurrentusername() const {
    return currentusername;
}

void Book::setCurrentusername(const string &currentusername) {
    Book::currentusername = currentusername;
}
