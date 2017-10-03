clear all;
close all;
clc;

fileName = '/home/micah/miura/analysis/data1.raw';
data = textread(fileName,'%s','delimiter','\n');
ftell(data)