import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from turtle import update
from Bank import *
from Account import *
import time
from datetime import *



def drawScreen(window, act, screen):
    clearWindow(window)
    balance = tk.Label(window, text="Current Account Balance: $" + str(act.balance))
    balance.pack()
    currentScreen = bankScreens[screen]
    entryList = []
    try:
        for labels in currentScreen["Labels"].values():
            label = tk.Label(window, text=labels)
            label.pack()
    except TypeError:
        pass
    try:
        for x in range(currentScreen["Entry"]):
            entry = tk.Entry(window)
            entry.pack()
            entryList.append(entry)
    except TypeError:
        pass
    try:
        for buttons in currentScreen["Buttons"]:
            buttonNum = 0
            func = currentScreen["Buttons"][buttons]["command"]
            if len(entryList) > 0:
                print("Generating entry buttons")
                e = entryList[buttonNum]
                button = tk.Button(window, text=currentScreen["Buttons"][buttons]["text"], command=lambda: func(window, act, e.get()))
            else:
                button = tk.Button(window, text=currentScreen["Buttons"][buttons]["text"], command=lambda: func(window, act, screen))
            button.pack()
            buttonNum += 1
    except TypeError:
        pass

    print(len(entryList))

    back = tk.Button(window, text="Back", command=lambda: goBackMain(window))
    back.pack()


def login(window):
    acct = simpledialog.askstring("A", "Please enter your username.", parent=window)
    found = False
    for accountie in testBank.accountList:
        if accountie.uName == acct:
            curAct = accountie
            found = True
            pwd = simpledialog.askstring("P", "Please enter your password.", parent=window, show="*")
            pwdattempts = 0
            while not curAct.pWord == pwd:
                if (pwdattempts > 4):
                    messagebox.showerror("ERROR", "Too many attempts. Please try again later.")
                    goBackTitle(window)
                messagebox.showerror("Incorrect", "Incorrect Password. Please try again.")
                pwd = simpledialog.askstring("P", "Please enter your password.", parent=window)
                pwdattempts += 1
            return curAct
    if not found:
        messagebox.showerror("ERROR", "Account not found. Please try again.")
        goBackTitle(window)


def quit(window):
    window.destroy()


def clearWindow(window):
    for widget in window.winfo_children():
        widget.destroy()


def titlescreen():
    window = tk.Tk()
    window.title("Bank Application")
    window.geometry("720x480")
    clearWindow(window)
    my_font1 = ('times', 18, 'bold')
    lab = tk.Label(window, text="Python Bank", font=my_font1, pady=50)
    lab.pack()
    button1 = tk.Button(window, text="Account Creation", command=lambda: accounts(window), pady=30)
    button1.pack()
    bankio = tk.Button(window, text="User Login", command=lambda: main_menu(window), pady=30)
    bankio.pack()
    admin = tk.Button(window, text="Administrator login", command=lambda: adminLogin(window, False), pady=30)
    admin.pack()
    quitb = tk.Button(window, text="QUIT", command=lambda: quit(window), pady=30)
    quitb.pack()
    window.mainloop()



def goBackMain(window):
    window.destroy()
    return main_menu(window)

def goBackTitle(window):
    window.destroy()
    return titlescreen()


def accounts(window):
    clearWindow(window)


    if testBank.numAccounts == 10:
        messagebox.showerror("Error", "Bank already has 10 accounts. Sorry!")
        goBackTitle(window)

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

    submit = tk.Button(window, text="Submit", command=lambda: createAccount(e1.get(), e2.get()))
    submit.grid(row = 5, column=1, pady=25)

    back = tk.Button(window, text="Back", command = lambda: goBackTitle(window))
    back.grid(row = 6, column = 1, pady = 10)

def createAccount(uName, pWord):
    for account in testBank.accountList:
        usr = account.uName
        if usr == uName:
            messagebox.showerror("ERR", "Username Already taken.")
            return

    testBank.addAccount(Account(uName, pWord, testBank.numAccounts, date.today()))



def deposit(window, act, amt):
    act.deposit(int(amt))


def withdraw(window, act, amt):
    act.withdraw(int(amt))


def adminLogin(window, flag):

    clearWindow(window)
    if not flag:
        answer = simpledialog.askstring("A", "Please Enter your admin login. ", parent=window)

        if not answer == "admin":
            messagebox.showerror("Denied", "Invalid Admin Password.")
            goBackTitle(window)

    label = tk.Label(window, text="Admin Login")
    button1 = tk.Button(window, text="List Accounts", command=lambda: accountList(window))
    button1.pack()

    back = tk.Button(window, text="Back", command=lambda: goBackTitle(window))
    back.pack()


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
    back = tk.Button(window, text="Back", command=lambda: adminLogin(window, True))
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


bankScreens = {
    "Deposit": {
        "Labels": {
            1: "Depositing",
            2: "How much do you want to deposit?"
        },
        "Buttons": {
            1: {
                "text": "Deposit Funds",
                "command": deposit
            },
        },
        "Entry": 1
    },
    "Withdraw": {
        "Labels": {
            1: "Withdraw",
            2: "How much do you want to withdraw?"
        },
        "Buttons": {
            1: {
                "text": "Withdraw Amount",
                "command": withdraw
            }
        },
        "Entry": 1
    },
    "Balance": {
        "Labels": {
            1: "Balance Check"
        },
        "Buttons": {
            1: {
                "text": "Add Money?",
                "command": drawScreen
            },
            2: {
                "text": "Withdraw?",
                "command": withdraw
            }
        },
        "Entry": 0
    }
}


def main_menu(window):
    clearWindow(window)
    act = login(window)
    #drawScreen(window, "Deposit")

    main_menu_label = tk.Label(window, text="Welcome to your Bank Manager")
    main_menu_label.grid(row = 0, column = 1, padx = 300)

    button2 = tk.Button(window, text="Balance Check", command=lambda: drawScreen(window, act, "Balance"))
    button2.grid(row = 2, column = 1)

    button3 = tk.Button(window, text="Deposit", command=lambda: drawScreen(window, act, "Deposit"))
    button3.grid(row = 3, column = 1)

    button4 = tk.Button(window, text="Withdraw", command=lambda: drawScreen(window, act, "Withdraw"))
    button4.grid(row = 4, column = 1)

    quitb = tk.Button(window, text="QUIT", command=lambda: quit(window))
    quitb.grid(row = 6, column = 1, pady = 100)



testBank = Bank("Bank")

testeo = Account("test", "test", 0, date.today())
testBank.accountList.append(testeo)

titlescreen()

