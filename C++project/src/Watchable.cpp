
#include <string>
#include <vector>
#include "../include/Session.h"
#include "../include/Watchable.h"
#include <iostream>
using namespace std;

Watchable::Watchable(long id, int length, const std::vector<std::string>& tags):id(id),length(length),tags(tags){}
Watchable::~Watchable() {
    tags.clear();
}


Watchable::Watchable(const Watchable &other):id(other.getId()),length(other.length),tags(other.tags) {
}
const std::vector<std::string>& Watchable::getTags() const {
    return tags;
}
const int& Watchable::getLength() const {
    return length;
}
const long& Watchable::getId() const {
    return id;
}


Movie::Movie(long id, const std::string& name, int length, const std::vector<std::string>& tags):Watchable(id,length,tags),name(name){}

std::string Movie::toString() const {
    std::string output=name;
    return output;
}
std::string Movie::getName() const { return name;}
Watchable* Movie::getNextWatchable(Session & s) const {
    return nullptr;
}
Watchable* Movie::clone() {
    return new Movie(*this);
}

Episode::Episode(long id, const std::string& seriesName,int length, int season, int episode ,const std::vector<std::string>& tags):Watchable(id,length,tags),seriesName(seriesName),season(season),episode(episode),nextEpisodeId(id+1) {
}
Episode::Episode(const Episode &other):Watchable(other),seriesName(other.seriesName),season(other.season),episode(other.episode),nextEpisodeId(other.nextEpisodeId)  {
}
std::string Episode::toString() const {
    std::string output=""+seriesName+" S";
    if (season<10)
        output=output+"0"+to_string(season)+"E";
    else
        output=output+to_string(season)+"E";
    if (episode<10)
        output=output+"0"+to_string(episode)+" ";
    else
        output=output+to_string(episode)+" ";
    return output;

}
std::string Episode::getName() const { return seriesName;}
Watchable* Episode::getNextWatchable(Session &s) const {
    //if he has not next episode
    int x= s.getContent().size();
    if(x==getId()){
        return nullptr;
    }
    else{
        //if next id from the same series
        if(seriesName==s.getContent().at(getId())->getName()){
            return s.getContent().at(getId());
        } //if next series is another series
        else return nullptr;
    }
}
Watchable* Episode::clone() {
    return new Episode(*this);
}
