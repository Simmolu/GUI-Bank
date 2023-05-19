import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from Bank import *
from Account import *
import time
from datetime import *


def clearWindow(window):
    for widget in window.winfo_children():
        widget.destroy()


def goBack(window):
    window.destroy()
    return main_menu()


def accounts(window):
    clearWindow(window)

    window.title("Account Creation")

    bank = testBank

    if bank.numAccounts == 10:
        messagebox.showerror("Error", "Bank already has 10 accounts. Sorry!")
        goBack(window)

    label = tk.Label(window, text="Account Creation")
    label.grid(row = 0, column = 1, padx = 300)

    e1 = tk.Entry(window)
    e2 = tk.Entry(window, show="*")

    label1 = tk.Label(window, text="Please enter your Desired Username: ")
    label1.grid(row = 1, column= 1, pady = 10)
    e1.grid(row = 2, column = 1)

    label2 = tk.Label(window, text="Please enter your Desired Password: ")
    label2.grid(row=3, column=1)
    e2.grid(row = 4, column = 1)

    submit = tk.Button(window, text="Submit", command=lambda: bank.addAccount(Account(e1.get(), e2.get(), bank.numAccounts, date.today())))
    submit.grid(row = 5, column=1, pady=25)

    back = tk.Button(window, text="Back", command = lambda: goBack(window))
    back.grid(row = 6, column = 1, pady = 10)


def balance(window):
    clearWindow(window)
    window.title("balance")
    acct = simpledialog.askstring("A", "Please enter your username.")
    found = False

    for accountie in testBank.accountList:
        if accountie.uName == acct:
            curAct = accountie
            found = True
            break
    if not found:
        messagebox.showerror("ERROR", "Account not found. Please try again.")
        goBack(window)

    label = tk.Label(window, text="Balance Check")
    label.pack()
    label = tk.Label(window, text="Current Balance: $" + str(curAct.balance))
    label.pack()

    butt = tk.Button(window, text="Add money?", command=lambda: deposit(window))
    butt.pack()

    back = tk.Button(window, text="Back", command=lambda: goBack(window))
    back.pack()


def deposit(window):
    window = tk.Toplevel()
    window.title("Deposit")

    label = tk.Label(window, text="Deposit")
    label.pack()

    # Add other widgets and configure layout

    # Handle events

def withdraw(window):
    window = tk.Toplevel()
    window.title("Withdraw")

    label = tk.Label(window, text="Withdraw")
    label.pack()

def adminLogin(window):

    clearWindow(window)
    window.title("Admin Login")
    answer = simpledialog.askstring("A", "Please Enter your admin login. ", parent=window)

    if not answer == "admin":
        messagebox.showerror("Denied", "Invalid Admin Password.")
        goBack(window)

    label = tk.Label(window, text="Admin Login")
    button1 = tk.Button(window, text="List Accounts", command=lambda: accountList(window))
    button1.pack()

    #button2 = tk.Button(window, text="Delete Bank", command=deleteBank)
    #button2.grid(row=1, column=1, pady = 50)

def accountList(window):

    clearWindow(window)
    window.title("Accounts")
    label = tk.Label(window, text="View All Accounts")
    label.pack()
    labelList = []
    for account in testBank.accountList:
        uName = account.uName
        butt = tk.Button(window, text=uName, command=lambda: displayaccountinfo(window, account))
        labelList.append(butt)
        butt.pack()
    back = tk.Button(window, text="Back", command=lambda: goBack(window))
    back.pack()

def displayaccountinfo(window, account):

    clearWindow(window)
    window.title("Account Info")
    label = tk.Label(window, text="Showing info for account")
    label.pack()

    username = tk.Label(window, text="Username: " + account.uName)
    pwd = tk.Label(window, text="Password: " + account.pWord)
    bal = tk.Label(window, text="Balance: " + str(account.balance))
    datey = tk.Label(window, text="Date created: " + str(account.timeCreated))
    username.pack()
    pwd.pack()
    bal.pack()
    datey.pack()
    back = tk.Button(window, text="Back", command=lambda: accountList(window))
    back.pack()

def main_menu():
    window = tk.Tk()
    window.title("Bank Application")
    window.geometry("720x480")

    main_menu_label = tk.Label(window, text="Welcome to your Bank Manager")
    main_menu_label.grid(row = 0, column = 1, padx = 300)

    button1 = tk.Button(window, text="Account Creation", command=lambda: accounts(window))
    button1.grid(row = 1, column = 1)

    button2 = tk.Button(window, text="Balance Check", command=lambda: balance(window))
    button2.grid(row = 2, column = 1)

    button3 = tk.Button(window, text="Deposit", command=lambda: deposit(window))
    button3.grid(row = 3, column = 1)

    button4 = tk.Button(window, text="Withdraw", command=lambda: withdraw(window))
    button4.grid(row = 4, column = 1)

    button5 = tk.Button(window, text="Admin Login", command=lambda: adminLogin(window))
    button5.grid(row = 5, column = 1, pady= 50)
    window.mainloop()

global testBank
testBank = Bank("Bank")

testeo = Account("test", "test", 0, date.today())
testBank.accountList.append(testeo)

main_menu()

