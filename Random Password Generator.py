import tkinter as tk
from tkinter import messagebox
import colorsys
import requests
import random

# GUI Window Code
root = tk.Tk()
root.title("Neon Password Generator!")
root.geometry('750x750')
root.config(bg='#121212')

# RGB Color Cycling
def rgb_cycle(widget):
    hue = 0
    def update_color():
        nonlocal hue
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        widget.config(fg=color)
        hue = (hue + 0.01) % 1
        root.after(50, update_color)
    update_color()

# Label
label = tk.Label(root, text='Custom Password Generator', font=('Arial', 30, 'bold'), bg='#121212', fg='white')
label.pack(pady=30)
rgb_cycle(label)

def generate_password():
    try:
        # Get user input
        num_digits = int(entry_digits.get())
        num_special_chars = int(entry_specialchars.get())
        num_words = int(entry_words.get())

        if num_digits < 0 or num_special_chars < 0 or num_words < 0:
            raise ValueError("Numbers cannot be negative.")

        # Generate password
        password = []
        for _ in range(num_words):
            response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
            if response.status_code == 200:
                word = response.json()[0]
                password.append(word)
            else:
                messagebox.showerror("Error", "Failed to fetch words. Please try again.")
                return

        for _ in range(num_special_chars):
            password.append(random.choice(['!', '@', '#', '$', '%', '^', '&', '*']))

        for _ in range(num_digits):
            password.append(str(random.randint(0, 9)))

        # Shuffle the list to mix up the order
        random.shuffle(password)

        # Join the list into a single string
        password = ''.join(password)

        # Display the generated password
        result_label.config(text=f"Generated Password: {password}")
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

# Hover Effect
def on_hover(event):
    event.widget.config(bg='#00ffff', fg='black')

def on_leave(event):
    event.widget.config(bg='#1a1a1a', fg='#00ffff')

# Number of digits label
label_digits = tk.Label(root, text='Number of digits:', font=('Arial',20), bg='#121212', fg='#33CC33')
label_digits.pack(pady=13)

# User input for digits label
entry_digits = tk.Entry(root, font=('Arial',15), justify='center', bg='#2a2a2a', fg='#FFA07A', insertbackground='#FFA07A', highlightthickness=2, highlightbackground='black', highlightcolor='black', borderwidth=5, relief="ridge")
entry_digits.pack(pady=7)

# Number of special characters label
label_specialchars = tk.Label(root, text='Number of special characters:', font=('Arial',20), bg='#121212', fg='#33CC33')
label_specialchars.pack(pady=13)

# User input for special characters label
entry_specialchars = tk.Entry(root, font=('Arial',15), justify='center', bg='#2a2a2a', fg='#FFA07A', insertbackground='#FFA07A', highlightthickness=2, highlightbackground='black', highlightcolor='black', borderwidth=5, relief="ridge")
entry_specialchars.pack(pady=7)

# Number of words label
label_words = tk.Label(root, text='Number of words:', font=('Arial',20), bg='#121212', fg='#33CC33')
label_words.pack(pady=13)

# User input for words label
entry_words = tk.Entry(root, font=('Arial',15), justify='center', bg='#2a2a2a', fg='#FFA07A', insertbackground='#FFA07A', highlightthickness=2, highlightbackground='black', highlightcolor='black', borderwidth=5, relief="ridge")
entry_words.pack(pady=7)

# Generate Password button
button = tk.Button(root, text='Generate Password', command=generate_password, font=('Arial', 15), bg='#1a1a1a', fg='#00ffff', activebackground='#00ffff', activeforeground='black')
button.pack(pady=50)
button.bind("<Enter>", on_hover)
button.bind("<Leave>", on_leave)

# Generated Password label
result_label = tk.Label(root, text="",font=('Arial', 20), wraplength=400, bg='#121212', fg='white')
result_label.pack()
rgb_cycle(result_label)

# Application Start
root.mainloop()