#include <iostream>
#include <fstream>
#include <string>
#include <stdio.h>
#include <chrono>

//modify LOOP_SIZE to determine how often the program writes to file
//write to command line to determine how often you'd like the program to write out

using namespace std;

const int LOOP_SIZE = 1000;

int read_file();

void write_to_file(unsigned long long int data_recv[LOOP_SIZE], double times[LOOP_SIZE], int index);

//input var to specify number of times through outer loop
int main (int argc, char *argv[]){

    //check if variable specified
    int num_repeats;
    if(argc==1){
        num_repeats = 1;
    } else{
        num_repeats = stoi(argv[1]);
    }

    //initalise chronos
    chrono::time_point<std::chrono::system_clock> previous,current;
    std::chrono::duration<double> elapsed_seconds;
    previous = chrono::system_clock::now();

    for (size_t j = 0; j < num_repeats; j++){

        unsigned long long int data_recv[LOOP_SIZE];

        double times[LOOP_SIZE];

        //read data LOOP_SIZE times and measure time elapsed each iter
        for (size_t i = 0; i < LOOP_SIZE; i++){
            data_recv[i] = read_file();
            current = chrono::system_clock::now();
            elapsed_seconds = current - previous;
            //cout << elapsed_seconds.count() << "\n";
            previous = current;
            times[i] = elapsed_seconds.count();
        }
        //cout << sizeof(data_recv);

        write_to_file(data_recv, times, j);
    }
    
    //cout << "\nHello World, by the way" << data_recv;
    
    return 0;

}
void write_to_file(unsigned long long int data_recv[LOOP_SIZE], double times[LOOP_SIZE], int index){
    //make filename
    string filename = "fraction_RDMA_probe_"; 
    filename.append(to_string(index));
    //open file
    ofstream fid (filename);

    fid << "time,   data_recv\n";

    if(fid.is_open()){
        for (size_t i = 0; i < LOOP_SIZE; i++){ //measures datasizei
            //cout << "Gday I am " << i << "\n";
            fid << times[i] << "," << data_recv[i] << "\n";
        }
    }

    fid.close();    

    return;
}




int read_file (){

    FILE* fp;
    char buffer [128]; //max size dictated by 64 bit counter
    string recv;

    fp = popen("cat /sys/class/infiniband/mlx5_0/ports/1/counters/port_rcv_data","r");

    if (fp != NULL) {
        fgets(buffer, 128, fp);
    }
    recv = buffer;
    //cast to int
    unsigned long long int data_recv = stoull(recv);

    //clean up
    pclose(fp);

    return data_recv;
}
