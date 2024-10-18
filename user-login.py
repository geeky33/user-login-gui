#add dob or some differentiating part for register page
import sqlite3
import re
from tkinter import *
from tkinter import messagebox

# Connect to SQLite database (create one if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a table for users if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')
conn.commit()

# Function to clear the current window  
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# Function to validate the username and password
def validate_registration(username, password):
    # Check if there are spaces
    if ' ' in username or ' ' in password:
        return "Username and password cannot contain spaces."

    # Check for at least one uppercase letter in the username
    if not any(char.isupper() for char in username):
        return "Username must contain at least one uppercase letter."

    # Check for password length
    if len(password) < 6:
        return "Password must be at least 6 characters long."

    # Check for at least one special character in the password
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."

    return None

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Query the database to find the user
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Login Success", "Welcome, " + username)
    else:
        messagebox.showwarning("Login Failed", "User does not exist, please register.")
        show_register_form()

# Function to handle registration
def register():
    username = reg_username_entry.get()
    password = reg_password_entry.get()

    # Validate the username and password
    validation_error = validate_registration(username, password)
    if validation_error:
        messagebox.showerror("Registration Error", validation_error)
        return

    # Check if username already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        messagebox.showwarning("Registration Failed", "Username already exists!")
    else:
        # Insert new user into the database
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Registration Success", "You have registered successfully!")
        show_login_form()

# Function to show the login form
def show_login_form():
    clear_window()

    frame = Frame(root, bg='#f0f0f0')
    frame.place(relwidth=1, relheight=1)

    Label(frame, text="Login", font=("Helvetica", 20), bg='#f0f0f0').pack(pady=20)

    Label(frame, text="Username:", font=("Helvetica", 12), bg='#f0f0f0').pack(pady=5)
    global username_entry
    username_entry = Entry(frame, font=("Helvetica", 12), bd=2)
    username_entry.pack(pady=5, padx=20, ipadx=20)

    Label(frame, text="Password:", font=("Helvetica", 12), bg='#f0f0f0').pack(pady=5)
    global password_entry
    password_entry = Entry(frame, font=("Helvetica", 12), show="*", bd=2)
    password_entry.pack(pady=5, padx=20, ipadx=20)

    Button(frame, text="Login", command=login, font=("Helvetica", 12), bg="#007bff", fg="white", bd=0, padx=10, pady=5).pack(pady=20)
    Button(frame, text="Register", command=show_register_form, font=("Helvetica", 12), bg="#28a745", fg="white", bd=0, padx=10, pady=5).pack()

# Function to show the registration form
def show_register_form():
    clear_window()

    frame = Frame(root, bg='#f0f0f0')
    frame.place(relwidth=1, relheight=1)

    Label(frame, text="Register", font=("Helvetica", 20), bg='#f0f0f0').pack(pady=20)

    Label(frame, text="Username:", font=("Helvetica", 12), bg='#f0f0f0').pack(pady=5)
    global reg_username_entry
    reg_username_entry = Entry(frame, font=("Helvetica", 12), bd=2)
    reg_username_entry.pack(pady=5, padx=20, ipadx=20)

    Label(frame, text="Password:", font=("Helvetica", 12), bg='#f0f0f0').pack(pady=5)
    global reg_password_entry
    reg_password_entry = Entry(frame, font=("Helvetica", 12), show="*", bd=2)
    reg_password_entry.pack(pady=5, padx=20, ipadx=20)

    Button(frame, text="Register", command=register, font=("Helvetica", 12), bg="#28a745", fg="white", bd=0, padx=10, pady=5).pack(pady=20)
    Button(frame, text="Back to Login", command=show_login_form, font=("Helvetica", 12), bg="#007bff", fg="white", bd=0, padx=10, pady=5).pack()

# Main window
root = Tk()
root.title("User Login System")

# Set window size and center it
root.geometry("500x400")

# Show login form on startup
show_login_form()

root.mainloop()

# Close the connection when done
conn.close()
