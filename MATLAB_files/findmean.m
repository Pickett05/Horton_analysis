function [yy] = findmean(tbf, tbc)
% tbf = to be fixed
% tbc = variable whose mean is to be calculated over tbf
A=tbf(1:end); %what you want to fix say hsi, or depth
% B=depth+1;
B=tbc(1:end);
[anew,aidx]=sort(A);
bnew=B(aidx);
auniq = unique(anew);
k=1;
for count=1:numel(auniq)
    for i=1:length(anew)
        if anew(i)==auniq(count)
            bb(count,k)=bnew(i);
            k=k+1;
        end        
    end
    comm_count(count) = k-1;
    k=1;
end
for count=1:numel(auniq)
    vec=bb(count,1:comm_count(count));
    yy(count)=mean(vec);
    zz(count)=var(vec);
end
xx=1:1:max(anew);
end