function [avg_eta,avg_hs,m,S] = getdata_eta_d(folder,init,final)

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

avg_eta = findmean(bt.depth,bt.eta);
avg_hs = findmean(bt.depth,bt.hsi);
d = unique(bt.depth);
[m,S] = polyfit((avg_hs(init:final)),log10(avg_eta(init:final)),1);
end