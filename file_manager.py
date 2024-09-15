import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
from cryptography.fernet import Fernet
import requests
import random
import string

class FileManager:
    def __init__(self, root, username, go_back_callback):
        self.root = root
        self.username = username
        self.go_back_callback = go_back_callback
        self.key = self.load_or_generate_key()
        self.cipher = Fernet(self.key)
        self.frame = ttk.Frame(self.root, padding="20")
        self.frame.pack(expand=True, fill='both')

    def setup_ui(self):
        self.root.title("Protector - File Manager")
        ttk.Label(self.frame, text=f"Welcome, {self.username}!").grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.frame, text="Upload File", command=self.upload_file).grid(row=1, column=0, pady=10)
        ttk.Button(self.frame, text="Download File", command=self.download_file).grid(row=1, column=1, pady=10)
        ttk.Button(self.frame, text="Share File", command=self.share_file).grid(row=2, column=0, pady=10)
        
        self.file_list = tk.Listbox(self.frame, width=50, height=15)
        self.file_list.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.frame, text="Go Back", command=self.go_back).grid(row=4, column=0, columnspan=2, pady=10)
        
        self.update_file_list()

    def upload_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to upload")
        if file_path:
            with open(file_path, "rb") as file:
                encrypted_data = self.cipher.encrypt(file.read())
            with open(f"encrypted_{os.path.basename(file_path)}", "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)
            messagebox.showinfo("Success", f"File uploaded and encrypted: {file_path}")
            self.update_file_list()

    def download_file(self):
        selected = self.file_list.curselection()
        if selected:
            file_name = self.file_list.get(selected[0])
            with open(file_name, "rb") as encrypted_file:
                decrypted_data = self.cipher.decrypt(encrypted_file.read())
            save_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Decrypted File")
            if save_path:
                with open(save_path, "wb") as decrypted_file:
                    decrypted_file.write(decrypted_data)
                messagebox.showinfo("Success", f"File decrypted and saved: {save_path}")
        else:
            messagebox.showerror("Error", "Please select a file to download")

    def share_file(self):
        selected = self.file_list.curselection()
        if selected:
            file_name = self.file_list.get(selected[0])
            password = self.generate_password()
            link = self.generate_share_link(file_name, password)
            messagebox.showinfo("Share Link", f"Shareable link: {link}\nPassword: {password}")
        else:
            messagebox.showerror("Error", "Please select a file to share")

    def generate_password(self):
        length = 12  # Length of the password
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for i in range(length))
        return password

    def generate_share_link(self, file_name, password):
        file_path = os.path.abspath(file_name)
        response = requests.post("http://127.0.0.1:5000/share", data={
            'file_path': file_path,
            'filename': file_name,
            'password': password
        })
        if response.status_code == 200:
            return response.json()["link"]
        else:
            return "Error generating share link"

    def update_file_list(self):
        self.file_list.delete(0, tk.END)
        for file in os.listdir():
            if file.startswith("encrypted_"):
                self.file_list.insert(tk.END, file)

    def go_back(self):
        self.go_back_callback()

    def load_or_generate_key(self):
        key_file = "secret.key"
        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key
