### Importing necessary libraries and modules
from tkinter import *
from datetime import date
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from tkinter.ttk import Combobox
import sqlite3
import random
import string
import getpass
import smtplib
from tkcalendar import Calendar
import re


background = "#06283D"
framebg = "#F0F0F0"
framefg = "#06283D"

# Create database connection
conn = sqlite3.connect('student.db')
c = conn.cursor()

# Create table if it doesn't exist

c.execute('''CREATE TABLE IF NOT EXISTS students (
             registration_no INTEGER PRIMARY KEY,
             name TEXT,
             class TEXT,
             gender TEXT,
             dob TEXT,
             date_of_registration TEXT,
             religion TEXT,
             email_id TEXT,
             father_name TEXT,
             mother_name TEXT,
             father_occupation TEXT,
             mother_occupation TEXT,
             username TEXT,
             password TEXT
             )''')
conn.commit()

root = Tk()
root.title("Student Detail Management System")
root.geometry("1250x700+210+100")
root.config(bg=background)

# Initialize variables
filename = None
img = None

# Exit function
def Exit():
    conn.close()
    root.destroy()

# Show Image function
def showimage():
    global filename, img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(), #Sets the initial directory for the file dialog to the current working directory.
                                           title="Select Image file",
                                           filetype=(("JPG File", "*.jpg"),
                                                     ("PNG File", "*.png"),
                                                     ("All files", "*.txt")))
    try:
        img = Image.open(filename)
        resized_image = img.resize((190, 190))
        photo2 = ImageTk.PhotoImage(resized_image)
        lbl.config(image=photo2)
        lbl.image = photo2
    except Exception as e:
        messagebox.showerror("Error", f"Failed to open image: {e}")


# Registration Number function
def registration_no():
    c.execute("SELECT MAX(registration_no) FROM students")
    max_row_value = c.fetchone()[0]
    if max_row_value:
        Registration.set(max_row_value + 1)
    else:
        Registration.set(1)

def generate_username_and_password(name, dob):
    first_name = name.split()[0].lower()

    # Check if the DOB is in the expected format (day/month/year)
    dob_parts = dob.split('/')
    if len(dob_parts) >= 2:
        formatted_dob = dob_parts[0] + dob_parts[1]
    else:
        # Handle the case where the DOB is not in the expected format
        formatted_dob = '0000'

    username = first_name + formatted_dob

    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    # random characters and date of birth for password
    password = random_chars + formatted_dob
    return username, password

# Clear function
def clear():
    global img
    Name.set('')
    DOB.set('')
    Religion.set('')
    Email_id.set('')
    F_Name.set('')
    M_Name.set('')
    Father_Occupation.set('')
    Mother_Occupation.set('')
    Class.set("Select Class")
    registration_no()
    saveButton.config(state='normal')
    img1 = PhotoImage(file="C:/Users/abin/OneDrive/Desktop/REimages/upload photo.png")
    lbl.config(image=img1)
    lbl.image = img1
    img = ""

# Save function
def Save():
    R1 = Registration.get()
    N1 = Name.get()
    C1 = Class.get()
    G1 = gender.get()
    D2 = DOB.get()
    D1 = Date.get()
    Re1 = Religion.get()
    E1 = Email_id.get()
    fathername = F_Name.get()
    mothername = M_Name.get()
    F1 = Father_Occupation.get()
    M1 = Mother_Occupation.get()
    U1, P1 = generate_username_and_password(N1, D2)

    try:
        if not img:  
            messagebox.showinfo("Error", "Profile picture not selected. Please select a profile picture.")
            return
    
        if N1 == "" or C1 == "Select Class" or D2 == "" or Re1 == "" or E1 == "" or fathername == "" or mothername == "" or F1 == "" or M1 == "":
            messagebox.showinfo("error", "Few Data is missing!")

            return

        # Check if input contains only alphabets and spaces
        if not is_valid_text_input(N1):
            handle_invalid_input("Full Name")
            return

        if not is_valid_text_input(fathername):
            handle_invalid_input("Father's Name")
            return

        if not is_valid_text_input(mothername):
            handle_invalid_input("Mother's Name")
            return

        if not is_valid_text_input(F1):
            handle_invalid_input("Father's Occupation")
            return

        if not is_valid_text_input(M1):
            handle_invalid_input("Mother's Occupation")
            return
    
        # Save Image using the Image class
        img.save("images/" + str(R1) + ".jpg")
        c.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
          (R1, N1, C1, gender.get(), D2, D1, Re1, E1, fathername, mothername, F1, M1, U1, P1))        
        conn.commit()
        
        # Send email with username and password
        send_email(U1, P1, E1)

        messagebox.showinfo("info", "Please check your Email for the Username and Password to Login")
        clear()

        messagebox.showinfo("Success", "Student details saved successfully. Click on Next button to enter the username and password.")
        clear()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

# Function to display a message box with a custom error message
def show_error_message(title, message):
    messagebox.showerror(title, message)

# Function to check if the input contains only alphabets and spaces
def is_valid_text_input(text):
    return all(char.isalpha() or char.isspace() for char in text)

# Function to handle invalid input and display a message box
def handle_invalid_input(field_name):
    show_error_message("Invalid Input", f"Invalid characters in {field_name}. Please use only alphabets .")

#smtp            
def send_email(username, password, recipient_email):
    sender_email = 'abinpillai23@gmail.com'  # Update email address
    sender_password = 'tyqo afai msgo eeke' # Update with your email password
    subject = "Student Detail Management System"
    message = f"Subject: {subject}\n\n"
    message += f"Dear Student,\n\nYour username: {username}\nYour password: {password}\n\nThank you!\n\nBest Regards,\nStudent Detail Management System"
    
    try:
        # Set up the SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            # Send the email
            server.sendmail(sender_email, recipient_email, message)
            
        messagebox.showinfo("Email Sent", "Email with registration information has been sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

def search():
    text = Search.get()
    filter_option = FilterOption.get()

    try:
        # Build the query based on the selected filter option
        if filter_option == "Name":
            c.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + text + '%',))
        elif filter_option == "Date of Birth":
            c.execute("SELECT * FROM students WHERE dob=?", (text,))
        elif filter_option == "Registration Number":
            c.execute("SELECT * FROM students WHERE registration_no=?", (text,))
        else:
            messagebox.showerror("Invalid Filter Option", "Please select a valid filter option (Name, Date of Birth, or Registration Number)!!!")
            return

        row = c.fetchone()
        if row:
            # Populate the form with the retrieved student information
            Registration.set(row[0])
            Name.set(row[1])
            Class.set(row[2])
            gender.set(row[3])
            DOB.set(row[4])
            Date.set(row[5])
            Religion.set(row[6])
            Email_id.set(row[7])
            F_Name.set(row[8])
            M_Name.set(row[9])
            Father_Occupation.set(row[10])
            Mother_Occupation.set(row[11])

            # Display the student image
            img = Image.open("images/" + str(row[0]) + ".jpg")
            resized_image = img.resize((190, 190))
            photo2 = ImageTk.PhotoImage(resized_image)
            lbl.config(image=photo2)
            lbl.image = photo2
        else:
            # Display an error message if no matching student is found
            messagebox.showerror("Invalid", f"No student found with the provided {filter_option.lower()}!!!")
    except Exception as e:
        # Display an error message for any unexpected errors
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        # Clear the search field
        search_entry.delete(0, END)

# Update function

def Update():
    R1 = Registration.get()
    N1 = Name.get()
    C1 = Class.get()
    G1 = gender.get()
    D2 = DOB.get()
    D1 = Date.get()
    Re1 = Religion.get()
    E1 = Email_id.get()
    fathername = F_Name.get()
    mothername = M_Name.get()
    F1 = Father_Occupation.get()
    M1 = Mother_Occupation.get()

    try:
        if img:  # Check if there's an image
            img.save("Student Images/" + str(R1) + ".jpg")  # Save the image using the Image class
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save image: {e}")

    c.execute('''UPDATE students SET name=?, class=?, gender=?, dob=?, date_of_registration=?, religion=?, 
                 email_id=?, father_name=?, mother_name=?, father_occupation=?, mother_occupation=? WHERE registration_no=?''',
              (N1, C1, G1, D2, D1, Re1, E1, fathername, mothername, F1, M1, R1))
    conn.commit()

    messagebox.showinfo("Update", "Update Successfully!!!!!")
    clear()

#gender
def selection():
    global gender
    value=radio.get()
    if value==1:
        gender="Male"
        print(gender)
    else:
        gender="Female"
        print(gender)

# Top frames
Label(root, text="For any Query : pillaiabincs232414@gmail.com", width=10, height=3, bg="#f0687c",anchor='e').pack(side=TOP, fill=X)
Label(root, text="STUDENT DETAIL MANAGEMENT SYSTEM", width=10, height=2, bg="#c36464", fg='#fff', font='arial 20 bold').pack(side=TOP, fill=X)

# Search box to update
Search = StringVar()
search_entry = Entry(root, textvariable=Search, width=15, bd=2, font="arial 20")
search_entry.place(x=1050, y=70)

# Add a filter option list
FilterOption = StringVar()
filter_option_combobox = Combobox(root, values=["Name", "Date of Birth", "Registration Number"],width=30, height=20, textvariable=FilterOption, font="Roboto 10",  state="r")
filter_option_combobox.place(x=1050, y=50)
FilterOption.set("Search information")  # Set the default filter option

# Add a search button to trigger the search function
imageicon3 = PhotoImage(file="C:/Users/abin/OneDrive/Desktop/REimages/search.png")
Srch = Button(root, image=imageicon3, compound=LEFT, width=123, bg='#68ddfa', font="arial 13 bold", command=search)
Srch.place(x=1350, y=70)


imageicon4=PhotoImage(file="C:/Users/abin/OneDrive/Desktop/REimages/Layer 4.png")
Update_button = Button(root, image=imageicon4, bg="#c36464", command=Update)
Update_button.place(x=110, y=64)

# Registration and date
Label(root, text="Registration No:", font="arial 13", fg="white", bg=background).place(x=30, y=150)
Label(root, text="Date:", font="arial 13", fg="white", bg=background).place(x=500, y=150)

Registration = IntVar()
Date = StringVar()

reg_entry = Entry(root, textvariable=Registration, width=15, font="arial 10",state='readonly')
reg_entry.place(x=160, y=150)

registration_no()

today = date.today()
d1 = today.strftime("%d/%m/%Y")
date_entry = Entry(root, textvariable=Date, width=15, font="arial 10",state='readonly')
date_entry.place(x=550, y=150)

Date.set(d1)

# Student details
obj = LabelFrame(root, text="Student's Details", font=20, bd=2, width=1100, fg=framefg, bg=framebg, height=250, relief=GROOVE)
obj.place(x=30, y=200)

Label(obj, text="Full Name:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj, text="Date of Birth:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=100)
Label(obj, text="Gender:", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=150)

Label(obj, text="Class:", font="arial 13", bg=framebg, fg=framefg).place(x=600, y=50)
Label(obj, text="Religion :", font="arial 13", bg=framebg, fg=framefg).place(x=600, y=100)

Name = StringVar()
name_entry = Entry(obj, textvariable=Name, width=20, font="arial 10")
name_entry.place(x=160, y=50)

DOB = StringVar()

def get_selected_date():
    cal = Calendar(root, selectmode='day', year=2005, month=5, day=22,
                   mindate=date(1999, 1, 1), maxdate=date(2007, 1, 1), yearspan=(17, 25),
                   width=10, height=6)
    cal.place(x=160, y=100)
    
    dob_entry = Entry(obj, textvariable=DOB, width=20, font="arial 10")
    dob_entry.place(x=160, y=100)

    cal.place(x=160, y=50)
    
    def update_dob():
        selected_date = cal.get_date()
        DOB.set(selected_date)
        dob_entry.delete(0, END)
        dob_entry.insert(0, selected_date)
        cal.destroy()
    
    Button(root, text="Confirm Date", command=update_dob).place(x=400, y=325)

# Button to get selected date
Button(obj, text="Select Date", command=get_selected_date).place(x=160, y=100)

gender = StringVar(value="Male")

R1 = Radiobutton(obj, text="Male", variable=gender, value="Male", bg=framebg, fg=framefg)
R1.place(x=150, y=150)

R2 = Radiobutton(obj, text="Female", variable=gender, value="Female", bg=framebg, fg=framefg)
R2.place(x=200, y=150)

gender.set("Male")

##Religion
Religion = StringVar()
religion_options = ['Hindu', 'Muslim', 'Christian', 'Sikh', 'Other']
Religion.set(religion_options[0])
Religion.set("Select Religion")

religion_combobox = Combobox(obj, values=religion_options, textvariable=Religion, font="Roboto 10", width=17, state="r")
religion_combobox.place(x=670, y=100)

##Email-id
Email_id = StringVar()
Email_id_options = ['']
Email_id.set(Email_id_options[0])
Label(obj, text="Email-id: ", font="arial 13", bg=framebg, fg=framefg).place(x=600, y=150)
Email_id_entry = Entry(obj, textvariable=Email_id, width=20, font="arial 10")
Email_id_entry.place(x=670, y=150)

##class
Class = Combobox(obj, values=['Fycs','Sycs','Tycs'], font="Roboto 10",width=17, state="r")
Class.place(x=670, y=50)
Class.set("Select Class")

# Parents details
obj2 = LabelFrame(root, text="Parent's Details", font=20, bd=2, width=1100, fg="black", bg=framebg, height=220,relief=GROOVE)
obj2.place(x=30, y=500)

Label(obj2, text="Father's Name: ", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=50)
Label(obj2, text="Occupation : ", font="arial 13", bg=framebg, fg=framefg).place(x=30, y=100)

##Father name
F_Name = StringVar()
f_entry = Entry(obj2, textvariable=F_Name, width=20, font="arial 10")
f_entry.place(x=160, y=50)

##Father ocuupation
Father_Occupation = StringVar()
FO_entry = Entry(obj2, textvariable=Father_Occupation, width=20, font="arial 10")
FO_entry.place(x=160, y=100)

Label(obj2, text="Mother's Name: ", font="arial 13", bg=framebg, fg=framefg).place(x=600, y=50)
Label(obj2, text="Occupation : ", font="arial 13", bg=framebg, fg=framefg).place(x=600, y=100)

##mother name
M_Name = StringVar()
M_entry = Entry(obj2, textvariable=M_Name, width=20, font="arial 10")
M_entry.place(x=730, y=50)

##mother occupation
Mother_Occupation = StringVar()
MO_entry = Entry(obj2, textvariable=Mother_Occupation, width=20, font="arial 10")
MO_entry.place(x=730, y=100)

# Image
f = Frame(root, bd=3, bg="black", width=200, height=200, relief=GROOVE)
f.place(x=1200, y=200)

img = PhotoImage(file="C:/Users/abin/OneDrive/Desktop/REimages/upload photo.png")
lbl = Label(f, bg="black", image=img)
lbl.place(x=0, y=0)

# Buttons
Button(root, text="Upload", width=19, height=2, font="arial 12 bold", bg="lightblue", command=showimage).place(x=1200,y=400)

saveButton = Button(root, text="Save", width=19, height=2, font="arial 12 bold", bg="lightgreen", command=Save)
saveButton.place(x=500, y=725)

Button(root, text="RESET", width=19, height=2, font="arial 12 bold", bg="lightpink", command=clear).place(x=1200,y=545)

Button(root, text="Exit", width=19, height=2, font="arial 12 bold", bg="red", command=Exit).place(x=1200, y=620)

from tkinter import Toplevel, Entry, Label, Button


login_window = None  # Declare login_window as a global variable
def open_login_window():
    global login_window 
    login_window = Toplevel(root)
    login_window.title("Login")
    login_window.geometry("400x200")
    login_window.config(bg=background)  # Set background color

    # Add login components to the new window
    Label(login_window, text="Username:", font="arial 13", bg=background, fg="white").pack(pady=10)
    username_entry_login = Entry(login_window, font="arial 13")
    username_entry_login.pack(pady=5)

    Label(login_window, text="Password:", font="arial 13", bg=background, fg="white").pack(pady=10)
    password_entry_login = Entry(login_window, show="*", font="arial 13")
    password_entry_login.pack(pady=5)

    login_button = Button(login_window, text="Login", font="arial 12 bold", bg="lightblue", command=lambda: login_user(username_entry_login.get(), password_entry_login.get()))
    login_button.pack(pady=10)

def login_user(username, password):
    global login_window
    c.execute("SELECT * FROM students WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    if row:
        messagebox.showinfo("Login Successful", "Welcome! You have successfully logged in.")
        login_window.destroy()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password. Please try again.")

# Add the Next button
next_button = Button(root, text="Next", width=19, height=2, font="arial 12 bold", bg="lightblue", command=open_login_window)
next_button.place(x=1200, y=470)

# Modify open_welcome_window function
def open_welcome_window():
    welcome_window = Toplevel(root)
    welcome_window.title("Welcome")
    welcome_window.geometry("400x200")
    welcome_window.config(bg=background)  # Set background color

    # Add welcome components to the new window
    Label(welcome_window, text="Welcome! You have successfully logged in.", font="arial 13", bg=background, fg="white").pack(pady=50)
    Button(welcome_window, text="Give Feedback", width=15, font="arial 12 bold", bg="lightblue").pack(pady=10)

root.mainloop()
