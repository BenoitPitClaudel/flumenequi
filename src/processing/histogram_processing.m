%Generate Histograms from Data

clc
clear all
close all

data = importdata('../processed_results/tcp_skew_burst24.csv');

data = data.data;

bw_est_burst = data(:,2);

h1 = histogram(bw_est_burst,200,'FaceColor','b','EdgeColor','b');
[counts_burst,edges_burst] = histcounts(bw_est_burst,200);

fprintf('mean burst is\n')
mean(bw_est_burst)


data = importdata('../processed_results/tcp_skew_consist24.csv');

data = data.data;

bw_est_consist = data(:,2);

hold on;
grid on;

h2 = histogram(bw_est_consist,160,'FaceColor','r','EdgeColor','r');

[counts_consist,edges_consist] = histcounts(bw_est_consist,160);

fprintf('mean consist is\n')
mean(bw_est_consist)

legend('Burst Traffic BW Estimates - 24 Gbps',...
'Consistent Traffic BW Estimates - 24 Gbps')

xlabel('Bandwidth Estimate (Gbps')
ylabel('Histogram Counts')

write = zeros(201,4);

write(1:200,1) = counts_burst;
write(1:201,2) = edges_burst;
write(1:160,3) = counts_consist;
write(1:161,4) = edges_consist;

writematrix(write,'traffic_histogram_data.csv')
