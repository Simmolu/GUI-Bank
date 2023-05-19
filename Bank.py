from tkinter import messagebox
from Account import Account

class Bank:
    numAccounts = -1
    accountList = []
    marketCap = 0
    name = ""

    def __init__(self, namey):
        self.name = namey
        return

    def addAccount (self, newAccount):

        self.accountList.append(newAccount)
        self.numAccounts += 1
        messagebox.showinfo("Created", f"Account created with Username {newAccount.uName}")
        return

