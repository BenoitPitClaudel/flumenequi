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
#include <arpa/inet.h>
#include <fstream>
using namespace std;

#define MAXLINE 20000
int main(int argc, char const *argv[]) 
{ 
	int server_fd, new_socket, n, len; 
	struct sockaddr_in address, client_addr; 
	int PORT = atoi(argv[1]);
	char buffer[MAXLINE];
	// Creating socket file descriptor 
	if ((server_fd = socket(AF_INET, SOCK_DGRAM, 0)) == 0) 
	{ 
		perror("socket failed"); 
		exit(EXIT_FAILURE); 
	} 
	
	address.sin_family = AF_INET; 
	//inet_pton(AF_INET, "172.32.11.1", &address.sin_addr);
	address.sin_addr.s_addr = INADDR_ANY;
	address.sin_port = htons( PORT ); 
	len = sizeof(client_addr);
	if (bind(server_fd, (const struct sockaddr *)&address, sizeof(address))<0) 
	{ 
		perror("bind failed"); 
		exit(EXIT_FAILURE); 
	}
	long long probe_period_data;
	int number_of_packets_received = 0;
	fstream file_handle;
	long long probe_duration = 30000;
	chrono::high_resolution_clock::time_point probe_period_start = chrono::high_resolution_clock::now();
	long long probe_sequence_time;
	printf("coucou");
	while(true){
		n = recvfrom(server_fd, (char *)buffer, MAXLINE, MSG_WAITALL, (struct sockaddr *) &client_addr, (socklen_t*) &len);
		if (n > 0) {
			number_of_packets_received += 1;
		} else if (n == 0) {
			printf(" received empty packet");
		} else {
			printf("received negative bytes %d", n);
		}

		probe_period_data += n;
		probe_sequence_time = (chrono::duration_cast<chrono::milliseconds>(chrono::high_resolution_clock::now() - probe_period_start)).count();
		if (probe_sequence_time >= probe_duration){
			file_handle.open("server_received_bytes", fstream::app | fstream::out);
			file_handle<<probe_sequence_time<<" "<<number_of_packets_received<<" "<<probe_period_data<<"\n";
			file_handle.close();
			probe_period_start = chrono::high_resolution_clock::now();
			probe_period_data = 0;
		}
	}
	return 0; 
} 

