#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <stdio.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <unistd.h> 
#include <string.h> 
#include <ctime>
#include <mutex>
#include <fstream>
using namespace std;
chrono::high_resolution_clock::time_point start;
//vector<int> diff;
//vector<int> fstart;
//vector<int> fct;
int num_flows;
int window_duration = 100000;
std::vector<int> start_time;
std::vector<long long> fsize;
std::vector<int> dst;
int num_helper_threads = 3;

int REST_TIME = 5;

long long data_sent=0;  // data sent in bytes (without including pkt headers)
int probe_period=1000;  // probe period in milliseconds
bool stop_probe=false;  // flag to stop the probe thread
std::mutex counter_lock;
std::mutex stop_lock;

char glob_content[] = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate, ex vitae ultrices dapibus, orci ipsum molestie lacus, ut rutrum urna eros et ante. Curabitur rhoncus laoreet lacus vitae sollicitudin. Nunc accumsan risus libero, at convallis est interdum vel. Aliquam placerat felis purus, nec sagittis magna ullamcorper et. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque tellus nisl, efficitur a luctus at, ullamcorper eu ipsum. Cras nec enim nec nunc lobortis pharetra. Donec ac erat fermentum, malesuada sapien ut, consectetur orci.\
Nam nec finibus velit. Maecenas feugiat orci turpis, eu dignissim elit hendrerit vitae. Vestibulum at lorem eget justo rhoncus rhoncus. Morbi ac magna sit amet orci interdum ultrices et eget augue. Praesent pretium auctor lacus eget volutpat. Cras ultrices nibh sit amet est volutpat venenatis. Sed leo est, tristique id blandit vel, suscipit malesuada ante. Nunc finibus velit vitae egestas feugiat. Mauris condimentum purus nec risus ornare maximus. Sed in pulvinar odio. Fusce dui odio, porttitor vel condimentum vitae, iaculis in nisi. Quisque porttitor felis leo, a eleifend risus pretiu\
m et. Sed ac vehicula massa. Nulla lorem diam, maximus vel quam quis, varius pretium ante. In rhoncus tincidunt placerat. Donec gravida nisl sed augue bibendum malesuada. Mauris venenatis nisl et odio placerat, ac ullamcorper ipsum commodo. Donec sodales nibh id sem lobortis, vitae varius mi sollicitudin. Suspendisse vulputate aliquet arcu, ac egestas nisl sagittis tristique. Nam a libero ac neque convallis laoreet in ac lorem. Fusce sit amet risus dui. Vestibulum eu semper massa. Duis rutrum tortor quis nisl faucibus hendrerit. Aliquam dignissim eros ut turpis lacinia, molestie iaculi\
s sapien dapibus. Aliquam commodo, arcu at pharetra tincidunt, ex felis eleifend tellus, nec dignissim leo diam eget enim. Praesent nec diam turpis. Phasellus a neque at diam faucibus semper. Curabitur et consequat mi, id blandit dolor. Pellentesque nec rhoncus eros. Etiam porttitor quis turpis id consectetur. Suspendisse potenti. Donec malesuada enim in tempor maximus. Nam ut dui a ex condimentum pulvinar faucibus sed risus. Aenean condimentum nibh vulputate faucibus eleifend. Sed sit amet mollis purus. Morbi commodo ex ipsum, et consequat augue interdum eget. Sed et tellus tempor, eu\
ismod sem et, auctor mi. Donec scelerisque magna metus, quis tristique eros semper eu. Cras et nunc at neque dapibus laoreet et at mauris. Integer velit neque, imperdiet non vestibulum id, molestie eget neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse accumsan tortor id magna lacinia, nec facilisis nibh rutrum. Phasellus facilisis quam felis, mollis varius massa aliquet vitae. Cras quis lorem erat. Curabitur neque velit, tempor a auctor et, facilisis non nulla. Nullam aliquet urna sed pulvinar commodo. Integer convallis sodales \
mi, sed congue est iaculis in. Vivamus tristique neque quis laoreet tempor.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate, ex vitae ultrices dapibus, orci ipsum molestie lacus, ut rutrum urna eros et ante. Curabitur rhoncus laoreet lacus vitae sollicitudin. Nunc accumsan risus libero, at convallis est interdum vel. Aliquam placerat felis purus, nec sagittis magna ullamcorper et. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque tellus nisl, efficitur a luctus at, ullamcorper eu ipsum. Cras nec enim nec nunc lobortis pharetra. Donec ac er\
at fermentum, malesuada sapien ut, consectetur orci. Nam nec finibus velit. Maecenas feugiat orci turpis, eu dignissim elit hendrerit vitae. Vestibulum at lorem eget justo rhoncus rhoncus. Morbi ac magna sit amet orci interdum ultrices et eget augue. Praesent pretium auctor lacus eget volutpat. Cras ultrices nibh sit amet est volutpat venenatis. Sed leo est, tristique id blandit vel, suscipit malesuada ante. Nunc finibus velit vitae egestas feugiat. Mauris condimentum purus nec risus ornare maximus. Sed in pulvinar odio. Fusce dui odio, porttitor vel condimentum vitae, iaculis in nisi \
Quisque porttitor felis leo, a eleifend risus pretium et. Sed ac vehicula massa. Nulla lorem diam, maximus vel quam quis, varius pretium ante. In rhoncus tincidunt placerat. Donec gravida nisl sed augue bibendum malesuada. Mauris venenatis nisl et odio placerat, ac ullamcorper ipsum commodo. Donec sodales nibh id sem lobortis, vitae varius mi sollicitudin. Suspendisse vulputate aliquet arcu, ac egestas nisl sagittis tristique. Nam a libero ac neque convallis laoreet in ac lorem. Fusce sit amet risus dui. Vestibulum eu semper massa. Duis rutrum tortor quis nisl faucibus hendrerit. Aliqu\
am dignissim eros ut turpis lacinia, molestie iaculi sapien dapibus. Aliquam commodo, arcu at pharetra tincidunt, ex felis eleifend tellus, nec dignissim leo diam eget enim. Praesent nec diam turpis. Phasellus a neque at diam faucibus semper. Curabitur et consequat mi, id blandit dolor. Pellentesque nec rhoncus eros. Etiam porttitor quis turpis id consectetur. Suspendisse potenti. Donec malesuada enim in tempor maximus. Nam ut dui a ex condimentum pulvinar faucibus sed risus. Aenean condimentum nibh vulputate faucibus eleifend. Sed sit amet mollis purus. Morbi commodo ex ipsum, et cons\
equat augue interdum eget. Sed et tellus tempor, euismod sem et, auctor mi. Donec scelerisque magna metus, quis tristique eros semper eu. Cras et nunc at neque dapibus laoreet et at mauris. Integer velit neque, imperdiet non vestibulum id, molestie eget neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse accumsan tortor id magna lacinia, nec facilisis nibh rutrum. Phasellus facilisis quam felis, mollis varius massa aliquet vitae. Cras quis lorem erat. Curabitur neque velit, tempor a auctor et, facilisis non nulla. Nullam aliquet ur\
na sed pulvinar commodo. Integer convallis sodales mi, sed congue est iaculis in. Vivamus tristique neque quis laoreet tempor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate, ex vitae ultrices dapibus, orci ipsum molestie lacus, ut rutrum urna eros et ante. Curabitur rhoncus laoreet lacus vitae sollicitudin. Nunc accumsan risus libero, at convallis est interdum vel. Aliquam placerat felis purus, nec sagittis magna ullamcorper et. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque tellus nisl, efficitur a luctus at, ullamcorper eu ipsum. C\
ras nec enim nec nunc lobortis pharetra. Donec ac erat fermentum, malesuada sapien ut, consectetur orci. Nam nec finibus velit. Maecenas feugiat orci turpis, eu dignissim elit hendrerit vitae. Vestibulum at lorem eget justo rhoncus rhoncus. Morbi ac magna sit amet orci interdum ultrices et eget augue. Praesent pretium auctor lacus eget volutpat. Cras ultrices nibh sit amet est volutpat venenatis. Sed leo est, tristique id blandit vel, suscipit malesuada ante. Nunc finibus velit vitae egestas feugiat. Mauris condimentum purus nec risus ornare maximus. Sed in pulvinar odio. Fusce dui odi\
o, porttitor vel condimentum vitae, iaculis in nisi Quisque porttitor felis leo, a eleifend risus pretium et. Sed ac vehicula massa. Nulla lorem diam, maximus vel quam quis, varius pretium ante. In rhoncus tincidunt placerat. Donec gravida nisl sed augue bibendum malesuada. Mauris venenatis nisl et odio placerat, ac ullamcorper ipsum commodo. Donec sodales nibh id sem lobortis, vitae varius mi sollicitudin. Suspendisse vulputate aliquet arcu, ac egestas nisl sagittis tristique. Nam a libero ac neque convallis laoreet in ac lorem. Fusce sit amet risus dui. Vestibulum eu semper massa. Du\
is rutrum tortor quis nisl faucibus hendrerit. Aliquam dignissim eros ut turpis lacinia, molestie iaculi sapien dapibus. Aliquam commodo, arcu at pharetra tincidunt, ex felis eleifend tellus, nec dignissim leo diam eget enim. Praesent nec diam turpis. Phasellus a neque at diam faucibus semper. Curabitur et consequat mi, id blandit dolor. Pellentesque nec rhoncus eros. Etiam porttitor quis turpis id consectetur. Suspendisse potenti. Donec malesuada enim in tempor maximus. Nam ut dui a ex condimentum pulvinar faucibus sed risus. Aenean condimentum nibh vulputate faucibus eleifend. Sed si\
t amet mollis purus. Morbi commodo ex ipsum, et consequat augue interdum eget. Sed et tellus tempor, euismod sem et, auctor mi. Donec scelerisque magna metus, quis tristique eros semper eu. Cras et nunc at neque dapibus laoreet et at mauris. Integer velit neque, imperdiet non vestibulum id, molestie eget neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse accumsan tortor id magna lacinia, nec facilisis nibh rutrum. Phasellus facilisis quam felis, mollis varius massa aliquet vitae. Cras quis lorem erat. Curabitur neque velit, tempor\
a auctor et, facilisis non nulla. Nullam aliquet urna sed pulvinar commodo. Integer convallis sodales mi, sed congue est iaculis in. Vivamus tristique neque quis laoreet tempor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate, ex vitae ultrices dapibus, orci ipsum molestie lacus, ut rutrum urna eros et ante. Curabitur rhoncus laoreet lacus vitae sollicitudin. Nunc accumsan risus libero, at convallis est interdum vel. Aliquam placerat felis purus, nec sagittis magna ullamcorper et. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque tellus \
nisl, efficitur a luctus at, ullamcorper eu ipsum. Cras nec enim nec nunc lobortis pharetra. Donec ac erat fermentum, malesuada sapien ut, consectetur orci. Nam nec finibus velit. Maecenas feugiat orci turpis, eu dignissim elit hendrerit vitae. Vestibulum at lorem eget justo rhoncus rhoncus. Morbi ac magna sit amet orci interdum ultrices et eget augue. Praesent pretium auctor lacus eget volutpat. Cras ultrices nibh sit amet est volutpat venenatis. Sed leo est, tristique id blandit vel, suscipit malesuada ante. Nunc finibus velit vitae egestas feugiat. Mauris condimentum purus nec risu\
s ornare maximus. Sed in pulvinar odio. Fusce dui odio, porttitor vel condimentum vitae, iaculis in nisi Quisque porttitor felis leo, a eleifend risus pretium et. Sed ac vehicula massa. Nulla lorem diam, maximus vel quam quis, varius pretium ante. In rhoncus tincidunt placerat. Donec gravida nisl sed augue bibendum malesuada. Mauris venenatis nisl et odio placerat, ac ullamcorper ipsum commodo. Donec sodales nibh id sem lobortis, vitae varius mi sollicitudin. Suspendisse vulputate aliquet arcu, ac egestas nisl sagittis tristique. Nam a libero ac neque convallis laoreet in ac lorem. Fu\
sce sit amet risus dui. Vestibulum eu semper massa. Duis rutrum tortor quis nisl faucibus hendrerit. Aliquam dignissim eros ut turpis lacinia, molestie iaculi sapien dapibus. Aliquam commodo, arcu at pharetra tincidunt, ex felis eleifend tellus, nec dignissim leo diam eget enim. Praesent nec diam turpis. Phasellus a neque at diam faucibus semper. Curabitur et consequat mi, id blandit dolor. Pellentesque nec rhoncus eros. Etiam porttitor quis turpis id consectetur. Suspendisse potenti. Donec malesuada enim in tempor maximus. Nam ut dui a ex condimentum pulvinar faucibus sed risus. Aenea\
n condimentum nibh vulputate faucibus eleifend. Sed sit amet mollis purus. Morbi commodo ex ipsum, et consequat augue interdum eget. Sed et tellus tempor, euismod sem et, auctor mi. Donec scelerisque magna metus, quis tristique eros semper eu. Cras et nunc at neque dapibus laoreet et at mauris. Integer velit neque, imperdiet non vestibulum id, molestie eget neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse accumsan tortor id magna lacinia, nec facilisis nibh rutrum. Phasellus facilisis quam felis, mollis varius massa aliquet vita\
e. Cras quis lorem erat. Curabitur neque velit, tempora auctor et, facilisis non nulla. Nullam aliquet urna sed pulvinar commodo. Integer convallis sodales mi, sed congue est iaculis in. Vivamus tristique neque quis laoreet tempor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate, ex vitae ultrices dapibus, orci ipsum molestie lacus, ut rutrum urna eros et ante. Curabitur rhoncus laoreet lacus vitae sollicitudin. Nunc accumsan risus libero, at convallis est interdum vel. Aliquam placerat felis purus, nec sagittis magna ullamcorper et. Interdum et malesuada fames a\
c ante ipsum primis in faucibus. Pellentesque tellus nisl, efficitur a luctus at, ullamcorper eu ipsum. Cras nec enim nec nunc lobortis pharetra. Donec ac erat fermentum, malesuada sapien ut, consectetur orci. Nam nec finibus velit. Maecenas feugiat orci turpis, eu dignissim elit hendrerit vitae. Vestibulum at lorem eget justo rhoncus rhoncus. Morbi ac magna sit amet orci interdum ultrices et eget augue. Praesent pretium auctor lacus eget volutpat. Cras ultrices nibh sit amet est volutpat venenatis. Sed leo est, tristique id blandit vel, suscipit malesuada ante. Nunc finibus velit vita\
e egestas feugiat. Mauris condimentum purus nec risus ornare maximus. Sed in pulvinar odio. Fusce dui odio, porttitor vel condimentum vitae, iaculis in nisi Quisque porttitor felis leo, a eleifend risus pretium et. Sed ac vehicula massa. Nulla lorem diam, maximus vel quam quis, varius pretium ante. In rhoncus tincidunt placerat. Donec gravida nisl sed augue bibendum malesuada. Mauris venenatis nisl et odio placerat, ac ullamcorper ipsum commodo. Donec sodales nibh id sem lobortis, vitae varius mi sollicitudin. Suspendisse vulputate aliquet arcu, ac egestas nisl sagittis tristique. Nam \
a libero ac neque convallis laoreet in ac lorem. Fusce sit amet risus dui. Vestibulum eu semper massa. Duis rutrum tortor quis nisl faucibus hendrerit. Aliquam dignissim eros ut turpis lacinia, molestie iaculi sapien dapibus. Aliquam commodo, arcu at pharetra tincidunt, ex felis eleifend tellus, nec dignissim leo diam eget enim. Praesent nec diam turpis. Phasellus a neque at diam faucibus semper. Curabitur et consequat mi, id blandit dolor. Pellentesque nec rhoncus eros. Etiam porttitor quis turpis id consectetur. Suspendisse potenti. Donec malesuada enim in tempor maximus. Nam ut dui \
a ex condimentum pulvinar faucibus sed risus. Aenean condimentum nibh vulputate faucibus eleifend. Sed sit amet mollis purus. Morbi commodo ex ipsum, et consequat augue interdum eget. Sed et tellus tempor, euismod sem et, auctor mi. Donec scelerisque magna metus, quis tristique eros semper eu. Cras et nunc at neque dapibus laoreet et at mauris. Integer velit neque, imperdiet non vestibulum id, molestie eget neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse accumsan tortor id magna lacinia, nec facilisis nibh rutrum. Phasellus fac\
ilisis quam felis, mollis varius massa aliquet vitae. Cras quis lorem erat. Curabitur neque velit, tempora auctor et, facilisis non nulla. Nullam aliquet urna sed pulvinar commodo. Integer convallis sodales mi, sed congue est iaculis in. Vivamus tristique neque quis laoreet tempor. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate, ex vitae ultrices dapibus, orci ipsum molestie lacus, ut rutrum urna eros et ante. Curabitur rhoncus laoreet lacus vitae sollicitudin. Nunc accumsan risus libero, at convallis est interdum vel. Aliquam placerat felis purus, nec sagittis \
magna ullamcorper et. Interdum et malesuada fames ac ante ipsum primis in faucibus. Pellentesque tellus nisl, efficitur a luctus at, ullamcorper eu ipsum. Cras nec enim nec nunc lobortis pharetra. Donec ac erat fermentum, malesuada sapien ut, consectetur orci. Nam nec finibus velit. Maecenas feugiat orci turpis, eu dignissim elit hendrerit vitae. Vestibulum at lorem eget justo rhoncus rhoncus. Morbi ac magna sit amet orci interdum ultrices et eget augue. Praesent pretium auctor lacus eget volutpat. Cras ultrices nibh sit amet est volutpat venenatis. Sed leo est, tristique id blandit ve\
l, suscipit malesuada ante. Nunc finibus velit vitae egestas feugiat. Mauris condimentum purus nec risus ornare maximus. Sed in pulvinar odio. Fusce dui odio, porttitor vel condimentum vitae, iaculis in nisi Quisque porttitor felis leo, a eleifend risus pretium et. Sed ac vehicula massa. Nulla lorem diam, maximus vel quam quis, varius pretium ante. In rhoncus tincidunt placerat. Donec gravida nisl sed augue bibendum malesuada. Mauris venenatis nisl et odio placerat, ac ullamcorper ipsum commodo. Donec sodales nibh id sem lobortis, vitae varius mi sollicitudin. Suspendisse vulputate ali\
quet arcu, ac egestas nisl sagittis tristique. Nam a libero ac neque convallis laoreet in ac lorem. Fusce sit amet risus dui. Vestibulum eu semper massa. Duis rutrum tortor quis nisl faucibus hendrerit. Aliquam dignissim eros ut turpis lacinia, molestie iaculi sapien dapibus. Aliquam commodo, arcu at pharetra tincidunt, ex felis eleifend tellus, nec dignissim leo diam eget enim. Praesent nec diam turpis. Phasellus a neque at diam faucibus semper. Curabitur et consequat mi, id blandit dolor. Pellentesque nec rhoncus eros. Etiam porttitor quis turpis id consectetur. Suspendisse potenti. \
Donec malesuada enim in tempor maximus. Nam ut dui a ex condimentum pulvinar faucibus sed risus. Aenean condimentum nibh vulputate faucibus eleifend. Sed sit amet mollis purus. Morbi commodo ex ipsum, et consequat augue interdum eget. Sed et tellus tempor, euismod sem et, auctor mi. Donec scelerisque magna metus, quis tristique eros semper eu. Cras et nunc at neque dapibus laoreet et at mauris. Integer velit neque, imperdiet non vestibulum id, molestie eget neque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Suspendisse accumsan tortor id magn\
a lacinia, nec facilisis nibh rutrum. Phasellus facilisis quam felis, mollis varius massa aliquet vitae. Cras quis lorem erat. Curabitur neque velit, tempora auctor et, facilisis non nulla. Nullam aliquet urna sed pulvinar commodo. Integer convallis sodales mi, sed congue est iaculis in. Vivamus tristique neque quis laoreet tempor.";

void function_(int time, int index, long long size, int dst, int sock, int PORT){
    int valread; 
    struct sockaddr_in serv_addr;
    char local_buffer[8] = {0};

	
    serv_addr.sin_family = AF_INET; 
    serv_addr.sin_port = htons(PORT);
    /*if(index > 32000 & (index  %100) == 0 ){
	    cerr<<index<<"\n";
    }*/
    
    // Convert IPv4 and IPv6 addresses from text to binary form 
    //if(inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr)<=0)
    if(dst == 0){
        if(inet_pton(AF_INET, "172.32.9.1", &serv_addr.sin_addr)<=0){
		cerr<<"inet_error\n";
		return;
	}
    }
    else if(dst == 1){
        if(inet_pton(AF_INET, "172.32.10.1", &serv_addr.sin_addr)<=0){
		cerr<<"inet_error\n";
		return;
	}
    }
    else if(dst == 2){
        if(inet_pton(AF_INET, "172.32.11.1", &serv_addr.sin_addr)<=0){
		cerr<<"inet_error\n";
		return;
	}
    }
    else{
        if(inet_pton(AF_INET, "172.32.12.1", &serv_addr.sin_addr)<=0){
		cerr<<"inet_error\n";
		return;
	}
    }
	//
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
	return;
    }
    long long file_size;
    file_size = size;
    local_buffer[0] = ((char*)(&file_size))[0];
    local_buffer[1] = ((char*)(&file_size))[1];
    local_buffer[2] = ((char*)(&file_size))[2];
    local_buffer[3] = ((char*)(&file_size))[3];
    local_buffer[4] = ((char*)(&file_size))[4];
    local_buffer[5] = ((char*)(&file_size))[5];
    local_buffer[6] = ((char*)(&file_size))[6];
    local_buffer[7] = ((char*)(&file_size))[7];
    send(sock, local_buffer, 8, 0);
    //delete file_size;
    long long bytes_sent = 0;
    unsigned long int chunk_size = sizeof(glob_content);
	//
    chrono::high_resolution_clock::time_point current = chrono::high_resolution_clock::now();
    auto elapsed_ = chrono::duration_cast<chrono::microseconds>(current - start);
    //if(elapsed_.count() + 600 < time){
    //    chrono::microseconds dura(time - elapsed_.count() - 600);
    //    this_thread::sleep_for(dura);
    //}

    //bool not_elapsed = true;
    //while(not_elapsed){
    //    chrono::high_resolution_clock::time_point t3 = chrono::high_resolution_clock::now();
    //    auto elapsed_ = std::chrono::duration_cast<std::chrono::microseconds>(t3 - start);
    //    not_elapsed = elapsed_.count() < time;
    //}
    //
    //char content[] = "Gday curd nerds, yeah nah glad it's working";
    //unsigned int sizeofcontents = sizeof(content);

    chrono::microseconds sleepy(REST_TIME);

    while(bytes_sent < size){
        int send_r;
        if(size - bytes_sent < chunk_size){
                send_r = send(sock, glob_content, size - bytes_sent, 0);
                if(send_r < 0){
                    cerr << "Sending negative bytes\n";
                }
                bytes_sent += send_r;
            }
            else{
                send_r = send(sock, glob_content, chunk_size, 0);
                bytes_sent += send_r;
            }
        this_thread::sleep_for(sleepy);
	//cout << send_r << "\n";
	//cout << bytes_sent<<"\n";
    }

    counter_lock.lock();
    data_sent += size + 8;
    counter_lock.unlock();

    this_thread::sleep_for(sleepy);

    if(shutdown(sock, SHUT_RDWR) < 0){
	    cerr<<"Error in shutdown\n";
    }
    if(close(sock) < 0){
	    cerr<<"Error in close\n";
    }

    //diff[index] =  elapsed.count() - time;
    //fstart[index] = elapsed1.count();
    //fct[index] = elapsed2.count();
    if (index % 200 == 0){
        std:cerr<< "Finished Flow and Killed Socket: " << index << "\n";
    }
}

void helper_thread(int index){
    int sock;
    int port  = 818080+index;
    //std::vector<thread> threads;
    //threads.reserve(num_flows/num_helper_threads + 2);
    int start_point = start_time[0];
    int stop_point = start_point + 2*window_duration;
    for(int i=index; i<num_flows; i+=num_helper_threads){
    	if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    	{
        	//printf("\n Socket creation error \n");
		std::cerr<< "Socket creation error: "<<errno<<": "<<strerror(errno)<<"\n";
        	if(errno == EMFILE){
                	std::cerr<<"per-process limit reached\n";
        	}
        	if(errno  == ENFILE){
                	std::cerr<<"system-wide limit reached\n";
        	}
		continue;
    	}
        if (i % 200 == 0){
            std::cerr<<"Starting Flow for : "<<i<<" target_time: "<<start_time[i]<< " actual~time: "<< stop_point <<" size: "<<fsize[i]<<"B\n";
        }
        thread t1(function_, start_time[i], i, fsize[i], dst[i], sock, port);
        t1.detach();

            //threads.push_back(move(t1));
        if(start_time[i] > stop_point){
            while(stop_point + window_duration < start_time[i]){
                start_point += window_duration;
                stop_point += window_duration;
            }
            chrono::high_resolution_clock::time_point current = chrono::high_resolution_clock::now();
            auto elapsed_ = chrono::duration_cast<chrono::microseconds>(current - start);
            if(elapsed_.count() + 1000 < start_point){
                chrono::microseconds dura(start_point - elapsed_.count() - 1000);
                this_thread::sleep_for(dura);
                bool sleep = true;
                while(sleep){
                    chrono::high_resolution_clock::time_point cur = chrono::high_resolution_clock::now();
                    auto elap_ = chrono::duration_cast<chrono::microseconds>(cur - start);
                    if(elap_.count() + 1000 > start_point)
                        {
                        //std::cerr<<"Slept till"<<elap_.count()<<" "<<i<<endl;
                        sleep = false;
                        }
                }
                start_point += window_duration;
                stop_point += window_duration;
                }
        }
    }
    //chrono::high_resolution_clock::time_point t_ = chrono::high_resolution_clock::now();
    //auto elapsed_ = std::chrono::duration_cast<std::chrono::microseconds>(t_ - start);
    /*for(int i=0; i<threads.size(); i++){
        threads[i].join();
    }*/
}

void probe_thread() {
    std::vector<float> bandwidth;   // bandwidth in Gbps
    std::vector<chrono::high_resolution_clock::time_point> time_stamp;
    chrono::high_resolution_clock::time_point current = chrono::high_resolution_clock::now();
    bool stop = false;
    chrono::milliseconds duration(probe_period);
    while(!stop) {
        long long total_data = 0;
        counter_lock.lock();
        total_data = data_sent;
        data_sent = 0;
        counter_lock.unlock();
        float bw = float(total_data)*8 / (float(probe_period)*1.0e6);
        bandwidth.push_back(bw);
	time_stamp.push_back(chrono::high_resolution_clock::now());
        stop_lock.lock();
        stop = stop_probe;
        stop_lock.unlock();
        this_thread::sleep_for(duration);
    }
    // write bw measure to file
    fstream file_handle;
    file_handle.open("bw.txt", ios::trunc | ios::out);
    for(int iter=0; iter<bandwidth.size(); iter++) {
        file_handle<<bandwidth[iter]<<" "<< (chrono::duration_cast<chrono::milliseconds>(time_stamp[iter] - current)).count()<<"\n";
    }
    file_handle<<bandwidth.size()<<"\n";
    file_handle.close();
    return;
}

int main(){
    int sock;
    cin>>num_flows;
    start_time = vector<int>(num_flows, 0);
    fsize = std::vector<long long>(num_flows, 0);
    dst = std::vector<int>(num_flows, 0);
    std::vector<thread> threads;
    threads.reserve(num_helper_threads);
    for(int i=0; i<num_flows; i++){
        cin>>start_time[i]>>fsize[i]>>dst[i];
	start_time[i]+=2000000;
    }
    start = chrono::high_resolution_clock::now();
    //for(int i=0; i<num_helper_threads; i++){
    thread bw_thread(probe_thread);
    for(int i=0; i<num_helper_threads; i++){
        thread t1(helper_thread, i);
        threads.push_back(move(t1));
    }
    //chrono::high_resolution_clock::time_point t_ = chrono::high_resolution_clock::now();
    //auto elapsed_ = std::chrono::duration_cast<std::chrono::microseconds>(t_ - start);
    for(int i=0; i<threads.size(); i++){
        threads[i].join();
    }
    chrono::microseconds dura__(10000000);
    this_thread::sleep_for(dura__);
    //for(int i=0; i<diff.size();i++){
	//    cout<<fstart[i]<<" "<<diff[i]<<" "<<dst[i]<<" "<<fsize[i]<<" "<<fct[i]<<"\n";
    //}
    //cout<<"Time for threads:"<<elapsed_.count()<<"\n";

    stop_lock.lock();
    stop_probe = true;
    stop_lock.unlock();
    bw_thread.join();

    auto curtime = chrono::system_clock::to_time_t(chrono::system_clock::now());
    std::cout << "Client finished sending data at" << std::ctime(&curtime) << "\n";
    return 0;
}

