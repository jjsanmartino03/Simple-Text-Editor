import tkinter as tk
from tkinter import filedialog, messagebox
from io import open
import pickle
import os


class App(tk.Tk):
    file_directory = None
    key_codes = None
    file_name = None

    def __init__(self):
        global file_directory, key_codes, file_name
        # variables---------------------
        key_codes = [16, 17, 18, 19, 20, 27, 33, 32, 34, 35, 37, 38, 39, 40, 44]  # these are the key codes of the
        # keys like Control, the arrows, shift...
        file_directory = None
        file_name = None
        # GUI configuration-----------------------
        super().__init__()  # It inherits for tk.tk()
        self.titly = tk.StringVar()  # declaring the variable of the title, the name of the differents files
        self.file_title = tk.Label(self, pady=15, textvariable=self.titly, font=("Comic Sans MS", 20))
        self.file_title.pack()
        self.framie = tk.Frame(self)
        self.framie.pack()
        self.text_box = tk.Text(self.framie, height=15, width=70, font=("Courier New", 16))
        self.text_box.config(insertwidth=7, selectbackground="#077371", spacing1=5, tabs=30, wrap="word")
        self.text_box.grid(row=0, column=0)
        self.scroll_bar = tk.Scrollbar(self.framie, command=self.text_box.yview)
        self.scroll_bar.grid(row=0, column=1, sticky="nsew")
        self.text_box.config(yscrollcommand=self.scroll_bar.set)
        self.text_box.focus()
        # menu configuration------------------
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open", command=self.open_it, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_it, accelerator="Ctrl+S")
        file_menu.add_command(label="Save as", command=self.save_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Close file", command=self.close_it, accelerator="Ctrl+W")
        # Shorcuts-------
        self.framie.bind_all("<Control-s>", self.ctrl_save)
        self.framie.bind_all("<Control-o>", self.ctrl_open)
        self.framie.bind_all("<Control-w>", self.ctrl_close_file)
        self.framie.bind_all("<Control-n>", self.ctrl_close_file)
        self.framie.bind_all("<Control-q>", self.ctrl_save_as)
        self.framie.bind_all("<Alt-c>", self.call_destroy)
        self.text_box.bind("<Key>", self.change)  # to see if the file is saved or not
        self.text_box.bind("<Control-Shift_L>", self.control_shift)
        self.protocol("WM_DELETE_WINDOW", lambda: self.closing_handler(True))
        self.open_last()

    # Functionality
    def open_last(self):  # Opens the last opened file, if possible
        global file_directory, file_name

        def set_default(self):
            self.titly.set("Untitled")
            self.title("Untitled - Pocket Note Editor")
            file_name = "Untitled"
            file_directory = "Untitled"
        
        if os.path.isfile("last"):
            last_one = open("last", "rb")  # opens the file where it's written the last directory
            try:
                file_directory = pickle.load(last_one)
                file_name = file_directory.split("/")[-1]
                self.title(f"{file_directory} - Pocket Note Editor")  # set the title as the name of the file
                self.titly.set(file_name)
                # Opens and gets the file content
                file_text = open(file_directory, "r")
                self.text_box.insert("1.0", file_text.read())
                file_text.close()
            except:
                set_default(self)
            finally:
                last_one.close()
        else:
            set_default(self)

    def open_it(self):
        global file_directory, file_name
        cancel = self.closing_handler(False)  # a function that aks the user to save the file
        if cancel:
            return None
        try_file = filedialog.askopenfilename(title="Open", initialdir="C:/Chulian/AA real_life/Python/myNotes",
                                             filetypes=(("All Files", ".*"), ("Python Files", "*.py")))
        if try_file == "":
            return None
        # opens the file and gets what is wrote in it
        file = open(try_file, "r+")
        try:
            textie = file.read()
        except:
            messagebox.showwarning("Opening Error", "This file can't be read")
            return None
        file_directory = try_file
        self.text_box.delete("1.0", "end-1c")
        self.text_box.insert("1.0", textie)
        file.close()
        file_name = file_directory.split("/")[-1]
        self.titly.set(file_name)
        self.title(f"{file_directory} - Pocket Note Editor")
        # opens 'last' and writes the directory of the opened file
        last_one = open("last", "wb")
        pickle.dump(file_directory, last_one)
        last_one.close()

    def save_as(self):
        global file_directory, file_name
        try_file = filedialog.asksaveasfilename(title="Save as",
                                                      initialdir="C:/Chulian/AA real_life/Python/myNotes")
        print(try_file)
        if try_file != "":  # If the user didn't pressed 'cancel'
            file_directory = try_file
            # opens the file in the directory and writes in it what is in the textbox
            save_file = open(file_directory, "w")
            save_file.write(self.text_box.get("1.0", "end-1c"))
            save_file.close()
            # sets the titles
            file_name = file_directory.split("/")[-1]
            self.titly.set(file_name)
            self.title(f"{file_directory} - Pocket Note Editor")
            # opens 'last' and writes the directory of the opened file
            last_one = open("last", "wb")
            pickle.dump(file_directory, last_one)
            last_one.close()
        else:
            return None

    def save_it(self):
        global file_directory, file_name
        if file_directory is not None and file_directory != "Untitled":

            file = open(file_directory, "w")
            file.write(self.text_box.get("1.0", "end-1c"))
            file.close()

            self.title(f"{file_directory} - Pocket Note Editor")
            file_name = file_directory.split("/")[-1]
            self.titly.set(file_name)

            last_one = open("last", "wb")
            pickle.dump(file_directory, last_one)
            last_one.close()
        else:
            self.save_as()

    def close_it(self):
        global file_directory, file_name
        cancel = self.closing_handler(False)
        if cancel:
            return None
        self.text_box.delete("1.0", "end-1c")
        file_directory = "Untitled"
        file_name = "New file"
        self.titly.set("Untitled")
        self.title(f"{file_directory} - Pocket Note Editor")
        last_one = open("last", "w")
        last_one.write("")
        last_one.close()

    # keyboard shortcuts ---------------------------------------------
    def ctrl_save(self, event):
        self.save_it()

    def ctrl_save_as(self, event):
        self.save_as()

    def ctrl_open(self, event):
        self.open_it()

    def ctrl_close_file(self, event):
        self.close_it()

    def call_destroy(self, event):
        self.destroy()

    # The methods to success with the Ctrl+Shift+S shortcut
    def control_shift(self,event):
        self.text_box.bind("<S>", self.control_shift_s)

    def control_shift_s(self,event):
        self.save_as()
        self.text_box.unbind("<S>")

    # the method that makes possible to the user to see if the file is saved or not
    def change(self, event):
        global key_codes, file_directory
        if "※" not in self.titly.get():
            if (event.keycode not in key_codes) and (event.state < 20) and (event.state not in [12, 4]):  # This conditional makes sure that the pressed button is a word, tab or backspace before saying that the file is modified.
                self.titly.set(f"{self.titly.get()} ※")
                self.title(f"{self.title().split()[0]}※ - Pocket Note Editor")

    # the method to ask if the user wants to save before closing the GUI or the file
    def closing_handler(self, b):  # If b=True it means that the user wants to close the GUI, if b=False it means that the user wants to close a file
        global file_name
        if "※" not in self.titly.get():
            if b:
                self.destroy()
            else:
                return None
        else:
            wants_to = messagebox.askyesnocancel("Save Changes?", f"{file_name} has been modified, save changes?")
            print(wants_to)
            if wants_to:
                self.save_it()
                if b:
                    self.destroy()
            elif b and not wants_to==None:
                self.destroy()
            if wants_to is None:  # If the users pressed cancel...
                return True


if __name__ == '__main__':
    app = App()
    app.mainloop()
