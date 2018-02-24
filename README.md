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
pip333 install .
```

Once the Robinhood API is setup correctly, you can generate the CSV files
by executing:
```
python3 robinhood_pl.py
```

NOTE: Running `robinhood_pl.py` will prompt you to enter your Robinhood
account login information in order to scrape the data. Your login information
will not be saved or recorded in any way.

## Spreadsheets

The CSV files generated, `orders.csv` and `stockwise_pl.csv`, can be
opened with Microsoft Excel, and Google Sheets in order to see a nicely
formatted spreadsheet rather than a text file.

### Additional

To see a Pie Chart of your profits/losses, run:

```
python3 demo.py
```

The code is currently messy and mostly copy and pasted from `robinhood_pl.py`
but I had to throw together a demo for an event and didn't want to go
messing anything up to much at the last minute.

`gui.py` is currently in progress for having a user interface rather than
using the command line.
