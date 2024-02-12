import tkinter as tk
from tkinter import messagebox
from base_app import BaseApp


class ComparisionApp(BaseApp):
    def __init__(self, master):
        super().__init__(master, "Porównaj Sekwencje")

        self.sequence1_text = tk.Text(self.master, wrap=tk.WORD, height=10, width=60)
        self.sequence2_text = tk.Text(self.master, wrap=tk.WORD, height=10, width=60)

        self.sequence1_text.place(x=230, y=5)
        self.sequence2_text.place(x=230, y=200)

        self.load_sequence1_button = tk.Button(
            self.master,
            text="Wczytaj z pliku pierwszą sekwencję",
            command=lambda: self.load_sequence_from_file(self.sequence1_text),
            width=26,
            height=1,
        )
        self.load_sequence2_button = tk.Button(
            self.master,
            text="Wczytaj z pliku drugą sekwencję",
            command=lambda: self.load_sequence_from_file(self.sequence2_text),
            width=26,
            height=1,
        )
        
        self.clear_button = tk.Button(
            self.master, 
            text="Wyczyść", 
            command=self.on_clear, 
            width=26, 
            height=1
        )
        self.find_differences_button = tk.Button(
            self.master,
            text="Znajdź różnice",
            command=self.find_differences,
            width=26,
            height=1,
        )
        
        self.load_sequence1_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.load_sequence2_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.clear_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.find_differences_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)

    def load_sequence_from_file(self, text_widget):
        nucleotides = self.load_file()

        if nucleotides is not None:
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, nucleotides)

    def find_differences(self):
        sequence1 = self.sequence1_text.get("1.0", tk.END).strip()
        sequence2 = self.sequence2_text.get("1.0", tk.END).strip()

        if not sequence1 or not sequence2:
            messagebox.showinfo("Info", "Załaduj obie sekwencje przed porównaniem.")
            return

        len1 = len(sequence1)
        len2 = len(sequence2)

        differences = [
            (i + 1, sequence1[i], sequence2[i])
            for i in range(min(len1, len2))
            if sequence1[i] != sequence2[i]
        ]


        tag_name = "difference"
        self.sequence1_text.tag_configure(tag_name, foreground="deeppink")
        self.sequence2_text.tag_configure(tag_name, foreground="deeppink")

        for i, _, _ in differences:
            self.sequence1_text.tag_add(tag_name, f"1.{i}", f"1.{i + 1}")

        for i, _, _ in differences:
            self.sequence2_text.tag_add(tag_name, f"1.{i}", f"1.{i + 1}")

        significant_threshold = 75
        if len(differences) > significant_threshold:
            messagebox.showinfo(
                "Info", "Znaczna różnica - więcej niż 75 sekwencji różni się."
            )
        else:
            dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

            if not differences:
                messagebox.showinfo("Info", "Nie znaleziono różnic we wspólnym fragmencie.")
            else:
                diff_message = "\n".join(
                    [
                        f"pozycja: {pos+1}, sekwencja 1: {nuc1}, sekwencja 2: {nuc2}"
                        for pos, nuc1, nuc2 in differences
                    ]
                )
                messagebox.showinfo("Różnice", f"Znaleziono różnice:\n{diff_message}")

            if len1 > len2:
                tag_name_extra = "extra_nucleotides"
                self.sequence1_text.tag_configure(
                    tag_name_extra, foreground="mediumaquamarine"
                )

                for i in range(len2, len1):
                    self.sequence1_text.tag_add(tag_name_extra, f"1.{i}", f"1.{i + 1}")
            elif len2 > len1:
                tag_name_extra = "extra_nucleotides"
                self.sequence2_text.tag_configure(
                    tag_name_extra, foreground="mediumaquamarine"
                )

                for i in range(len1, len2):
                    self.sequence2_text.tag_add(tag_name_extra, f"1.{i}", f"1.{i + 1}")

    def on_clear(self):
        self.sequence1_text.delete("1.0", tk.END)
        self.sequence2_text.delete("1.0", tk.END)
