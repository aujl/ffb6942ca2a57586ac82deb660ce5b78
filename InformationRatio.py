import numpy as np
import pandas as pd

class InformationRatio():
    """ 
    Synopsis: Class to compute the information ratio (IR) with a benchmark.
    ---------

    Properties:
    -----------
    self.AllData: pandas dataframe that contains all the IRs added

    Methods:
    --------
    __init__: initialize self.AllData with dataframe that contains the bare and risk-adjusted IR added
    CalculateInformationRatio: method to compute information ratios and add them to a dataframe
    SharpeRatio: function to compute the Sharpe ratio (risk-adjusted returns) and add them to a dataframe
    Returns: method to compute the returns or log-returns and add them to a dataframe

    """

###########################################
###########################################

    def __init__(self, 
                 SymbolList =  ['GADGX','^DJI'], 
                 BenchmarkLabel = '^DJI', 
                 Window = 50,
                 RiskFreeRate = 0.01,
                 AllData = None):
        """ 
        Synopsis: Initialize self.AllData dataframe by adding IR data to the input dataframe AllData.
        ---------

        Parameters:
        -----------

        AllData: pandas dataframe expected to contain OHLCV data of the assets/funds
        SymbolList: list of str, ticker symbols in dataframe AllData
        BenchmarkLabel: str, ticker symbol (per Yahoo finance standard) for use as the benchmark 
        Window: int, number of time steps to use to evaluate the information ratio
        RiskFreeRate: float, return rate of risk-free investment used to compute Sharpe ratio

        Returns:
        --------

        self.AllData: pandas dataframe, containing additional columns with the bare and risk-adjusted IRs labeled <InvestmentLabel>_<BenchmarkLabel>_<IR_label>_<Window>.
        """

        self.AllData = AllData
        # loop to add bare information ratios
        for ThisTicker in SymbolList:        
            self.AllData = self.CalculateInformationRatio(TickerDf = self.AllData, 
                                                          InvestmentLabel = ThisTicker, 
                                                          BenchmarkLabel = BenchmarkLabel, 
                                                          Window = Window,
                                                          RiskAdjusted = False,
                                                          RiskFreeRate = RiskFreeRate)
  
        # loop to add risk-adjusted information ratios
        for ThisTicker in SymbolList:        
            self.AllData=self.CalculateInformationRatio(TickerDf = self.AllData, 
                                                        InvestmentLabel = ThisTicker, 
                                                        BenchmarkLabel = BenchmarkLabel, 
                                                        Window = Window,
                                                        RiskAdjusted = True,
                                                        RiskFreeRate = RiskFreeRate)

        

        return

###########################################
###########################################

    def CalculateInformationRatio(self,
                                  TickerDf = None, 
                                  InvestmentLabel = None, 
                                  BenchmarkLabel = '^DJI', 
                                  Window = 50,
                                  RiskAdjusted = False,
                                  RiskFreeRate = 0.01):
        """ 
        Synopsis: Compute the information ratio (IR) using a window of values and a benchmark.
        ---------

        Parameters:
        -----------

        TickerDf: pandas dataframe expected to contain OHLCV data of the asset/fund
        InvestmentLabel: str, ticker symbol (per Yahoo finance standard) for use as the benchmark 
        BenchmarkLabel: str, ticker symbol (per Yahoo finance standard) for use as the benchmark 
        Window: int, number of time steps to use to evaluate the information ratio
        risk_adjusted: boolean, toggle to switch between risk-adjusted (IR_label=='IRA') and bare (IR_label=='IR') excess returns for the computation of the IR

        Returns:
        --------

        TickerDf: pandas dataframe, containing an additional column labeled <InvestmentLabel>_<BenchmarkLabel>_<IR_label>_<Window>.
        """

        # catch for comparing identical tickers
        if InvestmentLabel == BenchmarkLabel:
            print('Information ratios only make sense if the tickers are different.')
            return TickerDf

        # add returns to dataframe labeled <InvestmentLabel>_R_<Window>
        InvestmentBareReturnLabel = self.Returns(TickerDf = TickerDf, 
                                                 ColumnLabel = InvestmentLabel, 
                                                 Log = False,
                                                 Window = Window)

        # add returns to dataframe labeled <BenchmarkLabel>_R_<Window>
        BenchmarkBareReturnLabel = self.Returns(TickerDf = TickerDf, 
                                                ColumnLabel = BenchmarkLabel, 
                                                Log = False,
                                                Window = Window)


        # assemble label of and output column 
        if not RiskAdjusted:
            IRLabel=InvestmentLabel + "_" + BenchmarkLabel + "_IR_" + str(Window)
            InvestmentReturnLabel = InvestmentBareReturnLabel
            BenchmarkReturnLabel = BenchmarkBareReturnLabel
        else:
            IRLabel=InvestmentLabel + "_" + BenchmarkLabel + "_IRA_" + str(Window)
            InvestmentReturnLabel = self.SharpeRatio(TickerDf = TickerDf, 
                                                     ReturnsLabel = InvestmentBareReturnLabel, 
                                                     RiskFreeRate = RiskFreeRate, 
                                                     Window = Window)
            BenchmarkReturnLabel = self.SharpeRatio(TickerDf = TickerDf, 
                                                    ReturnsLabel = BenchmarkBareReturnLabel, 
                                                    RiskFreeRate = RiskFreeRate, 
                                                    Window = Window)


        
        # get difference/absolute returns, i.e., outperformance vs benchmark
        Alphas = TickerDf[InvestmentReturnLabel] - TickerDf[BenchmarkReturnLabel]

        # get omegas root variance / std. dev. of outperformance
        Omegas=Alphas.rolling(window=Window,min_periods = 0).std()

        # get expectation of returns --> Alphas
        Alphas=Alphas.rolling(window = Window, min_periods = 0).mean()

        # add information ratio to dataframe 
        TickerDf[IRLabel] = Alphas/Omegas

        # fill undefined values (here, it's important to use method 'ffill', because otherwise, future information could become available in the training of the predictive model)
        TickerDf.fillna(inplace=True,method='ffill')

        return TickerDf

###########################################
###########################################

    def SharpeRatio(self, 
                    TickerDf = None, 
                    ReturnsLabel = None, 
                    RiskFreeRate = 0.01, 
                    Window = 50):
        """
        Compute/add Sharpe ratio to a pandas dataframe

        Parameters
        ----
        TickerDf: pandas dataframe that contains a label given by ReturnsLabel
        ReturnsLabel: str, column label of column with returns
        RiskFreeRate: float, assumed risk-free return
        Window: int, number of steps to consider in the computation of the Sharpe ratio


        Returns:
        ----
        TickerDf: pandas dataframe with an added column suffixed '_SR_<window>' that contains the Sharpe ratio for window steps
        SR_Label: str, containing the label of the column with the Sharpe ratio

        """        

        # compute risk-free rate over sought window
        RiskFreeRateWindow = RiskFreeRate * ( 365 / Window )

        # assemble label of column
        SR_Label = ReturnsLabel.replace('_R_','_SR_')

        # assign Sharpe ratio to column
        TickerDf[SR_Label] = TickerDf[ReturnsLabel].rolling(Window).apply(lambda x: (x.mean() - RiskFreeRateWindow) / x.std(), raw = True)

        return SR_Label

###########################################
###########################################

    def Returns(self, 
                TickerDf = None, 
                ColumnLabel = None, 
                Log = False, 
                Window = 50):
        """
        Computes/adds the (log-)returns (pandas .diff(1).log()) to a pandas dataframe

        Parameters
        ----
        TickerDf: pandas dataframe that contains a label suffixed '_Close'
        ColumnLabel: str, used for the computation of the (log-)returns
        Log: boolean, toggle for computing the returns or the log-returns
        window: int, number of steps to consider for computing returns

        Returns:
        ----
        TickerDf: pandas dataframe with added (log-)returns with column label <ColumnLabel>_R or <ColumnLabel>_LR
        RLabel: str, label of the column added with (log-)returns

        """

        # catch bogus call to routine
        if (TickerDf is None) or (ColumnLabel is None) or (ColumnLabel + '_Close' not in TickerDf.columns):
            print('erroneous call of (Log-)Returns')
            return

        # attach '_Close' to ColumnLabel
        ColumnLabel += '_Close'

        # assign label for returns
        if Log:
            RLabel = ColumnLabel + '_LR_' + str(Window)
        else:
            RLabel = ColumnLabel + '_R_' + str(Window)

        # catch if these returns were already added to the dataframe
        if RLabel in TickerDf.columns:
            print('The returns required are already in the dataframe')
            return RLabel

        # assign (log-)returns to column
        if Log:
            TickerDf[RLabel] = np.log( (TickerDf[ColumnLabel] - TickerDf[ColumnLabel].shift(Window))/TickerDf[ColumnLabel] )
        else:
            TickerDf[RLabel] = (TickerDf[ColumnLabel] - TickerDf[ColumnLabel].shift(Window))/TickerDf[ColumnLabel] 

        # first window value will be nan, so we have to fill it
        TickerDf[RLabel].fillna(0.0, inplace = True)

        return RLabel