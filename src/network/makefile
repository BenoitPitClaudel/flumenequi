CXX=g++
CXXFLAGS=-lpthread

SRCS=client_test_mod.cpp multi_server_mod.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: client server

client: $(OBJS)
        $(CXX) client_test_mod.cpp $(CXXFLAGS) -o client

server: $(OBJS)
        $(CXX) multi_server_mod.cpp $(CXXFLAGS) -o server

client.o: client.cpp

server.o: server.cpp