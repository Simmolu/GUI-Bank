from tkinter import messagebox
class Account:
    accountNum = 0
    uName = ""
    pWord = ""

    def __init__(self, username, password, num, time):
        self.uName = username
        self.pWord = password
        self.accountNum = num
        self.timeCreated = time
        self.balance = 0
        return

    def deposit(self, amount):
        self.balance += amount
        messagebox.showinfo("$", "$" + str(amount) + " successfully deposited.")
        return True

    def withdraw(self, amount):
        if amount > self.balance:
            messagebox.showerror("$", "Not enough funds. Please try again later.")
            return
        else:
            self.balance -= amount
            messagebox.showinfo("$", "$" + str(amount) + " successfully withdrawn.")
            return

