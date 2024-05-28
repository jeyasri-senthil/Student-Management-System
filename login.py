from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty.')
    elif usernameEntry.get() == 'SRI' and passwordEntry.get() == '123':
        messagebox.showinfo('Success', 'WELCOME SRI !')
        window.destroy()
        import main
    else:
        messagebox.showerror('Error', 'Please enter correct credentials.')

window = Tk()
window.geometry('1920x1080+0+0')
window.title('LOGIN')
window.configure(bg='white')

loginFrame = Frame(window, bg='white')
loginFrame.place(relx=0.5, rely=0.5, anchor=CENTER)

logoImage = PhotoImage(file='img2.png')
logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2, pady=10, padx=20)

usernameImage = PhotoImage(file='img3.png')
usernameLabel = Label(loginFrame, image=usernameImage, text=' USERNAME  ', compound=LEFT,
                      font=('Trebuchet MS', 12, 'bold'), bg='white')
usernameLabel.grid(row=1, column=0)

usernameEntry = Entry(loginFrame, font=('Trebuchet MS', 12), bd=2)
usernameEntry.grid(row=1, column=1, pady=10, padx=20)

passwordImage = PhotoImage(file='img4.png')
passwordLabel = Label(loginFrame, image=passwordImage, text=' PASSWORD  ', compound=LEFT,
                      font=('Trebuchet MS', 12, 'bold'), bg='white')
passwordLabel.grid(row=2, column=0)

passwordEntry = Entry(loginFrame, font=('Trebuchet MS', 12), bd=2)
passwordEntry.grid(row=2, column=1, pady=10, padx=20)

loginButton = Button(loginFrame, text='LOGIN', width=15, fg='black', bg='DarkSeaGreen1',
                     activeforeground='black', activebackground='DarkSeaGreen1', cursor='hand2', command=login)
loginButton.grid(row=3, column=1, pady=10)

window.mainloop()
