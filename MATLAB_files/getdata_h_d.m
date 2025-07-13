function [avg_hs,d,m,S] = getdata_h_d(folder,init,final)

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

avg_hs = findmean(bt.depth,bt.hsi);
d = unique(bt.depth);
[m,S] = polyfit((d(init:final)),log10(avg_hs(init:final)),1);
end