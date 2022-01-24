CXX=g++
CXXFLAGS=-lpthread

SRCS=tcp_load_clientside.cpp  tcp_serverside.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: client server

client: $(OBJS)
	$(CXX) tcp_load_clientside.cpp $(CXXFLAGS) -o client

server: $(OBJS)
	$(CXX) tcp_serverside.cpp $(CXXFLAGS) -o server

client.o: client.cpp

server.o: server.cpp
