clear all;
close all;
clc;

fileName = '/home/micah/miura/analysis/downlink.log';
data = textread(fileName,'%c','delimiter','\n');