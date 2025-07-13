function [X,hs,m,S] = getdata_b(folder)

bl_folder = sprintf('%s/Communities_GN/BL_Mat.txt', folder);
bl_mat = readmatrix(bl_folder);
bl_names_folder = sprintf('%s/Communities_GN/BL_Mat_names.txt', folder);
bl_names_mat = readmatrix(bl_names_folder, "Delimiter"," ", "OutputType","string", 'Range',1);

bl = BT_branch;
bl.blname = bl_names_mat';
bl.hsi=bl_mat(1,:);
bl.eta=bl_mat(2,:);
bl.depth=bl_mat(3,:);
bl.szc=bl_mat(4,:);

hs = unique(bl.hsi);
X = zeros(1,numel(hs));
for i=1:numel(hs)
    X(i) = sum(bl.hsi(:) == hs(i));
end
[m,S] = polyfit((hs),log10(X),1);
end