function [avg_eta,hs,m,S] = getdata_eta(folder)

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

avg_eta = findmean(bt.hsi,bt.eta);
hs = unique(bt.hsi);
[m,S] = polyfit((hs(2:end)),log10(avg_eta(2:end)),1);
end