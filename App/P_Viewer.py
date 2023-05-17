from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog

from utils.Process_Dicom import from_Dicom_STL_Encapsulated, new_create_Dicom_From_Nothing

import os
Text_intro = "This page allow to manipulate DICOM STL Encapsulated files."

class P_Viewer(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        label = Label(self, text=Text_intro, font=("Arial", 12), borderwidth=2, relief="solid")
        label.place(x=50, y=10, width=550, height=45)

        self.ExtractButton = Button(self, text="Extract STL from DICOM STL Encapsulated", command=self.select_DICOM)
        self.ExtractButton.place(x=50, y=105, width=550, height=35)

        self.IntracrButton = Button(self, text="Encapsulate STL file into an empty DICOM", command=self.select_STL)
        self.IntracrButton.place(x=50, y=155, width=550, height=35)


    def select_DICOM(self):
        filetypes = [('DICOM File', '*.dcm')]
        file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose a file", filetypes=filetypes)
        if file:
            from_Dicom_STL_Encapsulated(file)
            print("File extracted to :"+os.path.dirname(file))

    def select_STL(self):
        filetypes = [('STL File', '*.stl')]
        file = filedialog.askopenfilename(initialdir=os.getcwd(), title="Choose a file", filetypes=filetypes)
        if file:
            new_create_Dicom_From_Nothing(file)
            print("File encapsulate to :" + os.path.dirname(file))
