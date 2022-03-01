from faulthandler import disable
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
import pickle
from tkinter import messagebox
import valuecheck
import currency
import requests
import re

dict_of_portfolio={}
currencies =[
'USD', 'AED', 'BRL', 'CAD', 'CHF', 'CNY', 
'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'ILS', 'INR', 
'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 
'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 
'USD', 'ZAR']

class Window(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Portfolio Manager')
        self.iconbitmap('portfolio-manager/wallet.ico')

        self.l1 = ttk.Label(self, text = "Portfolio value:").grid(row = 0, column = 0, padx= 5, pady=5)
        self.t1 = tk.Text(self, height = 1, width = 20)

        self.l2 = ttk.Label(self, text = "Growth since last close (%):").grid(row = 1, column = 0, padx= 5, pady=5)
        self.t2 = tk.Text(self, height = 1, width = 20)

        self.b1 = ttk.Button(self, text = "REFRESH", command = self.refresh).grid(row = 2, column = 0, padx= 5, pady=5)

        self.refresh()

    def refresh_window(self, sum):
        self.t1.delete("1.0", tk.END)
        self.t1.insert(tk.END,sum)
        self.t1.grid(row = 0, column = 1)
        
    def change_currency(self, event):

        changed = float(self.sum / float(currency.currency_covnertion(self.clicked.get())))

        self.t1.delete("1.0", tk.END)
        self.t1.insert(tk.END,round(changed, 2))
        self.t1.grid(row = 0, column = 1)

    def refresh(self):
        self.sum = 0
        self.growth = 0
        for i in dict_of_portfolio:
            temp_sum = float(valuecheck.get_stock_value(i)) * float(dict_of_portfolio[i])
            self.growth += temp_sum * float(valuecheck.growth_percent(i))
            self.sum += temp_sum

        self.percent_growth = self.growth/self.sum * 100

        self.refresh_window(round(self.sum, 2))

        self.clicked = tk.StringVar()
        ttk.OptionMenu(self, self.clicked, *currencies, command=self.change_currency).grid(row = 0, column = 2)

        self.t2.delete("1.0", tk.END)
        self.t2.insert(tk.END,self.percent_growth)
        self.t2.grid(row = 1, column = 1)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Portfolio Manager')
        self.iconbitmap('portfolio-manager/wallet.ico')

        self.l1 = ttk.Label(self, text = "SYMBOL", font=("Helvetica",12)).grid(row = 0, column = 0, padx= 5, pady=5)
        self.l2 = ttk.Label(self, text = "AMOUNT", font=("Helvetica",12)).grid(row = 0, column = 2, padx= 5, pady=5)
        
        self.b1 = ttk.Button(self, text = "ADD", command = self.add_to_list)
        self.b1.grid(row = 2, column = 1, padx= 5, pady=5)
        self.b1.config(state='active')
        self.b2 = ttk.Button(self, text = "IMPORT", command = self.import_from_file).grid(row = 3, column = 0, padx= 5, pady=5)
        self.b3 = ttk.Button(self, text = "EXPORT", command = self.export_to_file).grid(row = 3, column = 2, padx= 5, pady=5)
        self.b4 = ttk.Button(self, text = "NEXT", command = self.open_window).grid(row = 3, column = 1, padx= 5, pady=5)
        self.b5 = ttk.Button(self, text = "CLEAR LAST", command = self.clear_last).grid(row = 2, column = 2, padx= 5, pady=5)
        self.b6 = ttk.Button(self, text = "CLEAR ALL", command = self.clear_all).grid(row = 2, column = 0, padx= 5, pady=5)


        self.e1_value = tk.StringVar()
        self.e1 = ttk.Entry(self, textvariable = self.e1_value).grid(row = 1, column = 0, padx= 5, pady=5)
        self.e2_value = tk.StringVar()
        self.e2 = ttk.Entry(self, textvariable = self.e2_value).grid(row = 1, column = 2, padx= 5, pady=5)


    def open_window(self):
        if dict_of_portfolio:
            window = Window(self)
            window.grab_set()
        else:
            messagebox.showwarning(title="Warning", message="Empty portfolio")

    def incorrect_value(self):
        self.l3 = tk.Label(self, text = "Enter correct value", font=("Helvetica",8),fg="red").grid(row = 2, column = 2, padx= 5, pady=5)
        self.e2_value.set('')

    def add_to_list(self):

        try:
            if len(self.e2_value.get()) == 0 or float(self.e2_value.get()) < 0:
                    self.incorrect_value()
                    return None
            symbol = str(self.e1_value.get())
            amount = float(self.e2_value.get())
        except ValueError:
            self.incorrect_value()
            return None

        url = "https://finance.yahoo.com/quote/"+ symbol + "?p="+ symbol + "&.tsrc=fin-srch"

        response = requests.get(url)

        if response.status_code == 200:
            dict_of_portfolio[symbol] = amount
            self.e1_value.set('')
            self.e2_value.set('')

            print_records = ''
            for i in dict_of_portfolio :
                print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"

            if self.labelframe.winfo_exists:
                self.labelframe.destroy()
            
            if self.l3.winfo_exists:
                self.l3.destroy()

            self.labelframe = LabelFrame(self, text="Portfolio:")
            self.labelframe.grid(row=6, column=0, columnspan = 2, padx = 10, pady = 10)

            self.l3 = Label(self.labelframe, text = print_records, font=("Helvetica",12))
            self.l3.grid(row=5, column=0, columnspan = 2, padx = 10, pady = 10)
            
        elif response.status_code != 200:
            messagebox.showwarning(title="Warning", message="Symbol unknown")

    def import_from_file(self):
        global dict_of_portfolio
        a_file = open("data.pkl", "rb")
        dict_of_portfolio = pickle.load(a_file)

        print_records = ''
        for i in dict_of_portfolio :
            print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"
        
        self.labelframe = LabelFrame(self, text="Portfolio:")
        self.labelframe.grid(row=6, column=0, columnspan = 2, padx = 10, pady = 10)

        self.l3 = Label(self.labelframe, text = print_records, font=("Helvetica",12))
        self.l3.grid(row=5, column=0, columnspan = 2, padx = 10, pady = 10)

    def export_to_file(self):
        a_file = open("data.pkl", "wb")
        pickle.dump(dict_of_portfolio, a_file)
        a_file.close()

    def clear_last(self):
        try:
            dict_of_portfolio.popitem()

            print_records = ''
            for i in dict_of_portfolio :
                print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"

            self.labelframe.destroy()
            self.l3.destroy()

            if len(dict_of_portfolio) > 0:
                self.labelframe = LabelFrame(self, text="Portfolio:")
                self.labelframe.grid(row=6, column=0, columnspan = 2, padx = 10, pady = 10)

                self.l3 = Label(self.labelframe, text = print_records, font=("Helvetica",12))
                self.l3.grid(row=5, column=0, columnspan = 2, padx = 10, pady = 10)
        except KeyError:
            messagebox.showwarning(title="Warning", message="Empty portfolio")
    
    def clear_all(self):
        if len(dict_of_portfolio) > 0:
            dict_of_portfolio.clear()

            self.labelframe.destroy()
            self.l3.destroy()
        else:
            messagebox.showwarning(title="Warning", message="Portfolio already empty")


if __name__ == "__main__":
    app = App()
    app.mainloop()

    # TODO make better file saving