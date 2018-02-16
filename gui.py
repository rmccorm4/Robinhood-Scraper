#import PyQt5
from tkinter import *
import finance_tracker

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_window()

	def init_window(self):
		self.master.title = 'GUI'
		self.pack(fill=BOTH, expand=1)
		quitButton = Button(self, text="Quit", command=self.quit_gui)
		quitButton.place(x=0, y=0)
		csvButton = Button(self, text="Generate CSV file",
							command=self.get_csv)
		csvButton.place(x=10, y=0)
	
	def quit_gui(self):
		exit()

	def get_csv(self):
		finance_tracker.generate_csv()

def start_gui():
	root = Tk()
	root.geometry("800x600")
	app = Window(root)
	root.mainloop()

if __name__ == '__main__':
	start_gui()
