import tkinter as tk
from tkinter import ttk, scrolledtext, INSERT

import sys
import requests
import os
import subprocess
import webbrowser
import time
from colorama import Fore

from P_Viewer import P_Viewer
from P_RT_Struct import P_RT_Struct
from P_NIfTI import P_NIfTI
from P_TotalSegmentator import P_TotalSegmentator

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.server_process = None

        self.title("DICOM-STL")
        self.geometry("650x500")
        self.resizable(width=False, height=False)

        # Création du widget Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Création de la première page
        self.page1 = P_RT_Struct(self.notebook)
        self.notebook.add(self.page1, text="Reconstruction from RT Struct")

        # Création de la deuxième page
        self.page2 = P_Viewer(self.notebook)
        self.notebook.add(self.page2, text="DICOM STL Encapsulated")

        self.page3 = P_NIfTI(self.notebook)
        self.notebook.add(self.page3, text="Reconstruction from NIfTI")

        self.page4 = P_TotalSegmentator(self.notebook)
        self.notebook.add(self.page4, text="Total Segmentator")

        self.output = scrolledtext.ScrolledText(self, font=("Arial", 11), borderwidth=1, relief="solid")
        self.output.place(x=50, y=275, width=550, height=155)

        sys.stdout.write = self.write_stdout

        self.select_button = tk.Button(self, text="Show DICOM STL Encapsulated", command=self.select_files)
        self.select_button.place(x=50, y=470, width=200, height=25)

        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.quit_button = tk.Button(self, text="Quit", command=self.quitter)
        self.quit_button.place(x=500, y=470, width=100, height=25)


    def write_stdout(self, message):
        # self.output.config(text=self.output.cget("text") + message)
        colored_text = message.replace("[RED]",Fore.RED).replace("[GREEN]",Fore.GREEN)
        self.output.insert(INSERT, colored_text)
    def select_files(self):
        filetypes = (
            ('Fichiers DICOM', '*.dcm'),
            ('Tous les fichiers', '*.*')
        )
        if self.server_process != None:
            webbrowser.open_new('http://localhost:5000')
            return

        files = tk.filedialog.askopenfilenames(initialdir=os.getcwd(), title="Sélectionner des fichiers",filetypes=filetypes)
        if files:
            print("avant sub process")
            self.server_process = subprocess.Popen(['python', 'server.py'] + list(files))

            try:
                r = requests.get("http://localhost:5000")
                r.raise_for_status()
                print("Serveur en cours d'exécution.")
                webbrowser.open_new('http://localhost:5000')

            except requests.exceptions.RequestException:
                print("Serveur indisponible.")
                time.sleep(2)

    def quitter(self):
        if self.server_process:
            self.server_process.terminate()
        self.quit()


if __name__ == "__main__":
    app = MyApp()

    app.mainloop()