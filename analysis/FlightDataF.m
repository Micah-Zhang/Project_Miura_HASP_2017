%Opening only the F column for flight 11
    %Multiplying all the numbers by 5
        %Rounding the numbers down to get the smaller values to go to zero
%Convert back by dividing by 5 and seperating into chunks

data = xlsread('D:\Matlab\HASP_2017_flight.xlsx','F:F');%C:\Users\CK\Documents\Miura\HASP_2017_flight.xlsx');%C:\Users\Documents\Miura\HASP_2017_flight.xsls');
disp("It Hopefully Worked");
data = 10.*data;
%ceiled = ceil(data());
floored = floor(data());
%rounded = round(data());
%rounded = rounded/5;
floored = floored / 10;
disp("Maybe Success");

