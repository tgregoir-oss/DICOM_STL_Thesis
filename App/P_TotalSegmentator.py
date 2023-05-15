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
typeTask = ["total","lung_vessels","covid","cerebral_bleed","hip_implant","coronary_arteries","body","pleural_pericard_effusion","liver_vessels","heartchambers_test","bones_tissue_test","aortic_branches_test"]
fastOption = [False,True]
Text_intro = "This page allow to reconstruct 3D Models from a serie of DICOM CT Scan. \nYou can modify the settings to obtain results that you want."
class P_TotalSegmentator(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Ajouter du code pour la page 1 ici
        label = Label(self, text=Text_intro, font=("Arial",12),borderwidth=2,relief="solid")
        label.place(x=50, y=10, width=550, height=45)

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

        self.ComboTask = Combobox(self, values=typeTask, state="readonly")
        self.ComboTask.place(x=50, y=150, width=150, height=25)
        self.ComboTask.current(0)
        self.ComboTask_text = Label(self, text="Type of Task", anchor='w')
        self.ComboTask_text.place(x=50, y=125, width=150, height=25)

        self.ComboFast = Combobox(self, values=fastOption, state="readonly")
        self.ComboFast.place(x=250, y=150, width=150, height=25)
        self.ComboFast.current(0)
        self.ComboFast_text = Label(self, text="Fast Segmentation", anchor='w')
        self.ComboFast_text.place(x=250, y=125, width=150, height=25)

        self.select_button = Button(self, text="Select DICOM CT scan serie folder", command=self.run_code)
        self.select_button.place(x=50, y=195, width=550, height=35)

    def run_code(self):

        # Crée un thread pour exécuter la fonction de traitement
        t = threading.Thread(target=self.select_files)
        t.start()

    def select_files(self):
        directory = filedialog.askdirectory(initialdir=os.getcwd(), title="Sélectionner des fichiers")

        if directory:
            Process_Files.check_dicom_series(directory,0,0,fast=self.ComboFast.get(),task=self.ComboTask.get(),fichier=self.ComboSTL.get(),save_external_stl=self.ComboOutput.get(),smoothing=self.ComboSmooth.get())