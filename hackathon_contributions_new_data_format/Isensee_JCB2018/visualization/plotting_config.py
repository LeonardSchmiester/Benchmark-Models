
def plotting_config(visualization_specification, ax, axx, axy, conditions, ms, ind_plot, i):
    '''
       plotting routine / preparations

       Parameters:
       ----------

       visualization_specification: pandas data frame contains defined data format (visualization file)
       ax:
       axx:
       axy:
       conditions: Values on x-axis
       ms:
       ind_plot:
       i: current index (row number) of row which should be plotted in visualizationSpecification file

       Return:
       ----------
       ax: matplotlib.Axes
       '''

    # not time,condition
    if visualization_specification.plotTypeSimulation[i] == 'LinePlot':

        # set xScale
        if visualization_specification.xScale[i] == 'lin':
            ax[axx, axy].set_xscale("linear")
        elif visualization_specification.xScale[i] == 'log10':
            ax[axx, axy].set_xscale("log")
        elif visualization_specification.xScale[i] == 'order':        # equidistant
            ax[axx, axy].set_xscale("linear")
            # check if conditions are monotone decreasing or increasing
            if np.all(np.diff(conditions) < 0):             # monotone decreasing
                xlabel = conditions[::-1]                   # reversing
                conditions = range(len(conditions))[::-1]   # reversing
                ax[axx, axy].set_xticks(range(len(conditions)), xlabel)
            elif np.all(np.diff(conditions) > 0):
                print('monotone increasing')
                xlabel = conditions
                conditions = range(len(conditions))
                ax[axx, axy].set_xticks(range(len(conditions)), xlabel)
            else:
                print('Error: x-conditions do not coincide, some are mon. increasing,'\
                      ' some monotonically decreasing')

        conditions = conditions + visualization_specification.xOffset[i]

        if visualization_specification.plotTypeData[i] == 'MeanAndSD':
            ax[axx, axy].errorbar(conditions, ms['mean'], ms['sd'], linestyle='-', marker='.',
                                  label=visualization_specification[ind_plot].legendEntry[i])
        elif visualization_specification.plotTypeData[i] == 'MeanAndSEM':
            ax[axx, axy].errorbar(conditions, ms['mean'], ms['sem'], linestyle='-', marker='.',
                                  label=visualization_specification[ind_plot].legendEntry[i])
        elif visualization_specification.plotTypeData[i] == 'replicate':  # plotting all measurement data
            for ii in range(0, len(ms['repl'])):
                for k in range(0, len(ms.repl[ii])):
                    ax[axx, axy].plot(conditions[conditions.index.values[ii]],
                                      ms.repl[ii][ms.repl[ii].index.values[k]], 'x')
        ax[axx, axy].legend()
        ax[axx, axy].set_title(visualization_specification.plotName[i])

        # # time
        # uni_times = uni_times + visualization_specification.xOffset[i]
        #
        # ax[axx, axy].errorbar(uni_times, ms['mean'], ms['sd'], linestyle='-', marker='.',
        #                       label=visualization_specification[ind_plot].legendEntry[i]
        #                       )
        # ax[axx, axy].legend()
        # ax[axx, axy].set_title(visualization_specification.plotName[i])

    elif visualization_specification.plotTypeSimulation[i] == 'BarPlot':

        x_pos = range(len(visualization_specification[ind_plot]))  # how many x-values (how many bars)
        x_name = visualization_specification[ind_plot].legendEntry[i]

        ax[axx, axy].bar(x_name, ms['mean'], yerr=ms['sd'])
        ax[axx, axy].set_title(visualization_specification.plotName[i])

    return ax
