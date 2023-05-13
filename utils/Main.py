import random
import time
from Process_Files import *
path = "C:/Users/Thibault Gregoir/Documents/QX Memoire/Exemple DICOM/manifest-1666003711984/Pancreatic-CT-CBCT-SEG/Pancreas-CT-CB_001/07-06-2012-NA-PANCREAS-59677/1.000000-BSPCLLLRROISDPC-19315/1-1.dcm"
origin = "C:/Users/Thibault Gregoir/Documents/QX Memoire/Exemple DICOM/"
path2 = "manifest-1669628691361/LCTSC/LCTSC-Test-S1-101/03-03-2004-NA-NA-08186/1.000000-NA-56597/1-1.dcm"
path3 = "manifest-1669629168482/Soft-tissue-Sarcoma/STS_001/09-07-2000-NA-PET CT-63929/1.000000-RTstructCT-77278/1-1.dcm"
#extend = origin + "manifest-1598890146597/NSCLC-Radiomics-Interobserver1/interobs05/02-18-2019-NA-CT-90318/1.000000-ARIA RadOnc Structure Sets-55318/1-1.dcm"

extend = origin + path3
"""
start = time.time()
check_path(path)
process_DICOM_RT_Strcut(path, definition=206, fichier=0)

end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.2}s')
"""

path4 = "manifest-1666003711984/Pancreatic-CT-CBCT-SEG/Pancreas-CT-CB_001/07-06-2012-NA-PANCREAS-59677/56094.000000-Aligned resampled CB02-39781/1-001.dcm"

#to_Dicom_STL_Encapsulated(origin + path4,"oui.stl")

new_create_Dicom_From_Nothing("ROI_b.stl",random.randint(100000,999999),origin+path4)

DS = pydicom.dcmread("ROI_b.dcm")
print(DS)
