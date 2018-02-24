#import PyQt5
from tkinter import *
import robinhood_pl

class Window(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.top = Toplevel(master)
		self.init_window()

	def init_window(self):
		self.master.title('GUI')
		self.pack(fill=BOTH, expand=1)
		self.quitButton = Button(self, text="Quit", command=self.quit_gui)
		#quitButton.place(x=0, y=0)
		self.quitButton.pack()
		self.csvButton = Button(self, text="Generate CSV file",
							command=self.get_csv)
		#csvButton.place(x=10, y=0)
		self.csvButton.pack()

		self.loginButton=Button(self.master, text="click me!", command=self.popup)
		self.loginButton.pack()
		# TBD
		#self.b2=Button(self.master, text="print value", command=self.get_csv(self.w.username, self.w.password))
		#self.b2.pack()
	
	def quit_gui(self):
		exit()

	def get_csv(self):
		robinhood_pl.generate_csv()

	def popup(self):
		self.w=PopUpWindow(self.master)
		self.loginButton["state"] = "disabled" 
		self.master.wait_window(self.w.top)
		self.loginButton["state"] = "normal"

	#def getUsername(self):
	#	return self.username

class PopUpWindow(object):
	def __init__(self, master):
		top = self.top=Toplevel(master)
		self.l=Label(top,text="RobinHood Login")
		self.l.pack()
		#self.e=Entry(top)
		self.userLogin = Entry(top, text="Username: ", width=20)
		#self.e.pack()
		self.userLogin.pack()
		self.pwLogin = Entry(top, text="password: ", width=20, show='*')
		self.pwLogin.pack()
		self.b=Button(top,text='Ok',command=self.cleanup)
		self.b.pack()
	
	def cleanup(self):
		#self.value=self.e.get()
		self.username = self.userLogin.get()
		self.password = self.pwLogin.get()
		self.top.destroy()

def start_gui():
	root = Tk()
	root.geometry("800x600")
	app = Window(root)
	root.mainloop()

if __name__ == '__main__':
	start_gui()
