from tkinter import *
import pickle
from tkinter import messagebox
import valuecheck
import currency

dict_of_portfolio={}
currencies =['AED', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 
'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HUF', 'IDR', 'ILS', 'INR', 
'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 
'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'USD', 'ZAR', 'ZAR']

class Window(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Toplevel Window')

        self.l1 = Label(self, text = "Portfolio value:").grid(row = 0, column = 0, padx= 5, pady=5)
        self.t1 = Text(self, height = 1, width = 20)
        

        self.sum = 0
        for i in dict_of_portfolio :
            self.sum += float(valuecheck.get_stock_value(i)) * float(dict_of_portfolio[i])

        self.refresh_window(self.sum)

        self.clicked = StringVar()
        self.clicked.set('CHF')
        OptionMenu(self, self.clicked, *currencies, command=self.change_currency).grid(row = 0, column = 2)
        

    def refresh_window(self, sum):
        self.t1.delete("1.0", END)
        self.t1.insert(END,sum)
        self.t1.grid(row = 0, column = 1)
        
    def change_currency(self, event):

        changed = float(self.sum / float(currency.currency_covnertion(self.clicked.get())))

        self.t1.delete("1.0", END)
        self.t1.insert(END,changed)
        self.t1.grid(row = 0, column = 1)

class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Main Window')

        # place a button on the root window
        self.l1 = Label(self, text = "SYMBOL").grid(row = 0, column = 0, padx= 5, pady=5)
        self.l2 = Label(self, text = "AMOUNT").grid(row = 0, column = 2, padx= 5, pady=5)

        self.e1_value = StringVar()
        self.e1 = Entry(self, textvariable = self.e1_value).grid(row = 1, column = 0, padx= 5, pady=5)
        self.e2_value = StringVar()
        self.e2 = Entry(self, textvariable = self.e2_value).grid(row = 1, column = 2, padx= 5, pady=5)

        self.b1 = Button(self, text = "ADD", command = self.add_to_list).grid(row = 2, column = 1, padx= 5, pady=5)
        self.b2 = Button(self, text = "IMPORT", command = self.import_from_file).grid(row = 3, column = 0, padx= 5, pady=5)
        self.b3 = Button(self, text = "EXPORT", command = self.export_to_file).grid(row = 3, column = 2, padx= 5, pady=5)
        self.b4 = Button(self, text = "NEXT", command = self.open_window).grid(row = 4, column = 1, padx= 5, pady=5)

    def open_window(self):
        if dict_of_portfolio:
            window = Window(self)
            window.grab_set()
        else:
            messagebox.showwarning(title="Warning", message="Empty portfolio")

    def add_to_list(self):
        symbol = str(self.e1_value.get())
        amount = float(self.e2_value.get())

        dict_of_portfolio[symbol] = amount
        self.e1_value.set('')
        self.e2_value.set('')

        print_records = ''
        for i in dict_of_portfolio :
            print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"

        self.l3 = Label(self, text = print_records).grid(row=5, column=0)

    def import_from_file(self):
        global dict_of_portfolio
        a_file = open("data.pkl", "rb")
        dict_of_portfolio = pickle.load(a_file)

        print_records = ''
        for i in dict_of_portfolio :
            print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"
        
        self.l3 = Label(self, text = print_records).grid(row=5, column=0)

    def export_to_file(self):
        a_file = open("data.pkl", "wb")
        pickle.dump(dict_of_portfolio, a_file)
        a_file.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()

    # root.geometry("700x300")
    # label_city=Label(root, font="Calibri,12,bold")