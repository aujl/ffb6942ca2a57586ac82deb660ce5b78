
import datetime as dt
import pandas as pd 
import os
import pandas_datareader.data as web 

class DataExtractionAndPreprocessing():
    """
    Synopsis: Class that implements download and preprocessing of data for the selected funds.
    ---------

    Properties:
    -----------
    self.AllData: pandas dataframe that contains all the funds data required 

    Methods:
    --------

    __init__: initialization method; downloads the required data and puts it into self.AllData
    fetch_data: method to fill self.AllData with ticker dataframe
    MergeDfs: helper function to merge a list of dataframes into a single one
    AddColumnPrefix: helper function to prefix column of a dataframe with a string
    """

    def __init__(self, 
                 StartDate = '2017-01-01',
                 SymbolList = ['GADGX','^DJI']):
        """
        Synopsis: Fetches ticker data and populate self.AllData with a dataframe
        ---------

        Parameters:
        -----------
        SymbolList: list of str, containing the Symbols of the historical data to fetch
        StartDate: str, the YYYY-DD-MM starting date of the data analysis 


        Returns:
        --------
        Nothing, but initializes data in self.AllData

        """
        self.AllData = self.fetch_data(tickers = SymbolList,
                                       StartDate = StartDate,
                                       EndDate = dt.datetime.today().strftime('%Y-%m-%d') )

        return

###########################################
###########################################

    def fetch_data(self, 
                   tickers = None, 
                   StartDate = dt.datetime(2017,5,11), 
                   EndDate = dt.datetime(2021,1,4)):
        """
        Synopsis: Fetches ticker data and returns it as a merged dataframe with OHLCV column labels prefixed by the symbol name.
        ---------
        
        Parameters:
        -----------
        tickers: list of str, the ticker symbols of the desired funds 
        StartDate: datetime variable, the starting date of the data analysis
        EndDate: datetime variable, the final date of the data analysis

        Returns:
        --------
        self.MergeDfs(ListOfTickerDfs): pandas dataframe containing all downloaded data in columns labeled <Symbol>_Open/_High/...
        <files>: saves one .csv file for every element in the tickers list om the 'fund_details/' directory.
        
        References:
        -----------
        https://medium.com/codex/stock-price-prediction-a-modified-approach-8d63ea6726a7

        Notes
        -----
        
        Examples
        --------
        self.AllData = self.fetch_data(tickers=SymbolList)


        """
        # workaround for current issues with pandas datareader
        import yfinance as yf
        yf.pdr_override()

        # if the output directory does not exist, create it
        if not os.path.exists('fund_details'):
            os.makedirs('fund_details')

        # initialize dataframe with all the dates required 
        DatesDf = pd.DataFrame()
        DatesDf['Date'] = pd.date_range(start=StartDate,end=EndDate)

        # initializes list with all dates considered
        ListOfTickerDfs = [] 
        ListOfTickerDfs.append(DatesDf)

        for ticker in tickers:

            print("fetching historical data for "+ ticker)
            
            try:
                # workaround for pandas interface to yahoo finance
                df = web.get_data_yahoo(ticker, data_source='yahoo', start=StartDate, end=EndDate)

                # pandas interface stopped working
                #df=web.DataReader(ticker, 'yahoo', StartDate, EndDate) # read the data from 'yahoo finance' 
                self.AddColumnPrefix(df,ticker) # add ticker label as prefix to data
                ListOfTickerDfs.append(df) # append to list of dfs
                df.to_csv('fund_details/{}.csv'.format(ticker)) # save downloaded data for later

            except: # if the above fails, throw an error message and continue.
                print("Error")
                continue

        # merge list to single dataframe for return
        return self.MergeDfs(ListOfTickerDfs)
  
###########################################
###########################################
      
    def MergeDfs(self,ListOfDfs,ColLabelLeft='Date',ColLabelRight='Date'):
        """
        Synopsis: Merge all dataframes in the list ListOfDfs using ColLabelLeft/Right as the reference columns for the merge
        ----
        Parameters:
        ----
        ListOfDfs: list of pandas dataframes to merge
        ColLabelLeft: str, column label of the dataframe to merge into
        ColLabelRight: str, column label of the dataframe to merge from

        ----
        Returns:
        ----

        MergedDf: pandas dataframe containing all columns of all dataframes in the list ListOfDfs
        """

        # for initialization of output dataframe, the first iteration is used
        FirstIteration=True

        # loop through dataframes in ListOfDfs
        for Ticker in ListOfDfs:

            if FirstIteration: # initialize output

                MergedDf = Ticker       # initialize the output dataframe with the first element of the list
                FirstIteration=False    # initialization is done

            else:
                # merge keeping all dates in all data frames (how = 'outer') and filling forward in time (fill_method = 'ffill')
                MergedDf = pd.merge_ordered(left=MergedDf, 
                                            right=Ticker, 
                                            left_on=ColLabelLeft, 
                                            right_on=ColLabelRight,
                                            fill_method='ffill', 
                                            how='outer')
        return MergedDf

###########################################
###########################################

    def AddColumnPrefix(self,Df,Prefix):

        """
        Synopsis: Add prefix 'Prefix_' to the all column labels of the dataframe Df that are not 'Date'
        ---------

        Parameters:
        -----------
        Df : pandas dataframe
        Prefix : string to add as prefix to column labels of Df

        Returns:
        --------

        Df : pandas dataframe with prefixed column labels
        """

        # set columns to a list with prefixed columns
        Df.columns=[Prefix+'_'+j for j in Df.columns if j != 'Date']

        return Df