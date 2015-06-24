%% Script to visualise output from RADDOSE-3D DoseState.csv file
close all
clear all
clc

%% User defined inputs
name_of_input_csv_file = 'output-DoseState.csv'; %Name of the .csv file to be input into script 

isovalues = [63,64,65,66,67]; %Values for the isosurfaces

%% Read in the csv data 
data = xlsread(name_of_input_csv_file);

x = data(:,1); %get the x coordinates
y = data(:,2); %get the y coordinates
z = data(:,3); %get the z coordinates

%% Get the unique values for each coordinate
x_unique = unique(x); % Get unique x coordinate values 
y_unique = unique(y); % Get unique y coordinate values 
z_unique = unique(z); % Get unique z coordinate values 

%% Create a meshgrid with the coordinates required for 3D visualisation
[X,Y,Z] = meshgrid(x_unique,y_unique,z_unique);

%% Reshape the dose values into a 3D matrix corresponding to the coordinates of the meshgrid
dose = reshape(data(:,4),size(X));

%% Plot crystal
num = numel(isovalues);

%# plot isosurfaces at each level, using direct color mapping
figure('Renderer','opengl')
p = zeros(num,1);
for i=1:num
    p(i) = patch( isosurface(X,Y,Z,dose,isovalues(i)) );
    isonormals(X,Y,Z,dose,p(i))
    set(p(i), 'CData',i);
end
set(p, 'CDataMapping','direct', 'FaceColor','flat', 'EdgeColor','none')

%# define the colormap
clr = hsv(num);
colormap(clr)

%# legend of the isolevels
%#legend(p, num2str(isovalues(:)), ...
%#  'Location','North', 'Orientation','horizontal')

%# fix the colorbar to show iso-levels and their corresponding color
caxis([0 num])
colorbar('YTick',(1:num)-0.5, 'YTickLabel',num2str(isovalues(:)))

%# tweak the plot and view
box on; grid on; axis tight; daspect([1 1 1])
view(3); camproj perspective
camlight; lighting phong; alpha(0.75);
rotate3d on