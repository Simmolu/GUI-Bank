import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from turtle import update
from Bank import *
from Account import *
import time
from datetime import *
import sqlite3
from cryptography.fernet import Fernet



def drawScreen(window, act, screen, db, con):
    clearWindow(window)
    balance = tk.Label(window, text="Current Account Balance: $" + str(act.balance))
    balance.pack()
    info = db.execute("SELECT username, password, balance, date from users where username = ?", (act)).fetchall()[0]
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
                e = entryList[buttonNum]
                button = tk.Button(window, text=currentScreen["Buttons"][buttons]["text"], command=lambda: func(window, act, e.get()))
            else:
                button = tk.Button(window, text=currentScreen["Buttons"][buttons]["text"], command=lambda: func(window, act, screen))
            button.pack()
            buttonNum += 1
    except TypeError:
        pass

    back = tk.Button(window, text="Back", command=lambda: goBackMain(window, act, db, con), bg = 'grey')
    back.pack()


def login(window, db, con):
    acct = simpledialog.askstring("A", "Please enter your username.", parent=window)
    found = False
    for row in db.execute("SELECT username, password FROM users").fetchall()[0]:
        print(row)
        if row[0] == acct:
            curAct = acct
            found = True
            pwd = simpledialog.askstring("P", "Please enter your password.", parent=window, show="*")
            pwdattempts = 0
            while not row[1] == pwd:
                if (pwdattempts > 4):
                    messagebox.showerror("ERROR", "Too many attempts. Please try again later.")
                    goBackTitle(window, db, con)
                messagebox.showerror("Incorrect", "Incorrect Password. Please try again.")
                pwd = simpledialog.askstring("P", "Please enter your password.", parent=window)
                pwdattempts += 1
            return curAct
    if not found:
        messagebox.showerror("ERROR", "Account not found. Please try again.")
        goBackTitle(window, db, con)


def quit(window):
    window.destroy()


def clearWindow(window):
    for widget in window.winfo_children():
        widget.destroy()


def titlescreen(db, con):
    window = tk.Tk()
    window.title("Bank Application")
    window.geometry("720x480")
    clearWindow(window)
    my_font1 = ('times', 18, 'bold')
    lab = tk.Label(window, text="Python Bank", font=my_font1, pady=50)
    lab.pack()
    button1 = tk.Button(window, text="Account Creation", command=lambda: accounts(window, db, con), pady=30)
    button1.pack()
    bankio = tk.Button(window, text="User Login", command=lambda: main_menu(window, False, None, db, con), pady=30)
    bankio.pack()
    admin = tk.Button(window, text="Administrator login", command=lambda: adminLogin(window, False, db, con), pady=30)
    admin.pack()
    quitb = tk.Button(window, text="QUIT", command=lambda: quit(window), pady=30, bg = 'grey')
    quitb.pack()
    window.mainloop()



def goBackMain(window, act, db, con):
    main_menu(window, True, act, db, con)

def goBackTitle(window, db, con):
    window.destroy()
    return titlescreen(db, con)


def accounts(window, db, con):
    clearWindow(window)

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

    submit = tk.Button(window, text="Submit", command=lambda: createAccount(window, e1.get(), e2.get(), db, con))
    submit.grid(row = 5, column=1, pady=25)

    back = tk.Button(window, text="Back", command = lambda: goBackTitle(window, db, con), bg = 'grey')
    back.grid(row = 6, column = 1, pady = 10)

def createAccount(window, uName, pWord, db, con):
    accts = db.execute("SELECT username FROM users")
    for row in accts:
        usr = row[0]
        if usr == uName:
            messagebox.showerror("ERR", "Username Already taken.")
            return

    db.execute("INSERT INTO users(username, password, balance, date) VALUES(?,?,?,?)", (uName, pWord, 0, date.today()))
    con.commit()
    messagebox.showinfo("ACCT", "Account created with username " + uName)
    accounts(window, db, con)


def wipeAccounts(db, con):
    if messagebox.askyesno("S", "Are you sure you want to wipe the database?"):
        db.execute("DELETE FROM users")
        con.commit()

    return

def deleteAccount(window, db, con, uName):
    if messagebox.askyesno("S", "Are you sure you want to delete this account?"):
        db.execute("DELETE FROM users WHERE username = ?", (uName))
        con.commit()
        accountList(window, db, con)



def deposit(window, act, amt, db, con):
    db.execute("UPDATE users SET balance += amt WHERE uName = act")
    con.commit()
    drawScreen(window, act, "deposit", db, con)
    act.deposit(int(amt))


def withdraw(window, act, amt):
    act.withdraw(int(amt))


def adminLogin(window, flag, db, con):

    clearWindow(window)
    if not flag:
        answer = simpledialog.askstring("A", "Please Enter your admin login. ", parent=window)

        if not answer == "admin":
            messagebox.showerror("Denied", "Invalid Admin Password.")
            goBackTitle(window, db, con)

    label = tk.Label(window, text="Admin Login")
    button1 = tk.Button(window, text="List Accounts", command=lambda: accountList(window, db, con))
    button1.pack()
    button2 = tk.Button(window, text="Wipe Account Database", command=lambda: wipeAccounts(db, con))
    button2.pack()
    back = tk.Button(window, text="Back", command=lambda: goBackTitle(window, db, con), bg = 'grey')
    back.pack()


def accountList(window, db, con):

    clearWindow(window)
    window.title("Accounts")
    label = tk.Label(window, text="View All Accounts")
    label.pack()
    buttons = []
    # GRAB ALL ACCT INFO, PUT INTO TABLE/LIST AND THEN GRAB THE APPLICABLE NUMBER FOR ROW BC OTHERWISE IT JUST HAS THE LAST ONE
    ulist = []
    for row in db.execute("SELECT username FROM users"):
        ulist.append(row)

    print(ulist)
    for x in range(len(ulist)):
        func = funclist[1]
        uName = ulist[x][0]
        print(cur)
        btn = tk.Button(window, text=uName, command=lambda x=x: func(window, db, ulist[x], con))
        btn.pack()
        buttons.append(btn)
    back = tk.Button(window, text="Back", command=lambda: adminLogin(window, True, db, con), bg = 'grey')
    back.pack()

def displayaccountinfo(window, db, uName, con):

    clearWindow(window)
    window.title("Account Info")
    label = tk.Label(window, text="Showing info for account")
    label.pack()
    print(uName)
    info = db.execute("SELECT password, balance, date FROM users WHERE username = ?", (uName)).fetchall()[0]
    print(info)
    username = tk.Label(window, text="Username: " + uName[0])
    pwd = tk.Label(window, text="Password: " + info[0])
    bal = tk.Label(window, text="Balance: " + str(info[1]))
    datey = tk.Label(window, text="Date created: " + info[2])
    username.pack()
    pwd.pack()
    bal.pack()
    datey.pack()
    delo = tk.Button(window, text="Delete Account", command=lambda: deleteAccount(window, db, con, uName))
    delo.pack()
    back = tk.Button(window, text="Back", command=lambda: accountList(window, db, con), bg = 'grey')
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


def main_menu(window, flag, act, db, con):
    clearWindow(window)

    if not (flag):
        act = login(window, db, con)
    #drawScreen(window, "Deposit")

    main_menu_label = tk.Label(window, text="Welcome to your Bank Manager")
    main_menu_label.grid(row = 0, column = 1, padx = 300)

    button2 = tk.Button(window, text="Balance Check", command=lambda: drawScreen(window, act, "Balance", db, con))
    button2.grid(row = 2, column = 1)

    button3 = tk.Button(window, text="Deposit", command=lambda: drawScreen(window, act, "Deposit", db, con))
    button3.grid(row = 3, column = 1)

    button4 = tk.Button(window, text="Withdraw", command=lambda: drawScreen(window, act, "Withdraw", db, con))
    button4.grid(row = 4, column = 1)

    titleb = tk.Button(window, text="Return to Title Screen", command=lambda: goBackTitle(window, db, con))
    titleb.grid(row = 5, column = 1)

    quitb = tk.Button(window, text="QUIT", command=lambda: quit(window), bg = 'grey')
    quitb.grid(row = 7, column = 1, pady = 100)


funclist = [drawScreen, displayaccountinfo, accountList, adminLogin, withdraw]

con = sqlite3.connect("bank.db")
print("database accessed")
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users("
            "username, "
            "password, "
            "balance, "
            "date)")

testBank = Bank("Bank")

#testWindow = tk.Tk()
#accountList(testWindow, cur, con)

titlescreen(cur, con)
con.commit()
con.close()
print("database closed")