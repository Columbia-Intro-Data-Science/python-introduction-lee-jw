%% Read info.txt file, which was extracted from https://api.trackico.io/v1/icos/, and process data to put in a dataframe
% Read file
text = fileread('info.txt');
idx_titles = strfind(text,'title":"');
projects = string([]);

% Separate one big string into projects
for i = 1:length(idx_titles)-1
    projects = [projects text(idx_titles(i)-1:idx_titles(i+1)-5)];
end

title = string(['title']);
slug = string(['slug']);
url = string(['url']);
ico_type = string(['ico_type']);
category = string(['category']);
rating = string(['rating']);
pre_ico_start = string(['pre_ico_start']);
pre_ico_end = string(['pre_ico_end']);
ico_start = string(['ico_start']);
ico_end = string(['ico_end']);

% Extract features
for i = 1:length(projects)
    project = projects{i};
    title = [title project(strfind(project,'"title":"')+length('title')+length('":"')+1:strfind(project,',"slug"')-2)];
    slug = [slug project(strfind(project,'"slug"')+length('slug')+length('":"')+1:strfind(project,',"url"')-2)];
    url = [url project(strfind(project,'"url"')+length('url')+length('":"')+1:strfind(project,',"ico_type"')-2)];
    ico_type = [ico_type project(strfind(project,'"ico_type"')+length('ico_type')+length('":"')+1:strfind(project,',"premium"')-2)];
    category = [category project(strfind(project,'"category"')+length('category')+length('":"')+1:strfind(project,',"short_description"')-2)];
    rating = [rating project(strfind(project,'"rating"')+length('rating')+length('":"')+1:strfind(project,',"image"')-2)];
    pre_ico_start = [pre_ico_start project(strfind(project,'"pre_ico_start"')+length('pre_ico_start')+length('":"')+1:strfind(project,',"pre_ico_end"')-2)];
    pre_ico_end = [pre_ico_end project(strfind(project,'"pre_ico_end"')+length('pre_ico_end')+length('":"')+1:strfind(project,',"ico_start"')-2)];
    ico_start = [ico_start project(strfind(project,'"ico_start"')+length('ico_start')+length('":"')+1:strfind(project,',"ico_end"')-2)];
    ico_end = [ico_end project(strfind(project,'"ico_end"')+length('ico_end')+length('":"')+1:strfind(project,',"updated_at"')-2)];
end

% Process data - inconsistencies in raw data resulted in "null" to show as "ul"
for j = 1:length(pre_ico_start)
    if pre_ico_start(j) == 'ul'
        pre_ico_start(j) = 'null';
    end
    if pre_ico_end(j) == 'ul'
        pre_ico_end(j) = 'null';
    end
    if ico_start(j) == 'ul'
        ico_start(j) = 'null';
    end
    if ico_end(j) == 'ul'
        ico_end(j) = 'null';
    end
end

% Combine all data into matrix and export as csv file
data = [title', slug', url', ico_type', category', rating', pre_ico_start', pre_ico_end', ico_start', ico_end'];

data_trading = data;
for i = 1:length(projects)
    if ico_type(i) == 'Trading'
        data_trading = [data_trading; data(i,:)];
    end
end
        
fid = fopen('data.csv', 'w');
for k = 1:length(data)
	fprintf(fid,'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',data{k,:});
end
fclose(fid)

fid2 = fopen('data_trading.csv', 'w');
for l = 1:length(data_trading)
	fprintf(fid,'%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n',data_trading{l,:});
end
fclose(fid2)
