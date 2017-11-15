%clear all;
%close all;
%clc;

fileName = 'sens.log';  %D:\sens.log';
data = textread(fileName,'%s','delimiter',' ');%/n
temp = find(strcmp(data,'T9'));
camerawall3 = find(strcmp(data,'3:'));
%Everytime temp finds one give it a number n+1 for time
time = [1:5709];
plot(time,temp)
%format long
%disp(temp)

