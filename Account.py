
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

    def deposit(self, username, password, amount):
        return

    def withdrawl(self, username, password, amount):
        return

