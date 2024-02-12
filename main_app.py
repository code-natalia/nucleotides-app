import tkinter as tk
from search_app import SearchApp
from translate_app import TranslateApp
from comparison_app import ComparisionApp


class NucleotidesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplikacja Sekwencji")

        self.menu_frame = tk.Frame(self.master)
        self.menu_frame.pack(pady=28)

        self.translator_button = tk.Button(
            self.menu_frame, text="TŁUMACZ SEKWENCJE", command=self.open_translator
        )
        self.comparator_button = tk.Button(
            self.menu_frame, text="PORÓWNAJ SEKWENCJE", command=self.open_comparator
        )
        self.search_button = tk.Button(
            self.menu_frame, text="SZUKAJ SEKWENCJE", command=self.open_search
        )

        self.translator_button.grid(row=0, column=0, padx=10)
        self.comparator_button.grid(row=0, column=1, padx=10)
        self.search_button.grid(row=0, column=2, padx=10)

    def open_translator(self):
        translator_window = tk.Toplevel(self.master)
        TranslateApp(translator_window)

    def open_comparator(self):
        comparator_window = tk.Toplevel(self.master)
        ComparisionApp(comparator_window)

    def open_search(self):
        search_window = tk.Toplevel(self.master)
        SearchApp(search_window)


if __name__ == "__main__":
    root = tk.Tk()
    NucleotidesApp(root)
    root.mainloop()
