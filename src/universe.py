#importing pandas
import pandas as pd

# Wikipedia URL with the list of S&P 500 companies
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def clean_tickers(ticker_list):
    return [str(t).strip().upper() for t in ticker_list if pd.notna(t)]




# Read all HTML tables on the page
tables = pd.read_html(url)

#tables[0] is Current snp500 list and tables[1] is list of chnages made to snp500 and when 


#Assigning tables[0] to a new variable current_list
current_list = tables[0]
current_list.columns = current_list.columns.get_level_values(0)

#Assigning tables[1] to a new variable changes_list
changes_list = tables[1]

# Flatten column headers (in case of multi-index)
changes_list.columns = changes_list.columns.get_level_values(0)

#Changing Date column format to YYY-MM-DD
changes_list["Date"] = pd.to_datetime(changes_list["Date"], errors="coerce")


#list of tickers to be included in the universe
#To get a list of tickers that were in snp500 list throughout the year of 2024: 
#Get list of current Tickers -> add tickers that were removed in 2025 -> remove all the tickers that were added or removed during the year 2024

#List of current Tickers
tickers_list= current_list["Symbol"]


#converting tickers list from pandas series to a python list
tickers_list= tickers_list.to_list()

#List of changes made in 2025
changes_2025 = changes_list[changes_list["Date"].dt.year==2025]

#List tickers removed in 2025 and converting it from Pandas series to Python list
removed_2025_tickers = changes_2025.iloc[:,3].to_list()


#appending tickers removed in 2025 to tickers_list
tickers_list = list(set(tickers_list + removed_2025_tickers))

#List of chnages made in 2024
changes_2024 = changes_list[changes_list["Date"].dt.year==2024]

#List of tickers added in 2024
added_2024 = changes_2024.iloc[:,1]


#converting added_2024 to a list
added_2024=added_2024.tolist()

#List of tickers removed in 2024
removed_2024 = changes_2024.iloc[:,3]


#converting added_2024 to a list
removed_2024= removed_2024.tolist()

#final list of tickers to be removed from tickers_list
to_remove= set(added_2024 + removed_2024)

#final list of tickers
tickers_list= [ticker for ticker in tickers_list if ticker not in to_remove ]

print(len(tickers_list))
print(tickers_list)

def get_tickers_list():
    return tickers_list
