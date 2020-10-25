CFLAGS:=-c -Wall -Weffc++ -g -std=c++11 -Iinclude
LDFLAGS:=-lboost_system
CFLAGS += -pthread
LDFLAGS += -pthread

all: StompBookClubClient
	g++ -o bin/StompBookClubClient bin/connectionHandler.o bin/Book.o bin/StompEncoderDecoder.o bin/User.o bin/StompClient.o $(LDFLAGS) 

StompBookClubClient: bin/connectionHandler.o bin/Book.o bin/StompEncoderDecoder.o bin/User.o bin/StompClient.o
	
bin/connectionHandler.o: src/connectionHandler.cpp
	g++ $(CFLAGS) -o bin/connectionHandler.o src/connectionHandler.cpp

bin/Book.o: src/Book.cpp
	g++ $(CFLAGS) -o bin/Book.o src/Book.cpp
	
bin/StompEncoderDecoder.o: src/StompEncoderDecoder.cpp
	g++ $(CFLAGS) -o bin/StompEncoderDecoder.o src/StompEncoderDecoder.cpp

bin/User.o: src/User.cpp
	g++ $(CFLAGS) -o bin/User.o src/User.cpp

bin/StompClient.o: src/StompClient.cpp
	g++ $(CFLAGS) -o bin/StompClient.o src/StompClient.cpp
	
.PHONY: clean
clean:
	rm -f bin/*
