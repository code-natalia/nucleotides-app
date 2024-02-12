from base_app import BaseApp
from codon_table import CodonTable
import tkinter as tk
from tkinter import filedialog, messagebox


class TranslateApp(BaseApp):
    def __init__(self, master):
        super().__init__(master, "Tłumacz Sekwencje")

        self.sequence_text = tk.Text(
            self.master, wrap=tk.WORD, 
            height=10, width=60
        )
        self.output_text = tk.Text(
            self.master, wrap=tk.WORD, height=10, 
            width=60, state=tk.DISABLED
        )
        self.sequence_text.place(x=230, y=5)
        self.output_text.place(x=230, y=200)

        self.load_file_button = tk.Button(
            self.master,
            text="Wczytaj plik",
            command=self.on_load_file,
            width=26,
            height=1,
        )
        self.translate_button = tk.Button(
            self.master,
            text="Przetłumacz sekwencję",
            command=self.on_translate,
            width=26,
            height=1,
        )
        self.save_button = tk.Button(
            self.master,
            text="Zapisz wynik w nowym pliku",
            command=self.on_save,
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
        self.count_button = tk.Button(
            self.master,
            text="Policz nukleotydy",
            command=self.update_nucleotide_count,
            width=26,
            height=1,
        )
        self.count_result_button = tk.Button(
            self.master,
            text="Oblicz liczbę aminokwasów",
            command=self.count_letters_and_asterisks,
            width=26,
            height=1,
        )

        self.load_file_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.translate_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.save_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.clear_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.count_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)
        self.count_result_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=5)

        self.nucleotide_count_label = tk.Label(
            self.master, text="Liczba nukleotydów: 0"
        )
        self.letter_count_label = tk.Label(
            self.master, text="Liczba aminokwasów: 0"
        )
        self.asterisk_count_label = tk.Label(
            self.master, text="Liczba niezdefiniowanych kodonów: 0"
        )

        self.nucleotide_count_label.place(x=10, y=250)
        self.letter_count_label.place(x=10, y=270)
        self.asterisk_count_label.place(x=10, y=290)

    def on_load_file(self):
        nucleotides = self.load_file()

        if nucleotides is not None:
            self.sequence_text.delete("1.0", tk.END)
            self.sequence_text.insert(tk.END, nucleotides)

    def on_clear(self):
        self.sequence_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)

        self.update_nucleotide_count()
        self.count_letters_and_asterisks()

    def on_save(self):
        result = self.output_text.get("1.0", tk.END).strip()
        if result:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt", filetypes=[("Pliki tekstowe", "*.txt")]
            )
            if file_path:
                with open(file_path, "w") as file:
                    file.write(result)

    def translate_sequence(self, nucleotide_sequence):
        amino_acid_sequence = ""
        for i in range(0, len(nucleotide_sequence), 3):
            codon = nucleotide_sequence[i : i + 3]
            amino_acid_sequence += CodonTable.translate_codon(codon)
        return amino_acid_sequence

    def on_translate(self):
        nucleotide_sequence = self.sequence_text.get("1.0", tk.END).strip()
        if not all(base in "ATCG" for base in nucleotide_sequence):
            messagebox.showerror("Błąd", "Niepoprawna sekwencja nukleotydów!")
            return
        amino_acid_sequence = self.translate_sequence(nucleotide_sequence)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, amino_acid_sequence)
        self.output_text.config(state=tk.DISABLED)

    def update_nucleotide_count(self):
        nucleotide_sequence = self.sequence_text.get("1.0", tk.END).strip()
        if not all(base in "ATCG" for base in nucleotide_sequence):
            messagebox.showerror("Błąd", "Niepoprawna sekwencja nukleotydów!")
            return
        count = len(nucleotide_sequence)
        self.nucleotide_count_label.config(text=f"Liczba nukleotydów: {count}")

    def count_letters_and_asterisks(self):
        result_sequence = self.output_text.get("1.0", tk.END).strip()
        letter_count = sum(c.isalpha() for c in result_sequence)
        asterisk_count = result_sequence.count("*")
        self.letter_count_label.config(text=f"Liczba aminokwasów: {letter_count}")
        self.asterisk_count_label.config(
            text=f"Liczba niezdefiniowanych kodonów: {asterisk_count}"
        )
