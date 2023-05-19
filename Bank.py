from tkinter import messagebox

class Bank:
    numAccounts = -1
    accountList = [0,0,0,0,0,0,0,0,0,0]
    marketCap = 0
    name = ""



    def __init__(self, namey):
        self.name = namey
        return


    def addAccount (self, newAccount):

        self.accountList[self.numAccounts + 1] = newAccount
        self.numAccounts += 1
        messagebox.showinfo("Created", f"Account created with Username {newAccount.uName}")
        return


