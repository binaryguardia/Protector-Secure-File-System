import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt
import os

class AuthWindow:
    def __init__(self, root, go_to_file_manager_callback):
        self.root = root
        self.go_to_file_manager_callback = go_to_file_manager_callback
        
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True, fill="both")
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Protector - Sign In")
        
        # Add RGB styles
        style = ttk.Style()
        style.configure("TLabel", foreground="white", background="black", font=('Arial', 12, 'bold'))
        style.configure("TButton", foreground="black", background="#FF5733", font=('Arial', 10, 'bold'))
        
        ttk.Label(self.frame, text="Protector - Secure File System", font=('Arial', 14, 'bold')).pack(pady=20)
        
        ttk.Label(self.frame, text="Username:").pack(pady=10)
        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.pack(pady=10)
        
        ttk.Label(self.frame, text="Password:").pack(pady=10)
        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=10)
        
        ttk.Button(self.frame, text="Sign Up", command=self.sign_up).pack(side="left", padx=10)
        ttk.Button(self.frame, text="Sign In", command=self.sign_in).pack(side="right", padx=10)
        
        ttk.Button(self.frame, text="Exit", command=self.exit_app).pack(pady=20)

    def sign_up(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode()

        if username and password:
            # Check if user already exists
            if self.user_exists(username):
                messagebox.showerror("Error", "User already exists. Please sign in.")
                return

            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            with open("user_data.txt", "a") as f:
                f.write(f"{username},{hashed_password.decode()}\n")
            messagebox.showinfo("Sign Up", "Signed up successfully!")
        else:
            messagebox.showerror("Error", "Please fill in both fields!")

    def sign_in(self):
        username = self.username_entry.get()
        password = self.password_entry.get().encode()

        if username and password:
            if self.authenticate(username, password):
                messagebox.showinfo("Sign In", f"Welcome {username}!")
                self.go_to_file_manager_callback(username)
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        else:
            messagebox.showerror("Error", "Please fill in both fields!")

    def user_exists(self, username):
        if not os.path.exists("user_data.txt"):
            return False
        with open("user_data.txt", "r") as f:
            users = f.readlines()
        for user in users:
            stored_username, _ = user.strip().split(',')
            if stored_username == username:
                return True
        return False

    def authenticate(self, username, password):
        with open("user_data.txt", "r") as f:
            users = f.readlines()
        for user in users:
            stored_username, stored_password = user.strip().split(',')
            if stored_username == username and bcrypt.checkpw(password, stored_password.encode()):
                return True
        return False

    def exit_app(self):
        self.root.quit()
