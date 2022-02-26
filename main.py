from tkinter import *
import pickle
from tkinter import messagebox
import valuecheck
import currency

window = Tk()
window.title("Portfolio Manager")

dict_of_portfolio={}

currencies =['AED', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 
'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HUF', 'IDR', 'ILS', 'INR', 
'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON', 
'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'USD', 'ZAR', 'ZAR']


def add_to_list():
    symbol = str(e1_value.get())
    amount = float(e2_value.get())

    dict_of_portfolio[symbol] = amount
    print(dict_of_portfolio)
    e1_value.set('')
    e2_value.set('')

    print_records = ''
    for i in dict_of_portfolio :
        print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"
    
    Label(window, text=print_records).grid(row=5, column=0)

def import_from_file():
    global dict_of_portfolio
    a_file = open("data.pkl", "rb")
    dict_of_portfolio = pickle.load(a_file)
    print(dict_of_portfolio)

    print_records = ''
    for i in dict_of_portfolio :
        print_records += (str(i) + " : " + str(dict_of_portfolio[i])) + "\n"
    
    Label(window, text=print_records).grid(row=5, column=0)

def export_to_file():
    a_file = open("data.pkl", "wb")
    pickle.dump(dict_of_portfolio, a_file)
    a_file.close()

def OptionMenu_Select(chosen, sum):
    global t1
    different_currency = float(sum / float(currency.currency_covnertion(chosen)))
    t1.delete("1.0", END)
    t1.insert(END,different_currency)


def nex_win():
    # To prevent calculating an empty portfolio
    global t1
    if dict_of_portfolio:
        
        new= Toplevel(window)
        new.title("Next step")
        Label(new, text = "Portfolio value:").grid(row = 0, column = 0, padx= 5, pady=5)

        sum = 0
        for i in dict_of_portfolio :
            sum += float(valuecheck.get_stock_value(i)) * float(dict_of_portfolio[i])


        t1 = Text(new, height = 1, width = 20)
        t1.delete("1.0", END)
        t1.insert(END,sum)
        t1.grid(row = 0, column = 1)

        clicked = StringVar()
        clicked.set('USD')
        drop = OptionMenu(new, clicked, *currencies).grid(row = 0, column = 2)
        print(clicked)


    else:
        messagebox.showwarning(title="Warning", message="Empty portfolio")
    


l1 = Label(window, text = "SYMBOL").grid(row = 0, column = 0, padx= 5, pady=5)
l2 = Label(window, text = "AMOUNT").grid(row = 0, column = 2, padx= 5, pady=5)

e1_value = StringVar()
e1 = Entry(window, textvariable = e1_value).grid(row = 1, column = 0, padx= 5, pady=5)
e2_value = StringVar()
e2 = Entry(window, textvariable = e2_value).grid(row = 1, column = 2, padx= 5, pady=5)

b1 = Button(window, text = "ADD", command = add_to_list).grid(row = 2, column = 1, padx= 5, pady=5)
b2 = Button(window, text = "IMPORT", command = import_from_file).grid(row = 3, column = 0, padx= 5, pady=5)
b3 = Button(window, text = "EXPORT", command = export_to_file).grid(row = 3, column = 2, padx= 5, pady=5)
b4 = Button(window, text = "NEXT", command = nex_win).grid(row = 4, column = 1, padx= 5, pady=5)


window.mainloop()