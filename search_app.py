from base_app import BaseApp
import tkinter as tk
from tkinter import messagebox, simpledialog


class SearchApp(BaseApp):
    def __init__(self, master):
        super().__init__(master, "Szukaj Sekwencje")

        self.sequence_text = tk.Text(self.master, wrap=tk.WORD, height=10, width=60)
        self.sequence_text.place(x=230, y=5)

        self.load_file_button = tk.Button(
            self.master,
            text="Wczytaj plik",
            command=self.on_load_file,
            width=26,
            height=1,
        )
        self.find_button = tk.Button(
            self.master,
            text="Wyszukaj sekwencje nukleotydów",
            command=self.find_sequence,
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
        self.load_file_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.find_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.clear_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)

    def on_load_file(self):
        nucleotides = self.load_file()

        if nucleotides is not None:
            self.sequence_text.delete("1.0", tk.END)
            self.sequence_text.insert(tk.END, nucleotides)

    def find_sequence(self):
        sequence_to_find = simpledialog.askstring(
            "Znajdź sekwencję", "Podaj sekwencję do znalezienia:"
        )

        if not all(base in "ATCG" for base in sequence_to_find):
            messagebox.showerror("Błąd", "Niepoprawna sekwencja nukleotydów.")
            return

        if sequence_to_find is not None:
            input_content = self.sequence_text.get("1.0", tk.END)
            self.sequence_text.tag_remove(
                "highlight", "1.0", tk.END
            )  

            positions = []
            start_index = input_content.find(sequence_to_find)

            while start_index != -1:
                positions.append(start_index + 1)
                self.sequence_text.tag_add(
                    "highlight",
                    f"1.{start_index}",
                    f"1.{start_index + len(sequence_to_find)}",
                )
                start_index = input_content.find(sequence_to_find, start_index + 1)

            if positions:
                positions_str = ", ".join(map(str, positions))
                messagebox.showinfo(
                    "Znaleziono",
                    f"Sekwencja '{sequence_to_find}' została znaleziona na pozycjach: {positions_str}.",
                )
            else:
                messagebox.showinfo(
                    "Nie znaleziono",
                    f"Sekwencja '{sequence_to_find}' nie została znaleziona.",
                )

        self.sequence_text.tag_configure("highlight", background="yellow")

    def on_clear(self):
        self.sequence_text.delete("1.0", tk.END)
