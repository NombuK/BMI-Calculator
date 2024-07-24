from tkinter import *
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime

def open_main_window():
    main_window = Tk()
    main_window.title('Body Mass Index Calculator')
    main_window.iconbitmap('Images/crown_icon.ico')
    main_window.geometry('400x400')

    original_bg_img = Image.open('Images/fruit-basket.jpg')
    resized_bg_img = original_bg_img.resize((400, 400), Image.Resampling.LANCZOS)
    bg_img = ImageTk.PhotoImage(resized_bg_img)
    bg_label = Label(main_window, image=bg_img)
    bg_label.place(relwidth=1, relheight=1)

    conn = sqlite3.connect('bmi_data.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 weight REAL,
                 height REAL,
                 bmi REAL,
                 date TEXT)''')
    conn.commit()

    def calculate_bmi(weight, height):
        return weight / (height / 100) ** 2

    def classify_bmi(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    def save_bmi(name, weight, height, bmi):
        c.execute("INSERT INTO bmi_records (name, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                  (name, weight, height, bmi, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()

    def calculate():
        try:
            weight = float(weight_entry.get())
            height = float(height_entry.get())

            if not name_entry.get():
                messagebox.showwarning("Input Error", "Please enter a name.")
                return

            bmi = calculate_bmi(weight, height)
            category = classify_bmi(bmi)

            result_label.config(text=f"BMI: {bmi:.2f} ({category})")

        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numbers for weight and height.")

    def save():
        name = name_entry.get()
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        bmi = calculate_bmi(weight, height)
        save_bmi(name, weight, height, bmi)
        result_label.config(text="BMI: ")
        name_entry.delete(0, END)
        weight_entry.delete(0, END)
        height_entry.delete(0, END)
        messagebox.showinfo("Success", "BMI calculated and saved successfully.")

    def view_history():
        history_window = tk.Toplevel(main_window)
        history_window.iconbitmap('Images/crown_icon.ico') 
        history_window.title("Body Mass Index History")
        history_window.geometry("600x400")

        tree = ttk.Treeview(history_window, columns=("ID", "Name", "Weight", "Height", "BMI", "Category", "Date"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Weight", text="Weight")
        tree.heading("Height", text="Height")
        tree.heading("BMI", text="BMI")
        tree.heading("Category", text="Category")
        tree.heading("Date", text="Date")

        tree.pack(fill=tk.BOTH, expand=True)

        c.execute("SELECT * FROM bmi_records")
        records = c.fetchall()
        for record in records:
            bmi_category = classify_bmi(record[4])
            tree.insert("", tk.END, values=(record[0], record[1], record[2], record[3], record[4], bmi_category, record[5]))

        def delete_record():
            selected_item = tree.selection()[0]
            record_id = tree.item(selected_item)['values'][0]
            c.execute("DELETE FROM bmi_records WHERE id=?", (record_id,))
            conn.commit()
            tree.delete(selected_item)
            messagebox.showinfo("Success", f"Record with ID {record_id} deleted successfully.")

        delete_button = tk.Button(history_window, text="Delete Selected Record", command=delete_record)
        delete_button.pack(pady=10)

    def open_feedback():
        feedback_window = tk.Toplevel(main_window)
        feedback_window.iconbitmap('Images/crown_icon.ico') 
        feedback_window.title("Feedback")
        feedback_window.geometry("400x300")

        tk.Label(feedback_window, text="Please provide your feedback:").pack(pady=10)
        feedback_text = tk.Text(feedback_window, height=10, width=50)
        feedback_text.pack(pady=10)

        def submit_feedback():
            feedback = feedback_text.get("1.0", tk.END).strip()
            if feedback:
                messagebox.showinfo("Thank You", "Thank you for your feedback!")
                feedback_window.destroy()
            else:
                messagebox.showwarning("Input Error", "Please enter your feedback before submitting.")

        submit_button = tk.Button(feedback_window, text="Submit Feedback", command=submit_feedback)
        submit_button.pack(pady=10)

    frame = Frame(main_window, bg='white', bd=10)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.8, relheight=0.8)

    tk.Label(frame, text="Name:", bg='white').grid(row=0, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=50, pady=10)

    tk.Label(frame, text="Weight (kg):", bg='white').grid(row=1, column=0)
    weight_entry = tk.Entry(frame)
    weight_entry.grid(row=1, column=1, padx=50, pady=10)

    tk.Label(frame, text="Height (cm):", bg='white').grid(row=2, column=0)
    height_entry = tk.Entry(frame)
    height_entry.grid(row=2, column=1, padx=50, pady=10)

    calculate_button = tk.Button(frame, text="Calculate BMI", command=calculate)
    calculate_button.grid(row=3, column=0, columnspan=2, padx=91, pady=10)

    save_button = tk.Button(frame, text="Save BMI", command=save)
    save_button.grid(row=4, column=0, columnspan=2, padx=91, pady=10)

    result_label = tk.Label(frame, text="BMI: ", bg='white')
    result_label.grid(row=5, column=0, columnspan=2)

    history_button = tk.Button(frame, text="View History", command=view_history)
    history_button.grid(row=6, column=0, columnspan=2, padx=91, pady=10)

    feedback_button = tk.Button(frame, text="Calculations Complete", command=open_feedback)
    feedback_button.grid(row=7, column=0, columnspan=2, padx=91, pady=10)

    main_window.bg_img = bg_img

    main_window.mainloop()

    conn.close()

splash_screen = Tk()
splash_screen.title('Welcome to BMI Calculator')
splash_screen.iconbitmap('Images/crown_icon.ico')
splash_screen.geometry('470x400')


original_img = Image.open('Images/Screenshot (443).png')
resized_img = original_img.resize((470, 300), Image.Resampling.LANCZOS)
my_img = ImageTk.PhotoImage(resized_img)


frame = Frame(splash_screen)
frame.pack(expand=True, fill=BOTH)

my_label = Label(frame, image=my_img)
my_label.pack()

continue_button = Button(frame, text="Continue", command=lambda: [splash_screen.destroy(), open_main_window()])
continue_button.pack(pady=10)

splash_screen.mainloop()
