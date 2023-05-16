import tkinter
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog, Spinbox
import os
import sys
import pydicom
import threading
from colorama import Fore,Style

from utils import Process_Files

TypeSTL = ['Binary','ASCII']
SmoothOption = ['True','False']
OutputList = ["STL", "DICOM", "STL and DICOM"]

Text_intro = "This page allow to reconstruct 3D Models from NIfTI. \nYou can modify the settings to obtain results that you want.\nBe sure that the NIfTI file are correct before using."
class P_NIfTI(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Ajouter du code pour la page 1 ici
        label = Label(self, text=Text_intro, font=("Arial",12),borderwidth=2,relief="solid")
        label.place(x=50, y=10, width=550, height=57)

        self.ComboSTL = Combobox(self, values=TypeSTL,state="readonly")
        self.ComboSTL.place(x=50, y=100, width=150, height=25)
        self.ComboSTL.current(0)
        self.ComboSTL_text = Label(self, text="Type of the encrypted STL", anchor='w')
        self.ComboSTL_text.place(x=50, y=75, width=150, height=25)

        self.ComboSmooth = Combobox(self, values=SmoothOption,state="readonly")
        self.ComboSmooth.place(x=250, y=100, width=150, height=25)
        self.ComboSmooth.current(0)
        self.ComboSmooth_text = Label(self, text="Smoothing on the output", anchor='w')
        self.ComboSmooth_text.place(x=250, y=75, width=150, height=25)

        self.ComboOutput = Combobox(self, values=OutputList,state="readonly")
        self.ComboOutput.place(x=450, y=100, width=150, height=25)
        self.ComboOutput.current(0)
        self.ComboOutput_text = Label(self, text="Generated output", anchor='w')
        self.ComboOutput_text.place(x=450, y=75, width=150, height=25)

        self.select_button = Button(self, text="Select NIfTI files", command=self.run_code)
        self.select_button.place(x=50, y=195, width=550, height=35)

    def run_code(self):

        # Crée un thread pour exécuter la fonction de traitement
        t = threading.Thread(target=self.select_files)
        t.start()

    def select_files(self):
        filetypes = [('Fichiers DICOM', '*.nii')]
        files = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Choose files", filetypes=filetypes)

        if files:
            for f in files:
                RE_Value = Process_Files.process_Nifti_file(f,Smoothing=self.ComboSmooth.current(),save_external_stl=self.ComboSTL.current(),fichier=self.ComboSTL.current())
                if(RE_Value):
                    print(f.title() +" correctly constructed")
                else:
                    print(f.title() +" not reconstructed")