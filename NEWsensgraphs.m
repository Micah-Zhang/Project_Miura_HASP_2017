%New sensor temperature graphs!!!! It works!!!

fileName = 'sens.log';  %set a file name
data = textread(fileName,'%s','delimiter',' '); %read file

%Plot for CameraWall 3
temp = find(strcmp(data,'T9')); %check for T9 in data, kind of useless now
m2 = find(strcmp(data,'3:')); %check for 3: in data
moto2 = m2 + 1; %finds the temperature
motor2 = data(moto2); %converts from a line number into the temp value
motortemp = str2double(motor2); %converts camerawall from a cell into double
time = [1:6225]; %sets up time variable
plot(time, motortemp) %plot the graph
title('Camera Wall 3 Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Plot for Ambient External
amb = find(strcmp(data,'8:')); %check for 3: in data
ambient = amb + 1; %finds the temperature
ambientx = data(ambient); %converts from a line number into the temp value
ambientexternal = str2double(ambientx); %converts camerawall from a cell into double
time = [1:6225]; %sets up time variable
plot(time, ambientexternal) %plot the graph
title('Ambient External Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Plots temperature for motor driver
m = find(strcmp(data,'9:')); %check for 3: in data
moto = m + 1; %finds the temperature
motor = data(moto); %converts from a line number into the temp value
motorDriver = str2double(motor); %converts camerawall from a cell into double
time = [1:6225]; %sets up time variable
plot(time, motorDriver) %plot the graph
title('Motor Driver Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Temperature Motor Plot
m2 = find(strcmp(data,'5:')); %check for 3: in data
moto2 = m2 + 1; %finds the temperature
motor2 = data(moto2); %converts from a line number into the temp value
motortemp = str2double(motor2); %converts camerawall from a cell into double
time = [1:5709]; %sets up time variable
plot(time, motortemp) %plot the graph
title('Motor Temperature');
xlabel('Time (s)');
ylabel('Temp (F)');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%Weird!
%Camera wall 2 plot
a = find(strcmp(data,'2:')); %check for 3: in data
amb2 = a + 1; %finds the temperature
ambient = data(amb2); %converts from a line number into the temp value
ambientinternal = str2double(ambient); %converts camerawall from a cell into double
time2 = [1:6225]; %sets up time variable
plot(time2, ambientinternal) %plot the graph
title('Camera Wall 2 Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Ambient internal plot
a = find(strcmp(data,'7:')); %check for 3: in data
amb2 = a + 1; %finds the temperature
ambient = data(amb2); %converts from a line number into the temp value
ambientinternal = str2double(ambient); %converts camerawall from a cell into double
time2 = [1:6225]; %sets up time variable
plot(time2, ambientinternal) %plot the graph
title('Ambient Internal Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Camera wall 1 plot
c4 = find(strcmp(data,'1:')); %check for 3: in data
cama4 = c4 + 1; %finds the temperature
camera4 = data(cama4); %converts from a line number into the temp value
camerawall4 = str2double(camera4); %converts camerawall from a cell into double
time2 = [1:6225]; %sets up time variable
plot(time2, camerawall4) %plot the graph
title('Camera Wall 1 Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Camera wall 4 plot
c4 = find(strcmp(data,'4:')); %check for 3: in data
cama4 = c4 + 1; %finds the temperature
camera4 = data(cama4); %converts from a line number into the temp value
camerawall4 = str2double(camera4); %converts camerawall from a cell into double
time2 = [1:6225]; %sets up time variable
plot(time2, camerawall4) %plot the graph
title('Camera Wall 4 Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

%Buck Converter plot
b1 = find(strcmp(data,'6:')); %check for 3: in data
buc1 = b1 + 1; %finds the temperature
buck1 = data(buc1); %converts from a line number into the temp value
buckconverter = str2double(buck1); %converts camerawall from a cell into double
time2 = [1:6225]; %sets up time variable
plot(time2, buckconverter) %plot the graph
title('Buck Converter Temp');
xlabel('Time (s)');
ylabel('Temp (F)');

