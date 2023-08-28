clear

fname = "./CW_trimmed";
linestyles = ["-", "--", ":", "-.", "-x", "-o"];
vis = ["23km", "5km", "haze"];

for ii=1:size(vis, 2)
    styleno = 1;
    data = readtable(fname + ".csv", "VariableNamingRule","preserve");
    names = data.Properties.VariableNames;

    names = string(names);
    for i=2:size(names,2)
        names(i) = "_"+names(i);
    end
    
    
    filterstrings = [vis(ii)];
    legends = [""];
    leg_index = 1;
    figure
    
    
    for i=2:size(names,2)
    
        flag = true;
    
        for ind=1:size(filterstrings, 2)
            if ~contains(names(i), filterstrings(ind))
                flag = false;
            end
        end
    
        if flag
            n = extractAfter(string(names(i)), "_");

            line(i) = semilogy(data.(string(names(1))), data.(n),...
                linestyles(styleno),'LineWidth',2);

            legends(leg_index) = replace(string(names(i)), "_", " ");
            leg_index = leg_index + 1;
            styleno = styleno + 1;
            hold on
        end
    end
    
    grid minor
    set(gca, 'LineWidth', 1.5, 'FontSize', 16, 'FontWeight', 'bold', ...
        'Color', 'none', 'Xcolor', [0, 0, 0], 'YColor', [0, 0, 0], ...
        'TickLabelInterpreter', 'latex');
    titlestring = replace(fname + strjoin(filterstrings), "_", " ");
    title(titlestring)
    xlabel("Range [m]", 'Interpreter', 'latex')
    ylabel("Contrast SNR", 'Interpreter', 'latex')
    ylim([1, inf])
    legend(legends,'Interpreter', 'latex', 'location', 'northeast')
    set(gcf,'Position',[100 100 800 600])


    %saveas(gcf,replace(titlestring, " ", "_") +'.eps','epsc')
    %saveas(gcf,replace(titlestring, " ", "_") +'.png','png')
end