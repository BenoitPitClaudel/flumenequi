// Server side C/C++ program to demonstrate Socket programming 
#include <unistd.h> 
#include <stdio.h> 
#include <sys/socket.h> 
#include <stdlib.h> 
#include <netinet/in.h> 
#include <string.h>
#include <thread>
#include <vector>
#include <iostream>
using namespace std;

//make global var buffer that is separate from 8 Byte local buffer and is commonly written to by everything
char glob_buffer[20000] = {0};
//larger than the text being sent

void function(int new_socket){
    char local_buffer[8] = {0};
    int valread;
    long long* f_size = new long long(0);
    valread = read(new_socket, local_buffer, 8);
    //cout << valread;
    ((char*)f_size)[0] = local_buffer[0];
    ((char*)f_size)[1] = local_buffer[1];
    ((char*)f_size)[2] = local_buffer[2];
    ((char*)f_size)[3] = local_buffer[3];
    ((char*)f_size)[4] = local_buffer[4];
    ((char*)f_size)[5] = local_buffer[5];
    ((char*)f_size)[6] = local_buffer[6];
    ((char*)f_size)[7] = local_buffer[7];
	//socket numbers are reused so if all goes well new_socket will be < ~200
    if(new_socket % 25 == 0){
		cout << "Socket Opened: " << new_socket << "for size " << *f_size << "B\n";  
	}
	//cout << *f_size << "\n";
    long long data_received = 0;
    int count = 0;
    while(data_received < *f_size){
        //cout << count << "\n";
	count++;
	valread = read(new_socket, glob_buffer, sizeof(glob_buffer));
		if(valread < 0){
			cerr << "Valread Invalid :" << errno << "\n";
		}
        data_received+=valread;
		//cout << data_received << "\n";
    } 
	if(shutdown(new_socket, SHUT_RDWR) < 0){
	    cerr<<"Error in shutdown\n";
    }
    if(close(new_socket) < 0){
	    cerr<<"Error in close\n";
    }
	if(new_socket % 25 == 0){
		cout << "Socket Closed for: " << new_socket << "\n";  
	}
    delete f_size;
}

int main(int argc, char const *argv[]) 
{ 
	int server_fd, new_socket, valread; 
	struct sockaddr_in address; 
	int opt = 1; 
    int PORT = atoi(argv[1]);
	int addrlen = sizeof(address); 
	char buffer[500000] = {0}; 
	char *hello = "Hello from server"; 
    int* f_size = new int(0);
	// Creating socket file descriptor 
	if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	// Forcefully attaching socket to the port 8080 
	if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, 
												&opt, sizeof(opt))) 
	{ 
		perror("setsockopt"); 
		exit(EXIT_FAILURE); 
	} 
	address.sin_family = AF_INET; 
	address.sin_addr.s_addr = INADDR_ANY; 
	address.sin_port = htons( PORT ); 
	
	// Forcefully attaching socket to the port 8080 
	if (bind(server_fd, (struct sockaddr *)&address, 
								sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	} 
	if (listen(server_fd, 100) < 0) 
	{ 
		perror("listen"); 
		exit(EXIT_FAILURE); 
	} 
    //std::vector<thread> threads;
    while(true){
	    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, 
					(socklen_t*)&addrlen))<0) 
	    { 
		    perror("accept"); 
		    exit(EXIT_FAILURE); 
	    }
        thread t1(function, new_socket);
	t1.detach();
        //threads.push_back(move(t1));
    }
    /*for(int iter=0; iter<threads.size(); iter++){
        threads[iter].join();
    }*/
	return 0; 
} 

