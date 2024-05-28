import time
import pandas
import pymysql
import ttkthemes
from tkinter import *
from tkinter import ttk, messagebox, filedialog

# functionality part


def field_data(title, buttonText, command):
    global rollNoEntry, nameEntry, genderEntry, batchEntry, cgpaEntry, arrearEntry, mobileEntry, emailEntry, screen

    screen = Toplevel()
    screen.title(title)
    screen.grab_set()
    screen.resizable(False, False)

    rollNoLabel = Label(screen, text='ROLL NUMBER', font=('Trebuchet MS', 12, 'bold'))
    rollNoLabel.grid(row=0, column=0, padx=30, pady=5, sticky=W)
    rollNoEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    rollNoEntry.grid(row=0, column=1, padx=10, pady=5)

    nameLabel = Label(screen, text='NAME', font=('Trebuchet MS', 12, 'bold'))
    nameLabel.grid(row=1, column=0, padx=30, pady=5, sticky=W)
    nameEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    nameEntry.grid(row=1, column=1, padx=10, pady=5)

    genderLabel = Label(screen, text='GENDER', font=('Trebuchet MS', 12, 'bold'))
    genderLabel.grid(row=2, column=0, padx=30, pady=5, sticky=W)
    genderEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    genderEntry.grid(row=2, column=1, padx=10, pady=5)

    batchLabel = Label(screen, text='BATCH', font=('Trebuchet MS', 12, 'bold'))
    batchLabel.grid(row=3, column=0, padx=30, pady=5, sticky=W)
    batchEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    batchEntry.grid(row=3, column=1, padx=10, pady=5)

    cgpaLabel = Label(screen, text='CGPA (out of 10)', font=('Trebuchet MS', 12, 'bold'))
    cgpaLabel.grid(row=4, column=0, padx=30, pady=5, sticky=W)
    cgpaEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    cgpaEntry.grid(row=4, column=1, padx=10, pady=5)

    arrearLabel = Label(screen, text='HISTORY OF ARREAR (Y/N)', font=('Trebuchet MS', 12, 'bold'))
    arrearLabel.grid(row=5, column=0, padx=30, pady=5, sticky=W)
    arrearEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    arrearEntry.grid(row=5, column=1, padx=10, pady=5)

    mobileLabel = Label(screen, text='MOBILE NUMBER', font=('Trebuchet MS', 12, 'bold'))
    mobileLabel.grid(row=6, column=0, padx=30, pady=5, sticky=W)
    mobileEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    mobileEntry.grid(row=6, column=1, padx=10, pady=5)

    emailLabel = Label(screen, text='E-MAIL', font=('Trebuchet MS', 12, 'bold'))
    emailLabel.grid(row=7, column=0, padx=30, pady=5, sticky=W)
    emailEntry = Entry(screen, font=('Trebuchet MS', 10), width=25)
    emailEntry.grid(row=7, column=1, padx=10, pady=5)

    studentButton = ttk.Button(screen, text=buttonText, command=command)
    studentButton.grid(row=8, columnspan=2, pady=15)

    if title=='Update Student':
        indexing = studentTable.focus()
        if not indexing:
            messagebox.showerror('Error', 'Please select a student to update.', parent=screen)
            screen.destroy()
            return
        content = studentTable.item(indexing)
        listData = content['values']
        if not listData:
            messagebox.showerror('Error', 'Selected student data is empty.', parent=screen)
            screen.destroy()
            return
        rollNoEntry.insert(0, listData[0])
        nameEntry.insert(0, listData[1])
        genderEntry.insert(0, listData[2])
        batchEntry.insert(0, listData[3])
        cgpaEntry.insert(0, listData[4])
        arrearEntry.insert(0, listData[5])
        mobileEntry.insert(0, listData[6])
        emailEntry.insert(0, listData[7])


def i_exit():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = studentTable.get_children()
    newList = []
    for index in indexing:
        content=studentTable.item(index)
        dataList=content['values']
        newList.append(dataList)
    table = pandas.DataFrame(newList, columns=['ROLL NUMBER', 'NAME', 'GENDER', 'BATCH', 'CGPA', 'HISTORY OF ARREAR (Y/N)', 'MOBILE NUMBER', 'EMAIL', 'ADDED DATE', 'ADDED TIME'])
    table.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data is exported successfully.')


def update_data():
    query = 'UPDATE STUDENT set name=%s, gender=%s, batch=%s, cgpa=%s, arrearCount=%s, mobile=%s, email=%s, date=%s, time=%s WHERE rollNo=%s'
    my_cursor.execute(query, (nameEntry.get(), genderEntry.get(), batchEntry.get(), cgpaEntry.get(), arrearEntry.get(), mobileEntry.get(), emailEntry.get(), date, currentTime, rollNoEntry.get()))
    con.commit()
    messagebox.showinfo('Success', f'Roll No. {rollNoEntry.get()} is updated successfully.', parent=screen)
    screen.destroy()
    show_student()


def show_student():
    query = 'SELECT * from STUDENT'
    my_cursor.execute(query)
    fetched_data = my_cursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)


def delete_student():
    indexing = studentTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a student to delete.')
        return
    content = studentTable.item(indexing)
    content_id = content['values']
    if not content_id:
        messagebox.showerror('Error', 'Selected student data is empty.')
        return
    content_id = content_id[0]
    result = messagebox.askyesno('Confirm Deletion', f'Are you sure you want to delete the record for Roll No. {content_id}?')
    if result:
        query = 'DELETE from STUDENT where rollNo=%s'
        my_cursor.execute(query, (content_id,))
        con.commit()
        messagebox.showinfo('Deleted', f'Record of Roll No. {content_id} is deleted successfully.')
        show_student()
    else:
        messagebox.showinfo('Cancelled', 'Deletion has been cancelled.')


def search_data():
    query = 'SELECT * from STUDENT where rollNo=%s or name=%s or gender=%s or batch=%s or cgpa=%s or arrearCount=%s or mobile=%s or email=%s'
    my_cursor.execute(query, (rollNoEntry.get(), nameEntry.get(), genderEntry.get(), batchEntry.get(), cgpaEntry.get(), arrearEntry.get(), mobileEntry.get(), emailEntry.get()))
    studentTable.delete(*studentTable.get_children())
    fetched_data = my_cursor.fetchall()
    for data in fetched_data:
        studentTable.insert('', END, values=data)



def add_data():
    if rollNoEntry.get() == '' or nameEntry.get() == '' or genderEntry.get() == '' or batchEntry.get() == '' or cgpaEntry.get() == '' or arrearEntry.get() == '' or mobileEntry.get() == '' or emailEntry.get() == '':
        messagebox.showerror('Error', 'All fields are required.', parent=screen)
    else:
        try:
            query = 'INSERT into STUDENT values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            my_cursor.execute(query, (rollNoEntry.get(), nameEntry.get(), genderEntry.get(), batchEntry.get(), cgpaEntry.get(), arrearEntry.get(), mobileEntry.get(), emailEntry.get(), date, currentTime))
            con.commit()
            result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?', parent=screen)
            if result:
                rollNoEntry.delete(0, END)
                nameEntry.delete(0, END)
                genderEntry.delete(0, END)
                batchEntry.delete(0, END)
                cgpaEntry.delete(0, END)
                arrearEntry.delete(0, END)
                mobileEntry.delete(0, END)
                emailEntry.delete(0, END)
            else:
                pass
        except:
            messagebox.showerror('Error', 'Roll Number cannot be duplicated.', parent=screen)
            return

        query = 'SELECT * from STUDENT'
        my_cursor.execute(query)
        fetched_data = my_cursor.fetchall()
        studentTable.delete(*studentTable.get_children())
        for data in fetched_data:
            studentTable.insert('', END, values=data)


def clock():
    global date, currentTime
    date = time.strftime('%d/%m/%y')
    currentTime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currentTime}')
    datetimeLabel.after(1000, clock)


count = 0
text = ''


def slider():
    global text, count
    if count == len(str):
        count = 0
        text = ''
    text = text + str[count]
    sliderLabel.config(text=text)
    count += 1
    sliderLabel.after(200, slider)


def connect_database():

    def connect():
        global my_cursor, con
        try:
            con = pymysql.connect(host='localhost', user='root', password='123')
            my_cursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Invalid Details', parent=connectWindow)
            return

        try:
            query = 'CREATE database StudentManagementSystem'
            my_cursor.execute(query)
            query = 'USE StudentManagementSystem'
            my_cursor.execute(query)
            query = 'CREATE table STUDENT(rollNo varchar(7) not null primary key, name varchar(30), gender varchar(10), batch int, cgpa float not null, arrearCount varchar(1), mobile varchar(10), email varchar(30), date date, time time)'
            my_cursor.execute(query)
        except:
            query = 'USE StudentManagementSystem'
            my_cursor.execute(query)
        messagebox.showinfo('Success', 'Database connection is successful !')
        connectWindow.destroy()
        addStudentButton.config(state=NORMAL)
        deleteStudentButton.config(state=NORMAL)
        updateStudentButton.config(state=NORMAL)
        searchStudentButton.config(state=NORMAL)
        showStudentButton.config(state=NORMAL)
        exportStudentButton.config(state=NORMAL)

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('350x220+1100+500')
    connectWindow.title('Database Connection')
    connectWindow.resizable(False, False)

    hostnameLabel = Label(connectWindow, text='HOST NAME', font=('Trebuchet MS', 12, 'bold'))
    hostnameLabel.grid(row=0, column=0, padx=20)

    hostEntry = Entry(connectWindow, font=('Trebuchet MS', 12), bd=2)
    hostEntry.grid(row=0, column=1, padx=20, pady=10)

    usernameLabel = Label(connectWindow, text='USER NAME', font=('Trebuchet MS', 12, 'bold'))
    usernameLabel.grid(row=1, column=0, padx=20)

    usernameEntry = Entry(connectWindow, font=('Trebuchet MS', 12), bd=2)
    usernameEntry.grid(row=1, column=1, padx=20, pady=10)

    passwordLabel = Label(connectWindow, text='PASSWORD', font=('Trebuchet MS', 12, 'bold'))
    passwordLabel.grid(row=2, column=0, padx=20)

    passwordEntry = Entry(connectWindow, font=('Trebuchet MS', 12), bd=2)
    passwordEntry.grid(row=2, column=1, padx=20, pady=10)

    connectButton = ttk.Button(connectWindow, text='CONNECT', command=connect)
    connectButton.grid(row=3, column=1)

# GUI part


root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('arc')
root.geometry('1920x1080+0+0')
root.title('Student Database Management System')

datetimeLabel = Label(root, font=('Californian FB', 12, 'bold'))
datetimeLabel.place(x=5, y=40)
clock()

str = 'STUDENT DATABASE MANAGEMENT SYSTEM'
sliderLabel = Label(root, font=('Candara', 20, 'bold'))
sliderLabel.place(relx=0.5, y=50, anchor='center')
sliderLabel.config(text=str)
slider()

connectButton = ttk.Button(root, text='CONNECT DATABASE', command=connect_database)
connectButton.place(x=1370, y=40)

leftFrame = Frame(root)
leftFrame.place(x=50, y=100, width=300, height=680)

logo_image = PhotoImage(file='img5.png')
logo_label = Label(leftFrame, image=logo_image)
logo_label.grid(row=0, column=0)

style = ttk.Style()
style.configure('TButton', font=('Candara', 10, 'bold'), anchor='center')

addStudentButton = ttk.Button(leftFrame, text='ADD STUDENT', width=25, style='TButton', state=DISABLED, command=lambda :field_data('Add Student', 'ADD', add_data))
addStudentButton.grid(row=1, column=0, pady=20)

deleteStudentButton = ttk.Button(leftFrame, text='DELETE STUDENT', width=25, style='TButton', state=DISABLED, command=delete_student)
deleteStudentButton.grid(row=2, column=0, pady=20)

updateStudentButton = ttk.Button(leftFrame, text='UPDATE STUDENT', width=25, style='TButton', state=DISABLED, command=lambda :field_data('Update Student', 'UPDATE', update_data))
updateStudentButton.grid(row=3, column=0, pady=20)

searchStudentButton = ttk.Button(leftFrame, text='SEARCH STUDENT', width=25, style='TButton', state=DISABLED, command=lambda :field_data('Search Student', 'SEARCH', search_data))
searchStudentButton.grid(row=4, column=0, pady=20)

showStudentButton = ttk.Button(leftFrame, text='VIEW STUDENT', width=25, style='TButton', state=DISABLED, command=show_student)
showStudentButton.grid(row=5, column=0, pady=20)

exportStudentButton = ttk.Button(leftFrame, text='EXPORT DATA', width=25, style='TButton', state=DISABLED, command=export_data)
exportStudentButton.grid(row=6, column=0, pady=20)

exitButton = ttk.Button(leftFrame, text='EXIT', width=25, style='TButton', command=i_exit)
exitButton.grid(row=7, column=0, pady=20)

rightFrame = Frame(root)
rightFrame.place(x=350, y=100, width=1150, height=680)

scrollBarX = Scrollbar(rightFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(rightFrame, orient=VERTICAL)

studentTable = ttk.Treeview(rightFrame, columns=('Roll Number', 'Name', 'Gender', 'Batch', 'CGPA', 'History of Arrear (Y/N)', 'Mobile Number', 'Email', 'Added Date', 'Added Time'), xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)

studentTable.pack(fill=BOTH, expand=1)

studentTable.config(show='headings')
studentTable.heading('Roll Number', text='ROLL NUMBER')
studentTable.heading('Name', text='NAME')
studentTable.heading('Gender', text='GENDER')
studentTable.heading('Batch', text='BATCH')
studentTable.heading('CGPA', text='CGPA')
studentTable.heading('History of Arrear (Y/N)', text='HISTORY OF ARREAR (Y/N)')
studentTable.heading('Mobile Number', text='MOBILE NUMBER')
studentTable.heading('Email', text='EMAIL')
studentTable.heading('Added Date', text='ADDED DATE')
studentTable.heading('Added Time', text='ADDED TIME')

studentTable.column('Roll Number', width=100, anchor=CENTER)
studentTable.column('Name', width=130, anchor=CENTER)
studentTable.column('Gender', width=100, anchor=CENTER)
studentTable.column('Batch', width=60, anchor=CENTER)
studentTable.column('CGPA', width=60, anchor=CENTER)
studentTable.column('History of Arrear (Y/N)', width=155, anchor=CENTER)
studentTable.column('Mobile Number', width=120, anchor=CENTER)
studentTable.column('Email', width=170, anchor=CENTER)
studentTable.column('Added Date', width=90, anchor=CENTER)
studentTable.column('Added Time', width=90, anchor=CENTER)

root.mainloop()
