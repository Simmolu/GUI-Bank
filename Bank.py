import sqlite3
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from datetime import *


class Bank:

  def accounts(self):
    self.clearWindow()

    label = tk.Label(self.window, text="Account Creation")
    label.grid(row=0, column=1, padx=300)

    e1 = tk.Entry(self.window)
    e2 = tk.Entry(self.window, show="*")

    label1 = tk.Label(self.window, text="Please enter your Desired Username: ")
    label1.grid(row=1, column=1, pady=10)
    e1.grid(row=2, column=1)

    label2 = tk.Label(self.window, text="Please enter your Desired Password: ")
    label2.grid(row=3, column=1)
    e2.grid(row=4, column=1)

    submit = tk.Button(
      self.window,
      text="Submit",
      command=lambda: self.createAccount(e1.get(), e2.get()))
    submit.grid(row=5, column=1, pady=25)

    back = tk.Button(self.window,
                     text="Back",
                     command=lambda: self.titlescreen(),
                     bg='grey')
    back.grid(row=6, column=1, pady=10)

  def createAccount(self, uName, pWord):
    accts = self.cur.execute("SELECT username FROM users")
    for row in accts:
      usr = row[0]
      if usr == uName:
        messagebox.showerror("ERR", "Username Already taken.")
        return
    self.cur.execute(
      "INSERT INTO users(username, password, balance, date) VALUES(?,?,?,?)",
      (uName, pWord, 0, date.today()))
    self.con.commit()
    messagebox.showinfo("ACCT", "Account created with username " + uName)
    self.accounts()

  def drawScreen(self, act, screen):
    self.clearWindow()
    info = self.cur.execute(
      "SELECT username, password, balance, date from users WHERE username = ?",
      (act,)).fetchall()[0]
    bal = info[2]
    balance = tk.Label(self.window, text="Current Account Balance: $" + str(bal))
    balance.pack()
    currentScreen = self.screens[screen]
    entryList = []
    try:
      for labels in currentScreen["Labels"].values():
        label = tk.Label(self.window, text=labels)
        label.pack()
    except TypeError:
      pass
    try:
      for x in range(currentScreen["Entry"]):
        entry = tk.Entry(self.window)
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
          button = tk.Button(
            self.window,
            text=currentScreen["Buttons"][buttons]["text"],
            command=lambda: func(act, e.get(), bal))
        else:
          button = tk.Button(self.window,
                             text=currentScreen["Buttons"][buttons]["text"],
                             command=lambda: func(act, screen))
        button.pack()
        buttonNum += 1
    except TypeError:
      pass

    back = tk.Button(self.window,
                     text="Back",
                     command=lambda: self.main_menu(True, act),
                     bg='grey')
    back.pack()

  def login(self):
    acct = simpledialog.askstring("A",
                                  "Please enter your username.",
                                  parent=self.window)
    found = False
    for row in self.cur.execute("SELECT username, password FROM users"):
      if row[0] == acct:
        curAct = acct
        found = True
        pwd = simpledialog.askstring("P",
                                     "Please enter your password.",
                                     parent=self.window,
                                     show="*")
        pwdattempts = 0
        while not row[1] == pwd:
          if pwdattempts > 4:
            messagebox.showerror("ERROR",
                                 "Too many attempts. Please try again later.")
            self.titlescreen()
          messagebox.showerror("Incorrect",
                               "Incorrect Password. Please try again.")
          pwd = simpledialog.askstring("P",
                                       "Please enter your password.",
                                       parent=self.window)
          pwdattempts += 1
        return curAct
    if not found:
      messagebox.showerror("ERROR", "Account not found. Please try again.")
      self.titlescreen()

  def quit(self):
    self.window.destroy()

  def clearWindow(self):
    for widget in self.window.winfo_children():
      widget.destroy()

  def titlescreen(self):
    self.window.title("Bank Application")
    self.window.geometry("720x480")
    self.clearWindow()
    my_font1 = ('times', 18, 'bold')
    lab = tk.Label(self.window, text="Python Bank", font=my_font1, pady=50)
    lab.pack()
    button1 = tk.Button(self.window,
                        text="Account Creation",
                        command=lambda: self.accounts(),
                        pady=30)
    button1.pack()
    bankio = tk.Button(self.window,
                       text="User Login",
                       command=lambda: self.main_menu(False, None),
                       pady=30)
    bankio.pack()
    admin = tk.Button(self.window,
                      text="Administrator login",
                      command=lambda: self.adminLogin(False),
                      pady=30)
    admin.pack()
    quitb = tk.Button(self.window,
                      text="QUIT",
                      command=lambda: self.quit(),
                      pady=30,
                      bg='grey')
    quitb.pack()

  def main_menu(self, flag, act):
    self.clearWindow()

    if not (flag):
      act = self.login()
    # drawScreen(window, "Deposit")

    main_menu_label = tk.Label(self.window, text="Welcome to your Bank Manager")
    main_menu_label.grid(row=0, column=1, padx=300)

    button2 = tk.Button(
      self.window,
      text="Balance Check",
      command=lambda: self.drawScreen(act, "Balance"))
    button2.grid(row=2, column=1)

    button3 = tk.Button(
      self.window,
      text="Deposit",
      command=lambda: self.drawScreen(act, "Deposit"))
    button3.grid(row=3, column=1)

    button4 = tk.Button(
      self.window,
      text="Withdraw",
      command=lambda: self.drawScreen(act, "Withdraw"))
    button4.grid(row=4, column=1)

    titleb = tk.Button(self.window,
                       text="Return to Title Screen",
                       command=lambda: self.titlescreen())
    titleb.grid(row=5, column=1)

    quitb = tk.Button(self.window,
                      text="QUIT",
                      command=lambda: self.quit(),
                      bg='grey')
    quitb.grid(row=7, column=1, pady=100)

  def deposit(self, act, amt, bal):
    self.cur.execute("UPDATE users SET balance = ? WHERE username = ?",
               ((int(amt) + bal), act))
    self.con.commit()
    self.drawScreen(act, "Deposit",)

  def withdraw(self, act, amt, bal):
    if bal-int(amt) < 0:
      messagebox.showerror("$", "Insufficent balance.")
      return
    self.cur.execute("UPDATE users SET balance = ? WHERE username = ?",
               (bal - (int(amt)), act))
    self.con.commit()
    self.drawScreen(act, "Withdraw")

  def adminLogin(self, flag):

    self.clearWindow()
    if not flag:
      answer = simpledialog.askstring("A",
                                      "Please Enter your admin login. ",
                                      parent=self.window)

      if not answer == "admin":
        messagebox.showerror("Denied", "Invalid Admin Password.")
        self.titlescreen()

    label = tk.Label(self.window, text="Admin Login")
    button1 = tk.Button(self.window,
                        text="List Accounts",
                        command=lambda: self.accountList())
    button1.pack()
    button2 = tk.Button(self.window,
                        text="Wipe Account Database",
                        command=lambda: self.wipeAccounts())
    button2.pack()
    back = tk.Button(self.window,
                     text="Back",
                     command=lambda: self.titlescreen(),
                     bg='grey')
    back.pack()

  def accountList(self):

    self.clearWindow()
    label = tk.Label(self.window, text="View All Accounts")
    label.pack()
    buttons = []
    # GRAB ALL ACCT INFO, PUT INTO TABLE/LIST AND THEN GRAB THE APPLICABLE NUMBER FOR ROW BC OTHERWISE IT JUST HAS THE LAST ONE
    ulist = []
    for row in self.cur.execute("SELECT username FROM users"):
      ulist.append(row)

    for x in range(len(ulist)):
      uName = ulist[x][0]
      btn = tk.Button(self.window,
                      text=uName,
                      command=lambda x=x: self.displayaccountinfo(ulist[x]))
      btn.pack()
      buttons.append(btn)
    back = tk.Button(self.window,
                     text="Back",
                     command=lambda: self.adminLogin(True),
                     bg='grey')
    back.pack()

  def wipeAccounts(self):
    if messagebox.askyesno("S", "Are you sure you want to wipe the database?"):
      self.cur.execute("DELETE FROM users")
      self.con.commit()

    return

  def displayaccountinfo(self, uName):
    self.clearWindow()
    label = tk.Label(self.window, text="Showing info for account")
    label.pack()
    info = self.cur.execute(
      "SELECT password, balance, date FROM users WHERE username = ?",
      (uName)).fetchall()[0]
    username = tk.Label(self.window, text="Username: " + uName[0])
    pwd = tk.Label(self.window, text="Password: " + info[0])
    bal = tk.Label(self.window, text="Balance: " + str(info[1]))
    datey = tk.Label(self.window, text="Date created: " + info[2])
    username.pack()
    pwd.pack()
    bal.pack()
    datey.pack()
    delo = tk.Button(self.window,
                     text="Delete Account",
                     command=lambda: self.deleteAccount(uName))
    delo.pack()
    back = tk.Button(self.window,
                     text="Back",
                     command=lambda: self.accountList(),
                     bg='grey')
    back.pack()

  def deleteAccount(self, uName):
    if messagebox.askyesno("S", "Are you sure you want to delete this account?"):
      self.cur.execute("DELETE FROM users WHERE username = ?", (uName))
      self.con.commit()
      self.accountList()


  def __init__(self, root):
    self.window = root
    self.con = sqlite3.connect("bank.db")
    self.cur = self.con.cursor()
    self.cur.execute("CREATE TABLE IF NOT EXISTS users("
                "username, "
                "password, "
                "balance, "
                "date)")

    self.screens = {
      "Deposit": {
        "Labels": {
          1: "Depositing",
          2: "How much do you want to deposit?"
        },
        "Buttons": {
          1: {
            "text": "Deposit Funds",
            "command": self.deposit
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
            "command": self.withdraw
          }
        },
        "Entry": 1
      },
      "Balance": {
        "Labels": {
          1: "Balance Check"
        },
        "Buttons": 0,
        "Entry": 0
      }
    }





