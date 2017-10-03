clear all;
close all;
clc;

% Open and parse downlink log
fileName = '/home/micah/miura/analysis/downlink.log';
data = textread(fileName,'%s','delimiter',' ');
index = find(strcmp(data,'BU'));
format long;

% Creates a table displaying all bootup times during flight
bootups = zeros(14,1);
counter = 1;
for i = 1:5:size(index,1)
    time = cell2mat(data(index(i)+1));
    time = time(5:end);
    bootups(counter,1) = str2double(time);
    counter = counter + 1;
end

% Plot and display all bootup times
plot(1:14,bootups)
disp(bootups)