#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import re

root = Tk()
root.title("Python:  Simple Registration login form")

width = 640
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(10, 10)

# =======================================VARIABLES=====================================
EMAIL_ID = StringVar()
FUSERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()


# =======================================METHODS=======================================
def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, EMAIL_ID TEXT, password TEXT, firstname TEXT, lastname TEXT)")


def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    lbl_username = Label(LoginFrame, text="Email:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=EMAIL_ID, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_fpwd = Label(LoginFrame, text="Forget password?", fg="Blue", font=('arial', 18), width=35)
    lbl_fpwd.grid(row=5, columnspan=2)

    lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)
    lbl_fpwd.bind('<Button-1>', ToggleTofpwd)


def FpwdForm():
    global fpwdFrame, fpwd_result1, fpwd_result2
    fpwdFrame = Frame(root)
    fpwdFrame.pack(side=TOP, pady=80)
    fpwd_username = Label(fpwdFrame, text="Enter your Email:", font=('arial', 25), bd=18)
    fpwd_username.grid(row=1)
    fusername = Entry(fpwdFrame, font=('arial', 20), textvariable=FUSERNAME, width=15)
    fusername.grid(row=2)

    fpwd_result1 = Label(fpwdFrame, text="", font=('arial', 18))
    fpwd_result1.grid(row=3, columnspan=2)
    fpwd_result2 = Label(fpwdFrame, text="", font=('arial', 18))
    fpwd_result2.grid(row=4, columnspan=2)
    btn_fwd = Button(fpwdFrame, text="Get Password", font=('arial', 18), width=20, command=FPWD)
    btn_fwd.grid(row=5, pady=20)
    fwd_back = Label(fpwdFrame, text="Back", fg="Blue", font=('arial', 12))
    fwd_back.grid(row=0, sticky=W)
    fwd_back.bind('<Button-1>', Togglefromfpwdtologin)


def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)
    lbl_emailid = Label(RegisterFrame, text="Email:", font=('arial', 18), bd=18)
    lbl_emailid.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 18), bd=18)
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 18), bd=18)
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=EMAIL_ID, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=15)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)


def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()


def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()


def ToggleTofpwd(event=None):
    LoginFrame.destroy()
    FpwdForm()


def Togglefromfpwdtologin(event=None):
    fpwdFrame.destroy()
    LoginForm()


def Register():
    Database()
    USERNAME2 = (EMAIL_ID.get())
    validate_email = check(USERNAME2)
    PASSWORD2 = (PASSWORD.get())
    validate_pwd = password_check(PASSWORD2)

    if validate_email == 'Valid Email':
        if validate_pwd == '1':
            if EMAIL_ID.get == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
                lbl_result2.config(text="Please complete the required field!", fg="orange")
            else:
                cursor.execute("SELECT * FROM `member` WHERE `EMAIL_ID` = ?", (EMAIL_ID.get(),))
                if cursor.fetchone() is not None:
                    lbl_result2.config(text="Email ID already exist", fg="red")
                else:
                    cursor.execute("INSERT INTO `member` (EMAIL_ID, password, firstname, lastname) VALUES(?, ?, ?, ?)",
                                   (
                                       str(EMAIL_ID.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get())))
                    conn.commit()
                    EMAIL_ID.set("")
                    PASSWORD.set("")
                    FIRSTNAME.set("")
                    LASTNAME.set("")
                    lbl_result2.config(text="Successfully Created!", fg="black")
                cursor.close()
                conn.close()
        else:
            lbl_result2.config(text=validate_pwd, fg="orange")
    else:
        lbl_result2.config(text="Invalid Email ID!", fg="orange")


def Login():
    Database()
    USERNAME2 = (EMAIL_ID.get())
    validate_email = check(USERNAME2)
    if validate_email == 'Valid Email':
        if EMAIL_ID.get == "" or PASSWORD.get() == "":
            lbl_result1.config(text="Please complete the required field!", fg="orange")
        else:
            cursor.execute("SELECT * FROM `member` WHERE `EMAIL_ID` = ? and `password` = ?",
                           (EMAIL_ID.get(), PASSWORD.get()))
            if cursor.fetchone() is not None:
                lbl_result1.config(text="You Successfully Login", fg="blue")
            else:
                lbl_result1.config(text="Invalid Email ID or password", fg="red")
    else:
        lbl_result1.config(text="Invalid Email ID!", fg="orange")


def FPWD():
    Database()
    FUSERNAME2 = (FUSERNAME.get())
    validate_email = check(FUSERNAME2)
    if validate_email == 'Valid Email':

        if FUSERNAME.get == '':
            fpwd_result1.config(text="Please Enter username!", fg="orange")
        else:
            cursor.execute("SELECT password FROM `member` WHERE `EMAIL_ID` =?", (FUSERNAME.get(),))
            record = cursor.fetchone()

            if record is not None:
                fpwd_result1.config(text="Your Password is ", fg="blue")
                fpwd_result2.config(text=record, fg="green")
            else:
                fpwd_result1.config(text="Username is not exist", fg="red")
    else:
        fpwd_result1.config(text="Invalid Email ID!", fg="orange")


LoginForm()

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


def check(email):
    if (re.fullmatch(regex, email)):
        return ("Valid Email")
    else:
        return ("Invalid Email")


def password_check(passwd):
    SpecialSym = ['$', '@', '#', '%']
    val = '1'

    if len(passwd) < 5:
        return ('Password length should be at least 6')
        val = False

    if len(passwd) > 16:
        return ('Password length should be not be greater than 15')
        val = False

    if not any(char.isdigit() for char in passwd):
        return ('Password should have at least one digit')
        val = False

    if not any(char.isupper() for char in passwd):
        return ('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        return ('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        return ('Password should have at least one special character')
        val = False
    if val:
        return val


# ========================================INITIALIZATION===================================
if __name__ == '__main__':
    root.mainloop()


# In[ ]:





# In[ ]:




