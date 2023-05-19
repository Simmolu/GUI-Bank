import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from Bank import *
from Account import *



def clearWindow(window):
    for widget in window.winfo_children():
        widget.destroy()


def goBack(window):
    window.destroy()
    return main_menu(bankList)

def submenu1(window):
    clearWindow(window)

    window.title("Account Creation")
    answer = simpledialog.askstring("Bank Name", "Please Enter Bank Name: ", parent=window)

    found = False
    for banks in bankList:
        if answer == banks.name:
            bank = banks
            found = True
    if not found:
        messagebox.showerror("Error", "Bank not found. Sorry!")
        goBack(window)



    if bank.numAccounts == 10:
        messagebox.showerror("Error", "Bank already has 10 accounts. Sorry!")
        window.destroy()
        goBack(window)


    label = tk.Label(window, text="Account Creation")
    label.grid(row = 0, column = 1, padx = 300)

    e1 = tk.Entry(window)
    e2 = tk.Entry(window)

    label1 = tk.Label(window, text="Please enter your Desired Username: ")
    label1.grid(row = 1, column= 1, pady = 10)
    e1.grid(row = 2, column = 1)

    label2 = tk.Label(window, text="Please enter your Desired Password: ")
    label2.grid(row=3, column=1)
    e2.grid(row = 4, column = 1)

    submit = tk.Button(window, text="Submit", command=lambda: bank.addAccount(Account(e1.get(), e2.get(), bank.numAccounts)))
    submit.grid(row = 5, column=1, pady=25)

    back = tk.Button(window, text="Back", command = lambda: goBack(window))
    back.grid(row = 6, column = 1, pady = 10)


def submenu2():
    window = tk.Toplevel()
    window.title("Balance Check")

    label = tk.Label(window, text="Balance Check")
    label.pack()

    # Add other widgets and configure layout

    # Handle events

def submenu3():
    window = tk.Toplevel()
    window.title("Deposit")

    label = tk.Label(window, text="Deposit")
    label.pack()

    # Add other widgets and configure layout

    # Handle events

def submenu4():
    window = tk.Toplevel()
    window.title("Withdraw")

    label = tk.Label(window, text="Withdraw")
    label.pack()

    # Add other widgets and configure layout

    # Handle events

def adminLogin():

    window = tk.Toplevel()
    window.title("Admin Login")
    answer = simpledialog.askstring("A", "Please Enter your admin login. ", parent=window)

    if not answer == "nutballs":
        messagebox.showerror("Denied", "Invalid Admin Password.")
        window.destroy()
        return main_menu(bankList)

    label = tk.Label(window, text="Admin Login")
    button1 = tk.Button(window, text="Create Bank", command=createBank)
    button1.grid(row=0, column=1, padx=100)

    button2 = tk.Button(window, text="Delete Bank", command=deleteBank)
    button2.grid(row=1, column=1, pady = 50)

    window.mainloop()


def createBank():
    window = tk.Toplevel()
    window.title("Bank create")
    newBank = simpledialog.askstring("C", "Please enter name of new bank.", parent=window)

    newBanker = Bank(newBank)
    bankList.append(newBanker)
    messagebox.showinfo("Created", f"Bank {newBank} has been created")
    window.destroy()
    return



def deleteBank():
    window = tk.Toplevel()
    window.title("Bank delete")
    newBank = simpledialog.askstring("D", "Please enter name of bank.", parent=window)

    bankFound = False
    for banks in bankList:
        if banks.name == newBank:
            bankList.remove(banks)
            bankFound = True

    if not bankFound:
        messagebox.showerror("ERROR", "Bank does not exist.")
        return
    else:
        messagebox.showinfo("Removed", "Bank has been removed.")
        return



def main_menu(bank):
    window = tk.Tk()
    window.title("Bank Application")
    window.geometry("720x480")

    main_menu_label = tk.Label(window, text="Main Menu Title")
    main_menu_label.grid(row = 0, column = 1, padx = 300)

    button1 = tk.Button(window, text="Account Creation", command=lambda: submenu1(window))
    button1.grid(row = 1, column = 1)

    button2 = tk.Button(window, text="Balance Check", command=submenu2)
    button2.grid(row = 2, column = 1)

    button3 = tk.Button(window, text="Deposit", command=submenu3)
    button3.grid(row = 3, column = 1)

    button4 = tk.Button(window, text="Withdraw", command=submenu4)
    button4.grid(row = 4, column = 1)

    button5 = tk.Button(window, text="Admin Login", command=adminLogin)
    button5.grid(row = 5, column = 1, pady= 50)
    window.mainloop()

testBank = Bank("Bank")

bankList = []

bankList.append(testBank)

main_menu(bankList)


