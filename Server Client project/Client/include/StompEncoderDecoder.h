//
// Created by liorsze@wincs.cs.bgu.ac.il on 06/01/2020.
//

#ifndef BOOST_ECHO_CLIENT_STOMPENCODERDECODER_H
#define BOOST_ECHO_CLIENT_STOMPENCODERDECODER_H

#include <string>
#include <vector>
#include "User.h"

using namespace std;



class StompEncoderDecoder{
public:
    StompEncoderDecoder();

    string messageToString(string msg); //receivied answer from server-> encdec-> client
    string stringToFrame(string msg);//received from keyboard->encdec->server
    void setUser(User *user);
    ~StompEncoderDecoder();
    StompEncoderDecoder(const StompEncoderDecoder&);
    StompEncoderDecoder& operator=(const StompEncoderDecoder&);

private:
    int subsId;
    int recieptID;
    User *user;
    map<int,string> mapReciept;

};


#endif //BOOST_ECHO_CLIENT_STOMPENCODERDECODER_H
