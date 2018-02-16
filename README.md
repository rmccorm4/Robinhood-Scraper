# Robinhood-Scraper
This is a series of scripts I've created in order to better track
my finances. 

These scripts generate two CSV files
* orders.csv
	* Spreadsheet of all orders made on your Robinhood account
* stockwise\_pl.csv
	* Spreadsheet of the net Profit/Loss of each company/stock you've
	ever traded on your Robinhood account, sorted with your biggest
	gains at the top, and biggest losses at the bottom.

I am currently working on a simple GUI to make the experience a little
easier and aesthetically pleasing. I'm starting with Tkinter() for 
simplicity but plan to try out PyQt5 in the near future.

## How to Use
Until I get the GUI working, you will only need Python3 and the Robinhood
Private API which is already included in this repository, and can be setup
by executing the following in your terminal:
```
cd Robinhood
pip install .
```

Once the Robinhood API is setup correctly, you can generate the CSV files
by executing:
```
python3 finance_tracker.py
```

NOTE: Running `finance_tracker.py` will prompt you to enter your Robinhood
account login information in order to scrape the data. Your login information
will not be saved or recorded in any way.

The CSV files generated, `orders.csv` and `stockwise_pl.csv`, can be
opened with Microsoft Excel, and Google Sheets in order to see a nicely
formatted spreadsheet rather than a text file.
