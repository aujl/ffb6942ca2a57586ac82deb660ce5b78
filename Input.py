# List of symbols, for which daily OHLCV data is downloaded
SymbolList = ['0P00000UWV.F',   # pension
            'ESP0.DE',          # gaming
            'GADGX',            # conservative/Goldman Sachs dividends
            'MCSMX',            # asian smallcaps
            '^DJI' ]            # Dow Jones (benchmark)]

BenchmarkLabel = '^DJI'         # specify label of the benchmark
RiskFreeRate = 0.01             # return rate of risk free investment
StartDate = '2017-01-01'
Window = 92                    # number of days for which to evaluate the information ratios
