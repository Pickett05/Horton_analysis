function [X,hs,m,S] = getdata_X(folder)

bt_folder = sprintf('%s/Communities_GN/BT_Mat.txt', folder);
bt_mat = readmatrix(bt_folder);
bt_names_folder = sprintf('%s/Communities_GN/BT_Mat_names.txt', folder);
bt_names_mat = readmatrix(bt_names_folder, "Delimiter"," ", "OutputType","string", 'Range',1);

bt = BT_community;
bt.btname = bt_names_mat';
bt.hsi=bt_mat(1,:);
bt.eta=bt_mat(2,:);
bt.depth=bt_mat(3,:);
bt.szc=bt_mat(4,:);

hs = unique(bt.hsi);
X = zeros(1,numel(hs));
for i=1:numel(hs)
    X(i) = sum(bt.hsi(:) == hs(i));
end
[m, S] = polyfit((hs),log10(X),1);
end