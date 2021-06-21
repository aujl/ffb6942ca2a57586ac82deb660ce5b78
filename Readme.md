## Synopsis:
This repository prepares the information ratio of funds as features for a predictive model.
To this end

* the class [*DataExtractionAndPreprocessing*](DataExtractionAndPreprocessing.py) implements the download and preprocessing of funds data from Yahoo finance
* the class [*InformationRatio*](InformationRatio.py) implements the computation of information ratios with or without risk-adjusted returns and their addition to a dataframe
* the main routine [*FundsInformationRatioAnalysis.py*](FundsInformationRatioAnalysis.py) instantiates objects of the above classes and uses the details specified in the file [*Input.py*](Input.py) module to prepare a dataframe with information ratios for the possible use as features in a predictive model.
* some example plots are generated as .png images in the folder [*plots/*](plots)

<br/>

## Requirements
* development done using Anaconda/Python 3.8.2 (likely, any other virtual environment should work)
* a spec file [*conda_spec-file.txt*](conda_spec-file.txt) is included. Supposing that *conda* is used: to recreate the environment and run the main module, you can run the following commands:
  * *conda create --name QuantResearchAssessment --file conda_spec-file.txt*
  * *conda activate QuantResearchAssessment*
  * *python FundsInformationRatioAnalysis.py*


* Moreover, the file *requirements.txt* collects the dependencies (used versions in parenthesis, where applicable)
  * pandas (1.1.3)
  * pandas-datareader (0.9.0)
  * numpy  (1.19.2)
  * matplotlib (3.3.4)
  * datetime 
  * os 
* depending on your setup, you can try one of the following
  * *conda install --file requirements.txt*   (using conda)
  * *pip install -r requirements.txt*         (using pip inside of any other (virtual) environment)

<br/>

## Task breakdown:
Plot: We want to predict a fund’s future performance using information ratios that it
realized in the past. 

1. prepare the past information ratios (IRs) as features for a time-series prediction model. 
2. Desired functionality:
  * different parametrizations of IRs (see assumption 1)
  * calculate information ratios based on excess returns (see assumption 2)
  * as well as based on risk-adjusted excess returns (see assumption 3). 
3. Use openly available and free data on at least three funds and their respective benchmarks to illustrate the functionality. (see assumption 4)
4. How would you setup a prediction model using these features. 

<br/>

## Assumptions:
Here's a brief summary of the assumptions taken to deal with the ambiguity of the tasks (see references there).

1. as a parameter, we chose the window over which the expectation values and variances in the IR is evaluated
2. for simplicity, the excess return was computed with the Dow Jones Industrial average as benchmark. This is not the best benchmark for all considered examples, because they come from different sectors and geographical locations. 
3. for simplicity, we set as the risk-free return annual return is assumed to be 0.01 ; this should be adapted to the rate for long-term deposits with some treasury, for instance.
4. the data is queried from Yahoo finance via pandas-datareader; to get continuous and clean data, ETFs were selected. For funds reporting their value irregularly or at a larger step than a day, the implementation should add the missing data points by the call to the 'merge' method of pandas dataframes with a column that is populated with the dates at which the values of the fund are required. It might be required to apply some smoothing/interpolation instead to make the values better-digestible as features for machine learning models.

<br/>

## Comment on task 4.:

That's a multifaceted question, and depends if the 'using these features' is taken as, a), inclusive or, b), exclusive.

Generally, a predictive model for a time series represents an attempt at forecasting the future values of said time series. Here, for the sake of simplicity and nature of this assessment, consider the information ratio (IR) -- a predictive model could forecast (i.e. IR in t+365 days = 0.3798) or classify (i.e., IR larger or smaller than 0.5) the IR. The resulting investment strategy -- presupposing a reliable forecast or classification is feasible -- can then be used to make a recommendation which funds to choose with what weight. 

a) If we're allowed to consider additional data besides the IRs that use only the benchmark index and the funds values as ingredients, then I would opt for a deep neural network with a two-branch layout: one branch that is composed of a set of long-short-term-memory layers that process the IR features and a second branch of dense layers that processes out-of-series data like news sentiment or the tickers/features of the holdings of the funds (see [this example](./two_branch_model.png) for a sketch of the model we created doing the tutorial [here](https://medium.com/codex/stock-price-prediction-a-modified-approach-8d63ea6726a7 ).

b) If we're not allowed to consider additional out-of-series data, then I'd opt for a non-AI based statistical forecasting method like ARIMAs (auto-regressive integrated moving average) from the statsmodels python module or Facebook's 'Prophet' model [here](https://facebook.github.io/prophet/). This intuition is based on a recent comparison of statistical and machine-learning-based forecasting techniques with in-series data [(see here)](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0194889).


