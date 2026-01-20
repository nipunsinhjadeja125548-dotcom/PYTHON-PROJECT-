import os
import tkinter as tk
from tkinter import messagebox, filedialog
import subprocess
import platform

class FolderProtectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Folder Protection App")
        self.root.geometry("500x300")

        self.protected_folder = None
        self.password = None

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Folder selection
        self.folder_label = tk.Label(self.root, text="Select Folder to Protect:")
        self.folder_label.pack(pady=10)

        self.folder_entry = tk.Entry(self.root, width=50)
        self.folder_entry.pack(pady=10)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        self.browse_button.pack(pady=5)

        # Password setting
        self.password_label = tk.Label(self.root, text="Set Password to Protect Folder:")
        self.password_label.pack(pady=10)

        self.password_entry = tk.Entry(self.root, width=50, show="*")
        self.password_entry.pack(pady=10)

        self.set_password_button = tk.Button(self.root, text="Set Password", command=self.set_password)
        self.set_password_button.pack(pady=10)

        # Unlock Folder
        self.unlock_button = tk.Button(self.root, text="Unlock Folder", command=self.unlock_folder, state=tk.DISABLED)
        self.unlock_button.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder_selected)
            self.protected_folder = folder_selected

    def set_password(self):
        if not self.protected_folder:
            messagebox.showerror("Error", "Please select a folder first!")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showerror("Error", "Password cannot be empty!")
            return

        self.password = password
        self.password_entry.config(state=tk.DISABLED)
        self.set_password_button.config(state=tk.DISABLED)
        self.unlock_button.config(state=tk.NORMAL)

        # Lock the folder (hide it or restrict access)
        self.lock_folder()
        messagebox.showinfo("Success", "Password set! Folder is now protected.")

    def lock_folder(self):
        if os.name == 'nt':  # Windows
            os.system(f'attrib +h +s "{self.protected_folder}"')
        elif os.name == 'posix':  # Linux/Mac
            os.system(f'chmod 000 "{self.protected_folder}"')
        else:
            messagebox.showerror("Error", "Unsupported OS")

    def unlock_folder(self):
        if not self.protected_folder:
            messagebox.showerror("Error", "No folder selected!")
            return

        password_prompt = tk.simpledialog.askstring("Unlock Folder", "Enter password to unlock:", show="*")
        if password_prompt == self.password:
            # Unlock the folder (make it visible or restore access)
            if os.name == 'nt':  # Windows
                os.system(f'attrib -h -s "{self.protected_folder}"')
            elif os.name == 'posix':  # Linux/Mac
                os.system(f'chmod 755 "{self.protected_folder}"')
            messagebox.showinfo("Success", "Password correct! Folder unlocked.")
            self.open_folder(self.protected_folder)
        else:
            messagebox.showerror("Error", "Incorrect password!")

    def open_folder(self, folder_path):
        # Open the folder in the file explorer
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", folder_path])
        elif platform.system() == "Linux":
            subprocess.call(["xdg-open", folder_path])
        else:
            messagebox.showerror("Error", "Unsupported OS")

if __name__ == "__main__":
    root = tk.Tk()
    app = FolderProtectionApp(root)
    root.mainloop()
