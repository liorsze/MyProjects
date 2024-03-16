#include <stdlib.h>
#include <../include/connectionHandler.h>
#include <thread>
#include <istream>

using  namespace std;

ConnectionHandler* connectionHandler;
StompEncoderDecoder* encoderDecoder;

void readFromServer(){
    std::string answer;
    while (true) {
        if (!connectionHandler->getLine(answer)) {
            std::cout << "ERROR: Could not connect to the server1\n" << std::endl;
            break;
        }

        if(answer.substr(0,7)=="MESSAGE"){
            vector<string> arr;
            stringstream ss(answer);
            std::string segment;

            while(std::getline(ss, segment, '\n'))
            {
                arr.push_back(segment);
            }
            string genre = arr[3].substr(arr[3].find(':')+1);
            cout<<genre<<":"<<arr[5]<<endl;
        }

        string recived = encoderDecoder->messageToString(answer);

        if(recived==" "){

        }else if(recived.substr(0,4)=="SEND") {//send frame
            if (!connectionHandler->sendFrameAscii(recived, '\0')) {
                std::cout << "ERROR: Could not connect to the server2\n" << std::endl;
            }
        }else{ // print message to screen
            std::cout<<recived<<endl;
        }
        int len = answer.length();
        answer.resize(len - 1);

        if (recived == "LOGOUT") {
            std::cout << "Exiting...\n" << std::endl;
            break;
        }
        answer="";
    }

}

int main (int argc, char *argv[]) {
    User *user;

    string str;
    std::string host;
    int port=0;

    encoderDecoder=new StompEncoderDecoder;


    while (true){
        getline(cin,str);
        vector<string> arr;
        stringstream ss(str);
        std::string segment;

        while(std::getline(ss, segment, ' '))
        {
            arr.push_back(segment);
        }

        if(arr[0]=="login" && arr.size()==4){
            host=arr[1].substr(0,arr[1].find(':'));

            string s =arr[1].substr(arr[1].find(':')+1);
            stringstream geek(s);
            geek >> port;

            user = new User(arr[2], arr[3]);

            encoderDecoder->setUser(user);

            connectionHandler= new ConnectionHandler(host, port,*encoderDecoder);
            if (!connectionHandler->connect()) {
                std::cout << "ERROR: Could not connect to the server3\n" << std::endl;
                delete encoderDecoder;
                delete connectionHandler;
                delete user;
                return 1;
            }
            if (!connectionHandler->sendLine(str)) {
                std::cout << "ERROR: Could not connect to the server4\n" << std::endl;
            }
            string answer;
            if (!connectionHandler->getLine(answer)) {
                std::cout << "ERROR: Could not connect to the server1\n" << std::endl;
                break;
            }
            string recived = encoderDecoder->messageToString(answer);
            if(answer.substr(0,5)!="ERROR"){
                std::cout<<recived<< std::endl;
                break;
            }else{//error
                std::cout<<recived << std::endl;
                delete connectionHandler;
                delete user;
            }

        } else {
            std::cout<<"Please login first" << std::endl;
        }
    }



    thread readThread(readFromServer);
    while (true) {
        const short bufsize = 1024;
        char buf[bufsize];

        std::cin.getline(buf, bufsize);

        std::string line(buf);

        if (!connectionHandler->sendLine(line)) {
            std::cout << "ERROR:Could not connect to the server5\n" << std::endl;
            delete encoderDecoder;
            delete connectionHandler;
            delete user;
            return 0;
        }
        if(line=="logout"){
            break;
        }
    }
    readThread.join();
    delete encoderDecoder;
    delete connectionHandler;
    delete user;
    return 0;
}