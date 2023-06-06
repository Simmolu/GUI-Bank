# GUI-Bank
GUI Based Bank Management App

I wanted to try another bank simulator but this time as a GUI based app, not a command line app like I did in C.

I wrote a dynamic banking application simulator using Python with a Tkinter GUI. The project models functionalities seen in real-world banking software, offering a hands-on approach to understanding core principles in software design and database management.
Key Highlights:

**User Interface Design**: Built a user-friendly GUI with Tkinter that guides users through options such as account creation, user login, balance check, deposit, and withdrawal.

**Database Integration**: Utilized SQLite3 to maintain a local database that securely stored user information, including usernames, passwords, account balances, and account creation dates. Implemented CRUD operations for account management.

**Security and Authentication**: Incorporated a secure login system which allows a user to access their account details, and an admin system to oversee all accounts and manipulate the database.

**Account Operations**: Facilitated basic banking operations such as deposits and withdrawals, updating the balance in real-time and reflecting these changes in the database.

**Administrative Functions**: Enabled special privileges for an administrator to view all accounts, delete specific accounts, and even wipe the entire database, showcasing the multi-level user role capabilities of the application.

**Error Handling & Validation**: Implemented error handling and validation checks, ensuring correct user input and displaying appropriate feedback messages for situations like invalid login attempts or insufficient account balance.
