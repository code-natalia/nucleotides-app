from tkinter import filedialog, messagebox


class BaseApp:
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
        self.master.geometry("750x400")

    def load_file(self):
        try:
            file_path = filedialog.askopenfilename(
                title="Wybierz plik",
                filetypes=[
                    ("Pliki tekstowe", "*.txt"),
                    ("Pliki FASTA", "*.fasta;*.fa"),
                ],
            )

            if file_path:
                nucleotides = ""
                with open(file_path, "r") as file:
                    if file_path.lower().endswith((".fasta", ".fa")):
                        for line in file:
                            if not line.startswith(">"):
                                nucleotides += line.strip()
                    else:  
                        nucleotides = file.read()

                return nucleotides
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd podczas otwierania pliku: {e}")
            return None
