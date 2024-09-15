import tkinter as tk
from auth import AuthWindow
from file_manager import FileManager

def main():
    root = tk.Tk()
    root.geometry("400x600")  # Android-like app size
    app = AuthWindow(root, lambda username: go_to_file_manager(root, username))
    root.mainloop()

def go_to_file_manager(root, username):
    for widget in root.winfo_children():
        widget.destroy()
    file_manager = FileManager(root, username, lambda: go_back_to_auth(root))
    file_manager.setup_ui()

def go_back_to_auth(root):
    for widget in root.winfo_children():
        widget.destroy()
    app = AuthWindow(root, lambda username: go_to_file_manager(root, username))

if __name__ == "__main__":
    main()
