import os.path

import numpy as np

from utils.Offset import *
from utils.Point import *
import random
import pydicom
import pydicom.uid as uid
from pydicom.dataset import DataElement
from datetime import date, datetime


def retrieve_Contours(model):
    contours = []
    combien = 0  # Allow to determine the number of stage to see if we have multiple contours for the same Z value
    offset = Offset()

    # TODO faire un tri des Z values au cas ou ça soit pas trier
    for j in range(len(model.value)):
        sub_one_contour_data = []

        c = []
        list_of_points = model[j][0x3006, 0x0050].value
        for i in range(0, len(list_of_points), 3):
            sub = Point()
            sub.x = list_of_points[i + 0]
            sub.y = list_of_points[i + 1]
            sub.z = list_of_points[i + 2]
            offset.modify_offset(sub)
            c.append(sub)

        if (combien != 0):
            if (c[0].z == contours[len(contours) - 1][0][0].z):
                contours[len(contours) - 1].append(c)
            else:
                sub_one_contour_data.append(c)
                contours.append(sub_one_contour_data)
        else:
            sub_one_contour_data.append(c)
            contours.append(sub_one_contour_data)
        combien += 1

    offset.setup_offset()

    return contours, offset


def from_Dicom_STL_Encapsulated(Dicom_Path):
    DC = pydicom.dcmread(Dicom_Path)
    Dir_path = os.path.dirname(Dicom_Path)
    if ([0x0042, 0x0010] in DC):
        name = DC[0x0042, 0x0010].value+ ".stl"
    else:
        print("Error : The file doesn't contain a STL file encapsulated")
        return
    file = open(Dir_path+"/"+name,"wb")
    file.write(DC[0x0042, 0x0011].value)
    file.close()


def new_create_Dicom_From_Nothing(STL_Path,ID=None,DICOM_Path = None,New_Path = None):
    f = open(STL_Path, "rb")

    if(DICOM_Path != None):
        DS = pydicom.dcmread(DICOM_Path)
        for data_element in DS:
            del DS[data_element.tag]
    else:
        DS = pydicom.Dataset()
        preamble = np.zeros(128, dtype=np.uint8)
        preamble[:4] = [68,73,67,77]
        DS.preamble = preamble.tobytes()
    if(ID==None):
        NID = random.randint(100000,999999)
    else:
        NID = ID

    if(New_Path == None):
        NP_sub = f.name
        NP = NP_sub.replace(NP_sub[len(NP_sub) - 3:], "dcm")
    else:
        NP = New_Path

    General_id_frame_of_reference = uid.generate_uid()
    # -------------------------------- Patient --------------------------------
    DS.add(DataElement(0x00100010, "PN", ''))
    DS.add(DataElement(0x00100020, "LO", "TG"+ str(NID)))
    DS.add(DataElement(0x00100030, "DA", "20000101"))
    DS.add(DataElement(0x00100040, "CS", "M"))
    # -------------------------------- Patient --------------------------------

    # -------------------------------- GeneralStudy --------------------------------
    DS.add(DataElement((0x0020, 0x0010), 'SH', str(753951)))
    DS.add(DataElement(0x00080020, "DA", date.today().strftime("%Y%m%d")))
    DS.add(DataElement(0x00080030, "TM", datetime.now().strftime("%H%M%S.%f")))
    DS.add(DataElement((0x0020, 0x000D), 'UI', uid.generate_uid()))
    DS.add(DataElement((0x0008, 0x0050), 'SH', ''))
    DS.add(DataElement((0x0008, 0x0090), 'PN', ''))
    # -------------------------------- GeneralStudy --------------------------------

    DS.add(DataElement(0x00080023, "DA", date.today().strftime("%Y%m%d")))

    DS.add(DataElement(0x0008002A, "DT", datetime.now().strftime("%Y%m%d%H%M%S.%f")))

    DS.add(DataElement(0x00080033, "TM", datetime.now().strftime("%H%M%S.%f")))

    DS.add(DataElement(0x00200013, "IS", str(1)))

    DS.add(DataElement(0x00280301, "CS", "NO"))

    DS.add(DataElement(0x0040A043, "SQ", None))

    DS.add(DataElement(0x00420010, "ST", str(os.path.basename(f.name)).split(".")[0]))
    f_data = f.read()

    DS.add(DataElement((0x0042, 0x0011), 'OB', f_data))

    DS.add(DataElement((0x0042, 0x0012), 'LO', "model/stl"))
    # -------------------------------- Encapsuled Document --------------------------------
    # --- others
    DS.add(DataElement((0x0008, 0x0070), 'LO', "Thibault Gregoir"))
    DS.add(DataElement((0x0008, 0x1090), 'LO', "Master Thesis Programs"))
    DS.add(DataElement((0x0018, 0x1000), 'LO', "753951"))
    DS.add(DataElement((0x0018, 0x1020), 'LO', "2"))




    DS.add(DataElement(0x00080060, 'CS', 'M3D'))
    # --- others
    DS.add(DataElement((0x0020, 0x000E), 'UI', uid.generate_uid()))
    DS.add(DataElement((0x0020, 0x0011), 'IS', str(1)))
    # -------------------------------- Frame Of Reference --------------------------------
    DS.add(DataElement((0x0020, 0x0052), 'UI', General_id_frame_of_reference))

    DS.add(DataElement((0x0020, 0x1040), 'LO', ''))
    # -------------------------------- Frame Of Reference --------------------------------

    # -------------------------------- Manufacturing 3D Model --------------------------------
    new_subsequence = pydicom.Sequence()
    new_item = pydicom.dataset.Dataset()
    new_item.add(DataElement((0x0008, 0x0100), 'SH', "mm"))
    new_item.add(DataElement((0x0008, 0x0102), 'SH', "UCUM"))
    new_item.add(DataElement((0x0008, 0x0103), 'SH', "1.5"))
    new_item.add(DataElement((0x0008, 0x0104), 'LO', "STL file constructed from Dicom Rt-Struct"))

    new_subsequence.append(new_item)
    DS.add(DataElement((0x0040, 0x08EA), 'SQ', new_subsequence))
    # -------------------------------- Manufacturing 3D Model --------------------------------
    DS.SOPClassUID = uid.EncapsulatedSTLStorage
    DS.SOPInstanceUID = uid.generate_uid()


    if(DICOM_Path== None):
        DS.file_meta = pydicom.dataset.FileMetaDataset()
        DS.file_meta.ImplementationClassUID = '1.0.0.0.0.0.22213.1.143'
        DS.file_meta.ImplementationVersionName = '0.5'
        DS.file_meta.add_new((0x0002, 0x0000), "UL", 100)
        DS.file_meta.add_new((0x0002, 0x0001), "OB", b'\x00\x01')
    DS.file_meta.MediaStorageSOPClassUID = DS.SOPClassUID
    DS.file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID
    DS.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian

    DS.is_little_endian = True
    DS.is_implicit_VR = True
    DS.save_as(NP)
