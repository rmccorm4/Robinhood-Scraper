import csv
import json
import requests
import operator
import trade_history_downloader

class Order:
	def __init__(self, side, symbol, shares, price, date, state):
		self.side = side
		self.symbol = symbol
		self.shares = float(shares)
		self.price = float(price)
		self.date = date
		self.state = state
	
	def pl(self):
		if self.side == 'buy':
			return -1 * int(self.shares) * float(self.price)
		else:
			return int(self.shares) * float(self.price)

class Stock:
	def __init__(self, symbol):
		self.symbol = symbol
		self.orders = []
		self.net_shares = 0
		self.net_pl = 0

def generate_csv(username=None, password=None):
	trade_history_downloader.orders_to_csv(username, password)

def itemize_stocks():
	# Create list for each stock
	stocks = {}
	with open('orders.csv', 'r') as csvfile:
		lines = csv.reader(csvfile, delimiter=',')
		for line in lines:
			ticker = line[1]
			price = line[3]
			# Check for header or invalid entries
			if ticker == 'symbol' or price == '':
				continue

			# Add stock to dict if not already in there
			if ticker not in stocks:
				stocks[ticker] = Stock(ticker)
		
			# Add order to stock
			stocks[ticker].orders.append(Order(line[0], line[1], line[2], 
			line[3], line[4], line[5]))
	return stocks

def calculate_itemized_pl(stocks):
	for stock in stocks.values():
		for order in stock.orders:
			if order.side == 'buy':
				stock.net_shares += order.shares
			else:
				stock.net_shares -= order.shares
			# order.pl() is positive for selling and negative for buying
			stock.net_pl += order.pl()

		# Handle outstanding shares - should be current positions
		if stock.net_shares > 0:
			# SNAP needs to specifically be from NYSE
			
			#if stock.symbol == 'SNAP':
				#stock.symbol = 'NYSE:SNAP'

			rsp = requests.get('https://finance.google.com/finance?q=' + 
			stock.symbol + '&output=json')
			
			if rsp.status_code in (200,):
				# Deal with dumb google finance formatting - json() doesn't work
				try:
					fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
		
				except:
					rsp = requests.get('https://finance.google.com/finance?q=' +
					'NYSE:' + stock.symbol + '&output=json')
					fin_data = json.loads(rsp.content[6:-2].decode('unicode_escape'))
								
				# Doesn't include pre/post-market
				last_price = float(fin_data['l'].replace(',', ''))
				# Add currently held shares from net_pl as if selling now
				stock.net_pl += stock.net_shares * last_price
			else:
				print('BAD REQUEST: https://finance.google.com/finance?q=' + 
						stock.symbol + '&output=json')
				print('Perhaps try prepending exchange name to stock symbol')
				print('Example: If SNAP fails, try NYSE:SNAP')
		# Should handle free gift stocks
		elif stock.net_shares < 0:
			stock.symbol += ' (Free Gift)'

def piechart(sorted_pl, total_profits, total_losses):
	# CREATE PIE CHART
	import matplotlib.pyplot as plt
	
	chart_type = input('Enter "profits" or "losses": ')
	chart_depth = input('Enter "clean" or "all": ')

	if chart_type == 'profits':	
		if chart_depth == 'clean':
			threshold = float(input('Enter the minimum percent gains to include: '))
			profit_labels = [stock.symbol for stock in sorted_pl if (stock.net_pl*100/total_profits) >= threshold]
			profit_sizes = [(stock.net_pl/total_profits) for stock in sorted_pl if (stock.net_pl*100/total_profits) >= threshold]
			title = 'Itemized Profits > ' + str(threshold) + '%'
		else:
			profit_labels = [stock.symbol for stock in sorted_pl if stock.net_pl > 0]
			profit_sizes = [(stock.net_pl/total_profits) for stock in sorted_pl if stock.net_pl > 0]
			title = 'All Itemized Profits'
	else:
		if chart_depth == 'clean':
			threshold = float(input('Enter the minimum percent losses to include: '))
			profit_labels = [stock.symbol for stock in sorted_pl if stock.net_pl < 0 and (stock.net_pl*100/total_losses) >= threshold]
			profit_sizes = [(stock.net_pl/total_losses) for stock in sorted_pl if stock.net_pl < 0 and (stock.net_pl*100/total_losses) >= threshold]
			title = 'Itemized Losses > ' + str(threshold) + '%'
		else:
			profit_labels = [stock.symbol for stock in sorted_pl if stock.net_pl < 0]
			profit_sizes = [(stock.net_pl/total_losses) for stock in sorted_pl if stock.net_pl < 0]
			title = 'All Itemized Losses'

	#explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
	explode = None
	fig1, ax1 = plt.subplots()
	ax1.pie(profit_sizes, explode=explode, labels=profit_labels, autopct='%1.1f%%',
			shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	plt.title(title, fontsize=20)
	plt.show()

if __name__ == '__main__':
	generate_csv()
	stocks = itemize_stocks()
	calculate_itemized_pl(stocks)

	with open('stockwise_pl.csv', 'w') as outfile:
		writer = csv.writer(outfile, delimiter=',')
		writer.writerow(['SYMBOL', 'NET_P/L', '# BUYS/SELLS'])
		sorted_pl = sorted(stocks.values(), key=operator.attrgetter('net_pl'), reverse=True)
		total_pl = 0
		total_trades = 0
		total_profits = 0
		total_losses = 0
		
		for stock in sorted_pl:
			num_trades = len(stock.orders)
			writer.writerow([stock.symbol, '{0:.2f}'.format(stock.net_pl), len(stock.orders)])
			total_pl += stock.net_pl
			total_trades += num_trades
			
			if stock.net_pl > 0:
				total_profits += stock.net_pl
			else:
				total_losses += stock.net_pl
		writer.writerow(['Totals', total_pl, total_trades])
		print('Created', outfile.name, 'in this directory.')	
		print('------------------------------------------------')

	while True:
		piechart(sorted_pl, total_profits, total_losses)
		print('------------------------------------------------')
