from Bank import Bank
import tkinter as tk


def main():
    root = tk.Tk()
    myBank = Bank(root)
    print("database opened")
    myBank.titlescreen()
    root.mainloop()
    myBank.con.commit()
    myBank.con.close()
    print("database closed")

if __name__ == "__main__":
    main()


