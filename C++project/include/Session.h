#ifndef SESSION_H_
#define SESSION_H_

#include <vector>
#include <unordered_map>
#include <string>
#include "Action.h"

class User;
class Watchable;

class Session{
public:
    Session(const std::string &configFilePath);
    Session(const Session& other);// copy constructor
    Session(Session &&other);// Move constructor
    Session& operator=(const Session &other); //Copy Assigment
    Session& operator=(Session&& other); //Move Assigment

    ~Session();//Distructor
    void clean();
    void copy(const Session &other);
    void move(Session &other);
    void setOtherNull(Session &other);
    void start();
    const std::vector<Watchable*>& getContent() const;
    std::vector<BaseAction*>& getActionLog();
    User& getActiveUser();
    std::unordered_map<std::string,User*>& getUserMap() ;
    void deleteUserFromMap(std::string &name);
    void setActiveUser(User* newActiveUser);
    void addUserToMap(User* newActiveUser,std::string &newname);
private:
    std::vector<Watchable*> content;
    std::vector<BaseAction*> actionsLog;
    std::unordered_map<std::string,User*> userMap;
    User* activeUser;
    int findChar(std::string s,char c);
};
#endif
