StockHistory

These tools collect stock and search results data over time.

companies.txt
	contains the companies tracked as well as the data to be collected
	its header contains the columns from which the csv for each company will be made.
	time and price will fill the time and the price.
	search will fill the google results for that the particular company.
	search+[query] will fill up google search results of the company and a query.
		search+buy   ==> will fill in the search results for 'GOOGL buy'
	Following lines bellow the header should be filled with the stock companes to be look at.
	
If changes are done to the companies.txt then use the install.py which will format the data folder.
