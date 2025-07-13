function [avg_N,hs,m,S] = getdata_n(folder)

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

avg_N = findmean(bt.hsi,bt.szc);
hs = unique(bt.hsi);
[m,S] = polyfit((hs),log10(avg_N),1);
end