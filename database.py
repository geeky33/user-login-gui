import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# Database functions
def connect_db():
    return sqlite3.connect('students.db')

def create_table(cursor):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        major TEXT NOT NULL,
        gpa REAL
    )
    ''')

def insert_student(cursor, name, age, major, gpa):
    cursor.execute('''
    INSERT INTO students (name, age, major, gpa) VALUES (?, ?, ?, ?)
    ''', (name, age, major, gpa))

def fetch_all_students(cursor):
    cursor.execute('SELECT * FROM students')
    return cursor.fetchall()

def update_student(cursor, student_id, name, age, major, gpa):
    cursor.execute('''
    UPDATE students SET name = ?, age = ?, major = ?, gpa = ? WHERE student_id = ?
    ''', (name, age, major, gpa, student_id))

def delete_student(cursor, student_id):
    cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))

# GUI functions
def add_student():
    name = entry_name.get()
    age = entry_age.get()
    major = entry_major.get()
    gpa = entry_gpa.get()
    
    if name and age and major and gpa:
        with connect_db() as conn:
            cursor = conn.cursor()
            insert_student(cursor, name, int(age), major, float(gpa))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            clear_entries()  # Clear fields after adding
            load_students()
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

def load_students():
    for row in tree.get_children():
        tree.delete(row)
    with connect_db() as conn:
        cursor = conn.cursor()
        students = fetch_all_students(cursor)
        for student in students:
            tree.insert("", "end", values=student)

def delete_student_gui():
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item)["values"][0]
        with connect_db() as conn:
            cursor = conn.cursor()
            delete_student(cursor, student_id)
            conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            clear_entries()  # Clear fields after deletion
            load_students()
    else:
        messagebox.showwarning("Selection Error", "Please select a student to delete.")

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_major.delete(0, tk.END)
    entry_gpa.delete(0, tk.END)

def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        student_data = tree.item(selected_item)["values"]
        entry_name.delete(0, tk.END)
        entry_name.insert(0, student_data[1])
        entry_age.delete(0, tk.END)
        entry_age.insert(0, student_data[2])
        entry_major.delete(0, tk.END)
        entry_major.insert(0, student_data[3])
        entry_gpa.delete(0, tk.END)
        entry_gpa.insert(0, student_data[4])

def show_edit_menu(event):
    selected_item = tree.selection()
    if selected_item:
        context_menu.post(event.x_root, event.y_root)

def edit_student_from_menu():
    selected_item = tree.selection()
    if selected_item:
        student_id = tree.item(selected_item)["values"][0]
        student_data = tree.item(selected_item)["values"]
        open_edit_dialog(student_id, student_data)

def open_edit_dialog(student_id, student_data):
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Student")
    
    tk.Label(edit_window, text="Name").grid(row=0, column=0)
    entry_name_edit = tk.Entry(edit_window)
    entry_name_edit.grid(row=0, column=1)
    entry_name_edit.insert(0, student_data[1])

    tk.Label(edit_window, text="Age").grid(row=1, column=0)
    entry_age_edit = tk.Entry(edit_window)
    entry_age_edit.grid(row=1, column=1)
    entry_age_edit.insert(0, student_data[2])

    tk.Label(edit_window, text="Major").grid(row=2, column=0)
    entry_major_edit = tk.Entry(edit_window)
    entry_major_edit.grid(row=2, column=1)
    entry_major_edit.insert(0, student_data[3])

    tk.Label(edit_window, text="GPA").grid(row=3, column=0)
    entry_gpa_edit = tk.Entry(edit_window)
    entry_gpa_edit.grid(row=3, column=1)
    entry_gpa_edit.insert(0, student_data[4])

    def save_changes():
        name = entry_name_edit.get()
        age = entry_age_edit.get()
        major = entry_major_edit.get()
        gpa = entry_gpa_edit.get()
        
        if name and age and major and gpa:
            with connect_db() as conn:
                cursor = conn.cursor()
                update_student(cursor, student_id, name, int(age), major, float(gpa))
                conn.commit()
                messagebox.showinfo("Success", "Student updated successfully!")
                load_students()
                edit_window.destroy()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    tk.Button(edit_window, text="Save", command=save_changes).grid(row=4, columnspan=2, pady=10)

# Initialize the database
with connect_db() as conn:
    create_table(conn.cursor())

# Set up the main window
root = tk.Tk()
root.title("Student Management System")

# Entry fields
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name").grid(row=0, column=0)
entry_name = tk.Entry(frame)
entry_name.grid(row=0, column=1)

tk.Label(frame, text="Age").grid(row=1, column=0)
entry_age = tk.Entry(frame)
entry_age.grid(row=1, column=1)

tk.Label(frame, text="Major").grid(row=2, column=0)
entry_major = tk.Entry(frame)
entry_major.grid(row=2, column=1)

tk.Label(frame, text="GPA").grid(row=3, column=0)
entry_gpa = tk.Entry(frame)
entry_gpa.grid(row=3, column=1)

# Buttons with blue theme
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

blue_bg = "#007BFF"  # Blue background color
white_fg = "white"    # White foreground color

tk.Button(btn_frame, text="Add Student", command=add_student, bg=blue_bg, fg=white_fg).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Delete Student", command=delete_student_gui, bg=blue_bg, fg=white_fg).grid(row=0, column=1, padx=5)

# Treeview for displaying students
tree = ttk.Treeview(root, columns=("ID", "Name", "Age", "Major", "GPA"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Major", text="Major")
tree.heading("GPA", text="GPA")
tree.pack(pady=10)

# Load initial student data
load_students()

# Bind selection event
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Context menu for right-click
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Edit Student", command=edit_student_from_menu)

# Bind right-click event
tree.bind("<Button-3>", show_edit_menu)

root.mainloop()
