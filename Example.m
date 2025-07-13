%%
close all
clear all

%%

folder = {"sample_1"}; % path to the folder containing the network whose community structure is being analysed. We wish to obtain the Horton's laws for this network's community structure.
col = {'#ff997d'}; % color of the data points
dispname = {'sample_1'}; % display name of the data points in the legend
mar = {'o'}; % marker of the data points
msize = 6; % marker size of the data points

figure('DefaultAxesPosition', [0.06, 0.06, 0.9, 0.9])

% b vs h

X_p = cell(1,4); % b, hs, m, b_lin_fit
[b, hs, m, S] = getdata_b(string(folder(1)));
X_p{1,1} = log10(b); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(b) with linear fit
subplot(241)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2},X_p{1,1},Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_b = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2},X_p{1,4},LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$h$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(b_h)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% X vs h

X_p = cell(1,4); % X, hs, m, b_lin_fit
[X, hs, m, S] = getdata_X(string(folder(1)));
X_p{1,1} = log10(X); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(X) with linear fit
subplot(242)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2},X_p{1,1},Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{\chi} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2},X_p{1,4},LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$h$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\chi_h)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% eta vs h

X_p = cell(1,4); % eta, hs, m, b_lin_fit
[X, hs, m, S] = getdata_eta(string(folder(1)));
X_p{1,1} = log10(X); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(X) with linear fit
subplot(243)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2}(2:end),X_p{1,1}(2:end),Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{\eta} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2}(2:end),X_p{1,4}(2:end),LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$h$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\langle \eta \rangle_h)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% n vs h

X_p = cell(1,4); % n, hs, m, b_lin_fit
[X, hs, m, S] = getdata_n(string(folder(1)));
X_p{1,1} = log10(X); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(X) with linear fit
subplot(244)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2},X_p{1,1},Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{n} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2},X_p{1,4},LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$h$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\langle n \rangle_h)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% cutoffs for depth plots
init = 1; %these are indices
final = 5;

% h vs d at d

X_p = cell(1,4); % hs, d, m, b_lin_fit
[hs, d, m, S] = getdata_h_d(string(folder(1)),init,final);
X_p{1,1} = log10(hs); % in log10 scale
X_p{1,2} = d;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(b) with linear fit
subplot(245)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2}(init:final),X_p{1,1}(init:final),Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{h} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2}(init:final),X_p{1,4}(init:final),LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$d$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\langle h \rangle_d)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% X vs h at d

X_p = cell(1,4); % X, hs, m, b_lin_fit
[X, hs, m, S] = getdata_X_d(string(folder(1)),init,final);
X_p{1,1} = log10(X); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(X) with linear fit
subplot(246)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2}(init:final),X_p{1,1}(init:final),Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{\chi} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2}(init:final),X_p{1,4}(init:final),LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$\langle h \rangle_d$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\chi_d)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% eta vs h at d

X_p = cell(1,4); % eta, hs, m, b_lin_fit
[X, hs, m, S] = getdata_eta_d(string(folder(1)),init,final);
X_p{1,1} = log10(X); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(X) with linear fit
subplot(247)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2}(init:final),X_p{1,1}(init:final),Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{\eta} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2}(init:final),X_p{1,4}(init:final),LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$\langle h \rangle_d$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\langle \eta \rangle_d)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)

% n vs h at d

X_p = cell(1,4); % n, hs, m, b_lin_fit
[X, hs, m, S] = getdata_n_d(string(folder(1)),init,final);
X_p{1,1} = log10(X); % in log10 scale
X_p{1,2} = hs;
X_p{1,3} = m;
X_p{1,4} = (X_p{1,3}(1)*X_p{1,2}+X_p{1,3}(2)); % log10(X) with linear fit
subplot(248)
hold on
new_dispname = "$" + dispname{1} + "$";
plot(X_p{1,2}(init:final),X_p{1,1}(init:final),Marker=mar{1},LineStyle='none',Color=col{1},LineWidth=1, MarkerSize=8, MarkerFaceColor=col{1},DisplayName=new_dispname);
new_dispname = "$\gamma_{n} = " + round(X_p{1,3}(1),2) +"(" + round(S.rsquared,2) +")$";
plot(X_p{1,2}(init:final),X_p{1,4}(init:final),LineStyle='-',Color='#494a49',LineWidth=1.5,DisplayName=new_dispname);
set(gca,'linewidth',1,'fontsize',20,'TickLabelInterpreter','latex')
xlabel('$\langle h \rangle_d$', 'Interpreter','latex', 'FontSize', 22)
ylabel('$\log_{10}(\langle n \rangle_d)$', 'Interpreter','latex', 'FontSize', 22)
box on
axis square
f=get(gca,'Children');
legend([f(1)],'Interpreter','latex','Box','off','FontSize',16)