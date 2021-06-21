"""
Main routine:
-------------
* instantiate classes DataExtractionAndPreProcessing and InformationRatio to download data and calculate information ratios
* create a few plots stored in the folder ./plots/
"""




from Input import BenchmarkLabel
import matplotlib.pyplot as plt
import os

if __name__ == "__main__":
    # get input
    import Input as inp
    # get functions to add information ratios to dataframe
    from InformationRatio import InformationRatio as IR
    # get data extraction class
    from DataExtractionAndPreprocessing import DataExtractionAndPreprocessing as DataEx

    # download data and store it in the folder './fund_details/<Symbol>.csv'
    DataExInstance=DataEx(SymbolList = inp.SymbolList,
                          StartDate = inp.StartDate) # default for EndDate is today.

    # instantiate information ratio class
    IRInstance=IR(SymbolList = inp.SymbolList,
                  BenchmarkLabel = inp.BenchmarkLabel,
                  Window = inp.Window,
                  RiskFreeRate = inp.RiskFreeRate,
                  AllData=DataExInstance.AllData)
    
    # now, the information ratios are available in IRInstance.AllData 
    # for efficiency reasons, it's likely better to get the IRs as numpy arrays with pandas builtin .to_numpy() method (depends largely on what's the type of predictive modeling)

    # if the output directory does not exist, create it
    if not os.path.exists('plots'):
        os.makedirs('plots')


    for j in inp.SymbolList:
        if j != inp.BenchmarkLabel:

            #### IR based on Bare returns 
            #### IR based on Bare returns 

            # assemble column label (should make that a function...)
            ColumnLabel = j + "_" + inp.BenchmarkLabel + "_" + "IR" + "_" + str(inp.Window)
            # use pandas dataframe plot method
            ax = IRInstance.AllData[ColumnLabel].plot.hist(bins=12, alpha=0.5)
            # set title
            ax.set_title("Information ratio for " + j + " vs " + inp.BenchmarkLabel)
            # set axes label
            ax.set_xlabel("IR, bare returns")
            # save figure to png
            plt.savefig('plots/IR_bare_'+ j + "_vs_" + inp.BenchmarkLabel + "_hist.png")
            # clear/close figure
            plt.clf
            plt.close()

            # use pandas dataframe plot method
            ax = IRInstance.AllData[[ColumnLabel,'Date']].plot(x='Date',y=ColumnLabel)
            # set title
            ax.set_title("Information ratio for " + j + " vs " + inp.BenchmarkLabel)
            # set title
            ax.set_ylabel("IR, bare returns")
            ax.set_xlabel("Date")
            # save figure to png
            plt.savefig('plots/IR_bare_'+ j + "_vs_" + inp.BenchmarkLabel + ".png")
            # clear/close figure
            plt.clf
            plt.close()

            #### IR based on risk-adjusted returns 
            #### IR based on risk-adjusted returns 

            # assemble column label (should make that a function...)
            ColumnLabel = j + "_" + inp.BenchmarkLabel + "_" + "IRA" + "_" + str(inp.Window)
            # use pandas dataframe plot method
            ax = IRInstance.AllData[ColumnLabel].plot.hist(bins=12, alpha=0.5)
            # set title
            ax.set_title("Information ratio for " + j + " vs " + inp.BenchmarkLabel)
            # set axes label
            ax.set_xlabel("IR, adjusted returns")
            # save figure to png
            plt.savefig('plots/IR_adjusted_'+ j + "_vs_" + inp.BenchmarkLabel + "_hist.png")
            # clear/close figure
            plt.clf
            plt.close()

            # use pandas dataframe plot method
            ax = IRInstance.AllData[[ColumnLabel,'Date']].plot(x='Date',y=ColumnLabel)
            # set title
            ax.set_title("Information ratio for " + j + " vs " + inp.BenchmarkLabel)
            # set title
            ax.set_ylabel("IR, adjusted returns")
            ax.set_xlabel("Date")
            # save figure to png
            plt.savefig('plots/IR_adjusted_'+ j + "_vs_" + inp.BenchmarkLabel + ".png")
            # clear/close figure
            plt.clf
            plt.close()