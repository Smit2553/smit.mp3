import customtkinter
import sqlite3
from tkinter import filedialog

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


def primary_folder(c, conn):
    folder_location = filedialog.askdirectory(initialdir="/", title="Select Folder")
    if folder_location:
        c.execute("SELECT * FROM config WHERE name = 'folder'")
        if c.fetchone() is not None:
            c.execute("UPDATE config SET value = ? WHERE name = 'folder'", (folder_location,))
            conn.commit()
        else:
            c.execute("INSERT INTO config (name, value) VALUES (?, ?)", ("folder", folder_location))
            conn.commit()


def change_folder():
    conn = sqlite3.connect('./config/config.db')
    c = conn.cursor()
    primary_folder(c, conn)
    c.close()
    conn.close()


class FolderConfirmationDialogue(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x300")
        conn = sqlite3.connect('./config/config.db')
        c = conn.cursor()
        folder_location = c.execute("SELECT value FROM config WHERE name = 'folder'").fetchone()[0]
        c.close()
        conn.close()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure((0, 1), weight=1)
        self.label = customtkinter.CTkLabel(self, text=f"You have set your primary folder to: {folder_location}")
        self.label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.button = customtkinter.CTkButton(self, text="Change Folder", command=change_folder)
        self.button.grid(row=0, column=1, padx=20, pady=20, sticky="ew")
        self.close_button = customtkinter.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.toplevel_window = None
        self.geometry("400x240")
        self.title("smit.mp3")
        self.minsize(300, 200)
        conn = sqlite3.connect('./config/config.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS config (name TEXT PRIMARY KEY, value TEXT)")
        if c.execute("SELECT * FROM config WHERE name = 'folder'").fetchone() is None:
            primary_folder(c, conn)
            self.open_folder_confirm()
        c.close()
        conn.close()

    def open_folder_confirm(self):
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = FolderConfirmationDialogue(self)
            self.toplevel_window.focus()
        else:
            self.toplevel_window.focus()


if __name__ == "__main__":
    app = App()
    app.mainloop()
