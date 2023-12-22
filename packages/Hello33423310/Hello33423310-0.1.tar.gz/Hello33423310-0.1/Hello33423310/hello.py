from tkinter import messagebox

def display_description():
    """
    Fungsi untuk menampilkan deskripsi program pada konsol
    dan dalam sebuah dialog informasi.
    """
    description = """
    ini contoh deskripsi
    """

    print(description)
    messagebox.showinfo("Deskripsi kode program kelompok 2", description)

# Panggil fungsi untuk menampilkan deskripsi
display_description()
