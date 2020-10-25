
#include <sstream>
#include <iostream>
#include "../include/StompEncoderDecoder.h"
using namespace std;


StompEncoderDecoder::StompEncoderDecoder():subsId(0),recieptID(10),user(nullptr),mapReciept() {}


void StompEncoderDecoder::setUser(User *user) {
    this->user=user;
}

StompEncoderDecoder::StompEncoderDecoder(const StompEncoderDecoder &other):subsId(other.subsId),recieptID(other.recieptID),user(other.user),mapReciept() {
}
StompEncoderDecoder& StompEncoderDecoder::operator=(const StompEncoderDecoder & other) {
    if(this!=&other){
        delete user;
        mapReciept.clear();
        subsId=other.subsId;
        recieptID=other.recieptID;
        user=other.user;
    }
    return *this;
}

StompEncoderDecoder::~StompEncoderDecoder() {
    //delete user;
    mapReciept.clear();
}

string StompEncoderDecoder::stringToFrame(string msg) {
    //splitting to string array by " "
   vector<string> arr;
   stringstream ss(msg);
    std::string segment;
    while(std::getline(ss, segment, ' '))
    {
        arr.push_back(segment);
    }

    if(arr.size()>0) {
        if (arr[0] == "login") {
            if (arr.size() == 4) {

                string result ="";
                result=result+"CONNECT" + '\n';
                result = result + "accept-version:1.2" + '\n';
                result = result + "host:stomp.cs.bgu.ac.il" + '\n';
                result = result + "login:" + arr[2] + '\n';
                result = result + "passcode:" + arr[3] + '\n'+""+'\n';
                return result;
            } else {
                return " ";
            }
        } else if (arr[0] == "join")//join club
        {
            if (arr.size() == 2) {
                subsId++;
                recieptID++;
                string result ="";
                result=result+"SUBSCRIBE" + '\n';
                result = result + "destination:" + arr[1] + '\n';
                result = result + "id:" + to_string(subsId) + '\n';
                result = result + "receipt:" + to_string(recieptID) + '\n'+""+'\n';
                user->joinGenre(arr[1], subsId);
                string s("Joined club " + arr[1]);
                user->addReciept(recieptID, s);
                return result;
            }
           else{
                return " ";
           }
        } else if (arr[0] == "exit") {//exit club
            if (arr.size() == 2) {
                recieptID++;
                string result ="";
                result=result+"UNSUBSCRIBE" + '\n';
                int subId =user->getSubsId(arr[1]);
                result = result + "id:" + to_string(subId) + '\n';
                result = result + "receipt:" + to_string(recieptID) + '\n'+""+'\n';

                user->exitGenre(arr[1]);
                string s("Exited club " + arr[1]);
                user->addReciept(recieptID, s);
                return result;
            }
            else{
                return " ";
            }
        } else if (arr[0] == "add") {
            if (arr.size() >= 3) {
                string bookname="";
                int x = arr.size();
                for(int i=2; i<x;i++){
                    bookname=bookname+" "+arr[i];
                }
                Book *book = new Book(bookname,arr[1],user->getUsername());
                user->addBook(book);

                string result ="";
                result= result+"SEND" + '\n';
                result = result + "destination:" + arr[1] + '\n';
                result=result+""+'\n';
                result= result +user->getUsername()+" has added the book"+bookname+'\n';

                return result;
            } else{
                return " ";
            }

        } else if (arr[0] == "borrow") {
            // Borrow
            if (arr.size()>=3){
                string bookname="";
                int x = arr.size();
                for(int i=2; i<x;i++){
                    bookname=bookname+" "+arr[i];
                }
                user->addWishToBorow(bookname);

                string result ="";
                result=result+"SEND" + '\n';
                result = result + "destination:" + arr[1] + '\n';
                result=result+""+'\n';
                result=result + user->getUsername()+" wish to borrow"+bookname+'\n';
                return result;

            } else{
                return " ";
            }

        } else if (arr[0] == "return") {
            // Return
            if(arr.size()>=3){
                string bookname="";
                int x = arr.size();
                for(int i=2; i<x;i++){
                    bookname=bookname+" "+arr[i];
                }

                string bookOwner=user->getBookOwner(bookname);

                if(bookOwner!="-" && bookOwner!=user->getUsername()){
                    string result ="";
                    result=result+"SEND" + '\n';
                    result = result + "destination:" + arr[1] + '\n';
                    result=result+""+'\n';
                    result=result + "Returning"+bookname+" to "+bookOwner+'\n';

                    user->removeBook(bookname);

                    return result;
                } else{
                    return " ";
                }
            }
            else{
                return " ";
            }

        } else if (arr[0] == "status") {
            if(arr.size()==2){
                string result ="";
                result=result+"SEND" + '\n';
                result = result + "destination:" + arr[1] + '\n';
                result=result+""+'\n';
                result= result+"book status"+'\n';
                return result;
            }
            else{
                return " ";
            }

        } else if (arr[0] == "logout") {
            if (arr.size() == 1) {

                string result ="";

                map<string,int> unsub = user->getMap();
                for(auto sub : unsub){
                    recieptID++;
                    string gen = sub.first;
                    int subid = sub.second;

                    result=result+"UNSUBSCRIBE" + '\n';
                    result = result + "id:" + to_string(subid) + '\n';
                    result = result + "receipt:" + to_string(recieptID) + '\n'+""+'\n'+'\0';

                    user->exitGenre(gen);
                    string s("Exited club " + gen);
                    user->addReciept(recieptID, s);

                }

                recieptID++;
                result=result+"DISCONNECT" + '\n';
                result = result + "receipt:" + to_string(recieptID) + '\n'+""+'\n';
                user->addReciept(recieptID, "LOGOUT");
                return result;
            } else{
                return " ";
            }
        } else {
            return " ";
            }
    }else{
        return " ";
    }



}
string StompEncoderDecoder::messageToString(string msg) {
    vector<string> arr;
    stringstream ss(msg);
    std::string segment;
    while(std::getline(ss, segment, '\n'))
    {
        arr.push_back(segment);
    }
    if(arr[0]=="CONNECTED"){
        string result="Login successful ";
        //print result to the screen
        return  result;

    } else if (arr[0]=="RECEIPT"){
        string rid=arr[1];
        rid=rid.substr(rid.find(':')+1);
       stringstream g(rid);
       int x=0;
        g>>x;
        string result=user->receiptResult(x);
        //print result to the screen
        return result;

    } else if (arr[0]=="MESSAGE"&& arr.size()>=6){
        vector<string> messagevector;
        stringstream ss1(arr[5]);
        std::string segment1;
        while(std::getline(ss1, segment1, ' '))
        {
            messagevector.push_back(segment1);
        }
        string genre= arr[3].substr(arr[3].find(':')+1);
        //status book:
        if(messagevector.size()==2 && messagevector[0]=="book" && messagevector[1]=="status") {

            string result = "";
            result = result + "SEND" + '\n';
            result = result + "destination:" + genre + '\n';
            result=result+""+'\n';
            result = result + user->getUsername() + ":" + user->allBooksByGenre(genre) + '\n';
            return result;
        }//wish to borrow book
        else if (messagevector.size()>=5 && messagevector[1]=="wish" && messagevector[3]=="borrow"){
            string bookname="";
            string result="";
            int x = messagevector.size();
            for(int i=4; i<x;i++){
                bookname=bookname+" "+messagevector[i];
            }
            //i want to check if I have this book
            if(user->hasBook(bookname,genre)){

                result=result+"SEND"+'\n';
                result=result+arr[3]+'\n';
                result=result+""+'\n';
                result=result+user->getUsername()+" has"+bookname+'\n';
                //sent result to server
                return result;

            }
            else{
                return " ";
            }
        } else if(messagevector.size()>=3 && messagevector[0]!=user->getUsername() && messagevector[1]=="has" && messagevector[2]!="added"){
                string owner = messagevector[0];
                string bookname="";
            int x = messagevector.size();
            for(int i=2; i<x;i++){
                bookname=bookname+" "+messagevector[i];
            }
            if(user->ifIwantToBorowThisBook(bookname)){

                Book *book=new Book(bookname,genre,owner);

                book->setCurrentusername(user->getUsername());
                user->addBook(book);
                user->dontWantToBorrowAnymore(bookname);
                //send: taking dune from jonh
                string result="";
                result=result+"SEND"+'\n';
                result=result+arr[3]+'\n';
                result=result+""+'\n';
                result=result+"Taking"+bookname+" from "+owner+'\n';
                //sent result to server
                return result;
            }
            else{
                return " ";
            }
        } else if (messagevector.size()>=4&& messagevector[0]=="Taking" && messagevector[messagevector.size()-1]==user->getUsername()){
            string bookname="";
            int x = messagevector.size()-2;
            for(int i=1; i<x;i++){
                bookname=bookname+" "+messagevector[i];
            }
            string s = "-"+user->getUsername();
            user->setBookNewCurrentUser(s,bookname,genre);
            return " ";

        }
        else if (messagevector.size()>=4&& messagevector[0]=="Returning" && messagevector[messagevector.size()-1]==user->getUsername()){
            string bookname="";
            int x = messagevector.size()-2;
            for(int i=1; i<x;i++){
                    bookname=bookname+" "+messagevector[i];
            }
            user->setBookNewCurrentUser(user->getUsername(),bookname,genre);

        }else{
            string result=" ";
            return result;
        }
    }
    else if (arr[0]=="ERROR"&& arr.size()>=3){
        string result="ERROR:";
        result=result+arr[1].substr(8);
        //print result to the screen
        return result;
    }
    else{
        return " ";
    }
    return " ";
}

