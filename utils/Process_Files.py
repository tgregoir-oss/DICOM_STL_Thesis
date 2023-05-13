from scipy.ndimage import gaussian_filter
import nibabel as nib
import utils.Utils as Utils
from utils.Process_Dicom import *
import dicom2nifti
import gzip
import shutil
from utils.Marching_Cubes import *
import numpy as np
import os
import time


"""
fichier : 1 = ascii | 0 = Binary
"""


def process_DICOM_RT_Strcut(path, definition=256, save_external_stl=2, Smoothing=0, fichier=0):
    start = time.time()
    DC = pydicom.dcmread(path)
    contours = DC[0x3006, 0x0039]
    ROI_Sequence = DC[0x3006, 0x0020]
    for index in range(len(contours.value)):
        print(f'{index / len(contours.value) * 100}% done \t| Execution Time : {time.time() - start:.2}s')

        one_model = contours[index][0x3006, 0x0040]

        if (ROI_Sequence[index][0x3006, 0x0026].is_empty):
            name = str(index)
        else:
            name = str(ROI_Sequence[index][0x3006, 0x0026].value)

        one_model_contours, offset = retrieve_Contours(one_model)

        # On va transformer chaque contour en 1 image carrée de longueur definition. Le résultat sera qu'on aura des 1 à l'endroit ou se place le modèle

        model_bitmap, contours_z = Utils.create_bitmap(one_model_contours, offset, definition)

        for i in range(len(model_bitmap)):
            if (len(model_bitmap[i]) > 1):
                sub_table = model_bitmap[i][0]
                for j in range(1, len(model_bitmap[i])):
                    sub_table = sub_table ^ model_bitmap[i][j]
                model_bitmap[i] = np.pad(sub_table.T, pad_width=1, mode='constant', constant_values=0)
            else:
                model_bitmap[i] = np.pad(model_bitmap[i][0].T, pad_width=1, mode='constant', constant_values=0)
        # ---------------------- Step 3 ----------------------

        # ---------------------- Step 4 ----------------------
        # On ajoute une couche au dessus et en dessous pour avoir des modèles complets
        model_bitmap.insert(0, np.zeros((definition + 2, definition + 2)))
        model_bitmap.insert(len(model_bitmap), np.zeros((definition + 2, definition + 2)))
        model_bitmap.reverse()

        contours_z.insert(0, contours_z[0] + abs(contours_z[0] - contours_z[1]))
        contours_z.insert(len(contours_z), contours_z[len(contours_z) - 1] - abs(contours_z[0] - contours_z[1]))

        contours_z.reverse()
        # ---------------------- Step 4 ----------------------
        #if (Smoothing == 1 or Smoothing == 3):
        if (Smoothing == 0):
            model_bitmap = gaussian_filter(model_bitmap, sigma=[3, 3, 2], mode='constant', cval=0.0)

        if fichier == 1:
            STL_path = name + ".stl"
            f = open(STL_path, "w")
        else:
            STL_path = name + "_b.stl"
            f = open(STL_path, "wb")
        marching_cubes_offset(model_bitmap, f, offset, contours_z, definition + 2, fichier)
        f.close()

        #if (Smoothing == 2 or Smoothing == 3):
        if (Smoothing == 0):
            Smooth_Mesh(STL_path, 0,fichier)
        if (save_external_stl == 1 or save_external_stl == 2):
            to_Dicom_STL_Encapsulated(path, STL_path)
    print(f'100% done \t| Total Execution Time : {time.time()-start:.2}s')

def process_Nifti_file(path, new_path=None, Smoothing=3, fichier=1):
    file = nib.load(path)
    data = file.get_fdata()

    contour_z = []
    model_bitmap = []

    for i in range(data.shape[2]):
        sub_image = data[:, :, i]

        contour_z.append(5 * i)
        model_bitmap.append(sub_image)

    model_bitmap.insert(0, np.zeros((data.shape[0], data.shape[1])))
    model_bitmap.append( np.zeros((data.shape[0], data.shape[1])))
    model_bitmap.reverse()

    contour_z.insert(0,  - contour_z[1])
    contour_z.append(contour_z[len(contour_z) - 1] - abs(contour_z[0] - contour_z[1]))
    contour_z.reverse()
    # model_bitmap = gaussian_filter(model_bitmap, sigma=[3,3,2], mode='constant',cval=0.0 )

    check = marching_cubes(model_bitmap, new_path, contour_z, fichier)

    if (check == True):
        if (Smoothing == 3):
            Smooth_Mesh(new_path, 0,fichier)
        return True

    return False


def check_dicom_series(input_path, start, end):
    files = os.listdir(input_path)
    dicom_files = [f for f in files if f.endswith(".dcm")]
    if (len(dicom_files) == 0):
        return False

    datasets = [pydicom.dcmread(os.path.join(input_path, f)) for f in dicom_files]
    for F in datasets:
        if F.Modality != "CT":
            print("One of this file is not a CT Dicom Scan")
            return False
    datasets = sorted(datasets, key=lambda x: x.InstanceNumber)
    if start <= 0 or start > len(dicom_files):
        start = 1
    if end <= 0 or end > len(dicom_files):
        end = len(dicom_files)
    if start >= end:
        print("error on start and end")
        return False

    position = 0
    last_check = start
    new_datasets = []

    while (last_check <= end):
        if (datasets[position].InstanceNumber == last_check):
            new_datasets.append(datasets[position])
            last_check += 1
            position += 1
        elif (datasets[position].InstanceNumber > last_check):
            print("Dicom Series incomplete")
            return False
        else:
            position += 1
    print("everything seems ok")

    dicom2nifti.convert_dicom.dicom_array_to_nifti(new_datasets, "test.nii.gz", reorient_nifti=True)

    process_folder_gz()

    process_folder_nii()
    return True


def process_nii_gz(path):
    os.makedirs("nii_folder/", exist_ok=True)
    splitted_path = path.split(".")

    output_path = "nii_folder/" + splitted_path[0].split("/")[1] + "." + splitted_path[1]

    with gzip.open(path, 'rb') as f_in:
        with open(output_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    List_file = os.listdir("nii_folder/")


def process_folder_nii():
    List_file = os.listdir("nii_folder/")
    print("we enter in process_folder_nii ")
    for i in List_file:
        execute("nii_folder/" + i)


def process_folder_gz():
    print("we enter in process folder function")
    List_file = os.listdir("gz_folder/")
    for i in List_file:
        process_nii_gz("gz_folder/" + i)


def check_path(input_path, start=0, end= inf):

    if (os.path.isdir(input_path)):
        print("c'est un dossier")
        check_dicom_series(input_path, start, end)
    elif (os.path.isfile(input_path)):
        splitted = input_path.split(".")
        p = len(splitted) - 1
        print(splitted)
        if (splitted[p] == "dcm"):
            ds = pydicom.dcmread(input_path)
            if(ds.Modality == "RTSTRUCT"):
                process_DICOM_RT_Strcut(input_path,definition=206,fichier=0)
            else:
                print("error c'est pas un dicom rt struct")
        elif (splitted[p] == "nii"):
            new_path = input_path.replace(input_path[len(input_path)-3:],"stl")
            process_Nifti_file(input_path,new_path= new_path)

        elif (splitted[p] == "gz" and splitted[p - 1] == "nii"):
            print("c'est un série de fichier nii")
            print(input_path)
            process_nii_gz(input_path)
        else:
            print("non connu")
    else:
        print("error")
        return False

def execute(path):
    Splitted_path = path.split(".")

    new_path = "stl_folder" +"/"+ str(Splitted_path[0].split("/")[1]) + ".stl"

    start = time.time()
    check = process_Nifti_file(path,new_path=new_path,fichier=0)

    end = time.time()
    elapsed = end - start
    if(check):
        print("\033[92mFile : {} Correctly created\033[00m ".format(new_path))
        print(f'\033[92mTemps d\'exécution : {elapsed:.2}s \033[00m ')
    else:
        print("\033[91mFile : {} Not created because the file didn't contain data to create STL file\033[00m".format(new_path))

