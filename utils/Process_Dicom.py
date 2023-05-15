import os.path

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

def create_Dicom_From_Nothing(STL_Path,ID):
    General_id_frame_of_reference = uid.generate_uid()
    DS = pydicom.Dataset()
    # -------------------------------- Patient --------------------------------
    DS.add(DataElement(0x00100010, "PN", ''))
    DS.add(DataElement(0x00100020, "LO", "TG"+ str(ID)))
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

    f = open(STL_Path,"rb")
    DS.add(DataElement(0x00420010, "ST", str(f.name).split(".")[0]))

    f_data = f.read()
    print(f.name)
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


    #DS.file_meta.MediaStorageSOPClassUID = uid.EncapsulatedSTLStorage
    #DS.file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID
    DS.file_meta = pydicom.dataset.FileMetaDataset()
    DS.file_meta.MediaStorageSOPClassUID = DS.SOPClassUID
    DS.file_meta.MediaStorageSOPInstanceUID = DS.SOPInstanceUID
    DS.file_meta.ImplementationClassUID = '1.0.0.0.0.0.22213.1.143'
    DS.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    DS.file_meta.ImplementationVersionName = '0.5'  # implementation version name
    DS.file_meta.SourceApplicationEntityTitle = 'POSDA'
    DS.file_meta.add_new((0x0002, 0x0000), "UL", 208)
    DS.file_meta.add_new((0x0002, 0x0001), "OB", b'\x00\x01')
    DS.is_little_endian = True
    DS.is_implicit_VR = True
    DS.save_as(str(f.name).split(".")[0] + ".dcm")


def new_create_Dicom_From_Nothing(STL_Path,ID=None,DICOM_Path = None,New_Path = None):
    f = open(STL_Path, "rb")

    if(DICOM_Path != None):
        DS = pydicom.dcmread(DICOM_Path)
        for data_element in DS:
            del DS[data_element.tag]
        print(DS)
    else:
        DS = pydicom.Dataset()
    if(ID==None):
        NID = random.randint(100000,999999)
    else:
        NID = ID

    if(New_Path == None):
        #NP = os.path.dirname(STL_Path) +"/" + os.path.basename(STL_Path)
        NP = str(f.name).split(".")[0] + ".dcm"
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

    DS.add(DataElement(0x00420010, "ST", str(f.name).split(".")[0]))

    f_data = f.read()
    print(f.name)
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


def to_Dicom_STL_Encapsulated(Dicom_Path, STL_Path):

    General_id_frame_of_reference = uid.generate_uid()
    dataset = [
        [0x0008, 0x1070],
        [0x0008, 0x1072],
        [0x0020, 0x0013],
        [0x3006, 0x0002],
        [0x3006, 0x0004],
        [0x3006, 0x0004],
        [0x3006, 0x0006],
        [0x3006, 0x0008],
        [0x3006, 0x0009],
        [0x3006, 0x0010],
        [0x3006, 0x0018],
        [0x3006, 0x0020],
        [0x3006, 0x0039],
        [0x3006, 0x0080],
        [0x300e, 0x0002],
        [0x300e, 0x0004],
        [0x300e, 0x0005],
        [0x300e, 0x0008],
        [0x0008, 0x1140],
        [0x0008, 0x114a],
        [0x0008, 0x2111],
        [0x0008, 0x2112],
        [0x0008, 0x9215],
        [0x0013, 0x0010],
        [0x0013, 0x1010],
        [0x0013, 0x1013],
        [0x0018, 0x0015],  # ce dernier peu être utile mais osef un peu puisque c'est un tag créé par des gens

        [0x0008, 0x0021],
        [0x0008, 0x0031],
        [0x0008, 0x0060],
        [0x0008, 0x103E],
        [0x0008, 0x103F],
        [0x0008, 0x1050],
        [0x0008, 0x1052],
        [0x0008, 0x1070],
        [0x0008, 0x1072],
        [0x0008, 0x1111],
        [0x0008, 0x1250],
        [0x0010, 0x2210],
        [0x0018, 0x0015],
        [0x0018, 0x1030],
        [0x0018, 0x5100],
        [0x0018, 0x990C],
        [0x0018, 0x990D],
        [0x0020, 0x0060],
        [0x0028, 0x0108],
        [0x0028, 0x0109],
        [0x0040, 0x0244],
        [0x0040, 0x0245],
        [0x0040, 0x0250],
        [0x0040, 0x0251],
        [0x0040, 0x0253],
        [0x0040, 0x0254],
        [0x0040, 0x0260],
        [0x0040, 0x0275],
        [0x0040, 0x0280],

        [0x0008, 0x0008],
        [0x0008, 0x0022],
        [0x0008, 0x0023],
        [0x0008, 0x002A],
        [0x0008, 0x0032],
        [0x0008, 0x0033],
        [0x0008, 0x2218],
        [0x0008, 0x2228],
        [0x0008, 0x3010],
        [0x0020, 0x0012],
        [0x0020, 0x0013],
        [0x0020, 0x0020],
        [0x0020, 0x0062],
        [0x0020, 0x1002],
        [0x0020, 0x4000],
        [0x0028, 0x0300],
        [0x0028, 0x0301],
        [0x0028, 0x0302],
        [0x0028, 0x2110],
        [0x0028, 0x2112],
        [0x0028, 0x2114],
        [0x0040, 0x9096],
        [0x0088, 0x0200],
        [0x2050, 0x0020],

        [0x0008, 0x1140],
        [0x0008, 0x114A],
        [0x0008, 0x2111],
        [0x0008, 0x2112],
        [0x0008, 0x9215],
        [0x0042, 0x0013],

        [0x0018, 0x0050],
        [0x0020, 0x0032],
        [0x0020, 0x0037],
        [0x0020, 0x1041],
        [0x0028, 0x0030],

        [0x0028, 0x0002],
        [0x0028, 0x0004],
        [0x0028, 0x0006],
        [0x0028, 0x0010],
        [0x0028, 0x0011],
        [0x0028, 0x0034],
        [0x0028, 0x0100],
        [0x0028, 0x0101],
        [0x0028, 0x0102],
        [0x0028, 0x0103],
        [0x0028, 0x0106],
        [0x0028, 0x0107],
        [0x0028, 0x0121],
        [0x0028, 0x1101],
        [0x0028, 0x1102],
        [0x0028, 0x1103],
        [0x0028, 0x1201],
        [0x0028, 0x1202],
        [0x0028, 0x1203],
        [0x0028, 0x2000],
        [0x0028, 0x2002],
        [0x0028, 0x7FE0],
        [0x7FE0, 0x0001],
        [0x7FE0, 0x0002],
        [0x7FE0, 0x0010],

        [0x0018, 0x0010],
        [0x0018, 0x0012],
        [0x0018, 0x0014],
        [0x0018, 0x1040],
        [0x0018, 0x1041],
        [0x0018, 0x1042],
        [0x0018, 0x1043],
        [0x0018, 0x1044],
        [0x0018, 0x1046],
        [0x0018, 0x1047],
        [0x0018, 0x1048],
        [0x0018, 0x1049],

        [0x0050, 0x0010],

        [0x0040, 0x0512],
        [0x0040, 0x0513],
        [0x0040, 0x0515],
        [0x0040, 0x0518],
        [0x0040, 0x051A],
        [0x0040, 0x0520],
        [0x0040, 0x0560],

        [0x0008, 0x0008],
        [0x0008, 0x2218],
        [0x0008, 0x2228],
        [0x0018, 0x0022],
        [0x0018, 0x0060],
        [0x0018, 0x0090],
        [0x0018, 0x1100],
        [0x0018, 0x1110],
        [0x0018, 0x1111],
        [0x0018, 0x1120],
        [0x0018, 0x1130],
        [0x0018, 0x1140],
        [0x0018, 0x1150],
        [0x0018, 0x1151],
        [0x0018, 0x1152],
        [0x0018, 0x1153],
        [0x0018, 0x115E],
        [0x0018, 0x1160],
        [0x0018, 0x1170],
        [0x0018, 0x1190],
        [0x0018, 0x1210],
        [0x0018, 0x1271],
        [0x0018, 0x1272],
        [0x0018, 0x9305],
        [0x0018, 0x9306],
        [0x0018, 0x9307],
        [0x0018, 0x9309],
        [0x0018, 0x9310],
        [0x0018, 0x9311],
        [0x0018, 0x9313],
        [0x0018, 0x9318],
        [0x0018, 0x9323],
        [0x0018, 0x9324],
        [0x0018, 0x9345],
        [0x0018, 0x9346],
        [0x0018, 0x9351],
        [0x0018, 0x9352],
        [0x0018, 0x9353],
        [0x0018, 0x9360],
        [0x0018, 0x9361],
        [0x0020, 0x0012],
        [0x0028, 0x0002],
        [0x0028, 0x0004],
        [0x0028, 0x0100],
        [0x0028, 0x0101],
        [0x0028, 0x0102],
        [0x0028, 0x1052],
        [0x0028, 0x1053],
        [0x0028, 0x1054],
        [0x0054, 0x0220],
        [0x0054, 0x0500],
        [0x300A, 0x0122],
        [0x300A, 0x0129],
        [0x300A, 0x012A],
        [0x300A, 0x012C],
        [0x300A, 0x0140],
        [0x300A, 0x0144],

        [0x0018, 0x9362],
        [0x0018, 0x9363],
        [0x0018, 0x9364],

        [0x0028, 0x1050],
        [0x0028, 0x1051],
        [0x0028, 0x1055],
        [0x0028, 0x1056],
        [0x0028, 0x3010]
    ]

    ds = pydicom.dcmread(Dicom_Path)

    for T in dataset:
        if T in ds:
            del ds[T[0], T[1]]

    # -------------------------------- Encapsuled Document --------------------------------
    if ([0x0008, 0x0023] in ds):
        ds[0x0008, 0x0023].value = date.today().strftime("%Y%m%d")
    else:
        ds.add(DataElement(0x00080023, "DA", date.today().strftime("%Y%m%d")))

    if ([0x0008, 0x002A] in ds):
        if(ds[0x0008, 0x002A].value == ''):
            ds[0x0008, 0x002A].value = datetime.now().strftime("%Y%m%d%H%M%S.%f")
    else:
        ds.add(DataElement(0x0008002A, "DT", datetime.now().strftime("%Y%m%d%H%M%S.%f")))

    if ([0x0008, 0x0030] in ds):
        if(ds[0x0008, 0x0030].value == ''):
            ds[0x0008, 0x0030].value = datetime.now().strftime("%H%M%S.%f")
    else:
        ds.add(DataElement(0x00080030, "TM", datetime.now().strftime("%H%M%S.%f")))

    if ([0x0008, 0x0033] in ds):
        ds[0x0008, 0x0033].value = datetime.now().strftime("%H%M%S.%f")
    else:
        ds.add(DataElement(0x00080033, "TM", datetime.now().strftime("%H%M%S.%f")))

    if ([0x0020, 0x0013] in ds):
        ds[0x0020, 0x0013].value = str(1)
    else:
        ds.add(DataElement(0x00200013, "IS", str(1)))

    if ([0x0028, 0x0301] in ds):
        ds[0x0028, 0x0301].value = 'NO'
    else:
        ds.add(DataElement(0x00280301, "CS", "NO"))

    # to modify if j'ai la motiv
    if ([0x0040, 0xA043] in ds):
        ds[0x0040, 0xA043].value = None
    else:
        ds.add(DataElement(0x0040A043, "SQ", None))

    f = open(STL_Path,"rb")
    if ([0x0042, 0x0010] in ds):
        ds[0x0042, 0x0010].value = str(f.name).split(".")[0]
    else:
        ds.add(DataElement(0x00420010, "ST", str(f.name).split(".")[0]))

    f_data = f.read()
    if ([0x0042, 0x0011] in ds):
        ds[0x0042, 0x0011].value = f_data
    else:
        ds.add(DataElement((0x0042, 0x0011), 'OB', f_data))

    if ([0x0042, 0x0012] in ds):
        ds[0x0042, 0x0012].value = "model/stl"
    else:
        ds.add(DataElement((0x0042, 0x0012), 'LO', "model/stl"))
    # -------------------------------- Encapsuled Document --------------------------------
    # --- others
    if ([0x0018, 0x1000] in ds):
        ds[0x0018, 0x1000].value = str(753951)
    else:
        ds.add(DataElement((0x0018, 0x1000), 'LO', str(753951)))
    if ([0x0018, 0x1020] in ds):
        ds[0x0018, 0x1020].value = str(1.5)
    else:
        ds.add(DataElement((0x0018, 0x1020), 'LO', str(1.5)))

    if ([0x0020, 0x0010] in ds):
        ds[0x0020, 0x0010].value = str(753951)
    else:
        ds.add(DataElement((0x0020, 0x0010), 'SH', str(753951)))
    if ([0x0008, 0x0060] in ds):
        del ds[0x0008, 0x0060]

    ds.add(DataElement(0x00080060, 'CS', 'M3D'))
    # --- others
    if ([0x0020, 0x0011] in ds):
        ds[0x0020, 0x0011].value = str(1)
    else:
        ds.add(DataElement((0x0020, 0x0011), 'IS', str(1)))
    # -------------------------------- Frame Of Reference --------------------------------
    if ([0x0020, 0x0052] in ds):
        ds[0x0020, 0x0052].value = General_id_frame_of_reference
    else:
        ds.add(DataElement((0x0020, 0x0052), 'UI', General_id_frame_of_reference))

    if ([0x0020, 0x1040] in ds):
        ds[0x0020, 0x1040].value = None
    else:
        ds.add(DataElement((0x0020, 0x1040), 'UI', None))
    # -------------------------------- Frame Of Reference --------------------------------

    # -------------------------------- Manufacturing 3D Model --------------------------------
    new_subsequence = pydicom.Sequence()
    new_item = pydicom.dataset.Dataset()
    new_item.add(DataElement((0x0008, 0x0100), 'SH', "mm"))
    new_item.add(DataElement((0x0008, 0x0102), 'SH', "UCUM"))
    new_item.add(DataElement((0x0008, 0x0103), 'SH', "1.5"))
    new_item.add(DataElement((0x0008, 0x0104), 'LO', "STL file constructed from Dicom Rt-Struct"))

    new_subsequence.append(new_item)
    ds.add(DataElement((0x0040, 0x08EA), 'SQ', new_subsequence))
    # -------------------------------- Manufacturing 3D Model --------------------------------
    ds.file_meta.MediaStorageSOPClassUID = uid.EncapsulatedSTLStorage
    ds.file_meta.MediaStorageSOPInstanceUID = uid.generate_uid()
    ds.SOPClassUID = uid.EncapsulatedSTLStorage
    ds.SOPInstanceUID = ds.file_meta.MediaStorageSOPInstanceUID

    ds.save_as(str(f.name).split(".")[0] + ".dcm")


