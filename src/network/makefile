CXX=g++
CXXFLAGS=-lpthread

SRCS=tcp_load_clientside.cpp  tcp_serverside.cpp
OBJS=$(subst .cpp,.o,$(SRCS))

all: tcp udp

tcp: tcp_client tcp_server

tcp_client: $(OBJS)
	$(CXX) tcp_load_clientside.cpp $(CXXFLAGS) -o tcp_client

tcp_server: $(OBJS)
	$(CXX) tcp_serverside.cpp $(CXXFLAGS) -o tcp_server

client.o: client.cpp

server.o: server.cpp
udp_client: $(OBJS)
	        $(CXX) udp_clientside.cpp $(CXXFLAGS) -o client

udp_server: $(OBJS)
	        $(CXX) udp_serverside.cpp $(CXXFLAGS) -o server
udp: udp_client udp_server
