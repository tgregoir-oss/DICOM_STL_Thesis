from utils.Utils import *
from utils.Point import *
from utils.Triangle import *


def marching_cubes_offset(bitmap, f, GO, z_values, size, fichier):
    triangle_queue = []

    for L in range(len(bitmap)-1):
        for i in range(len(bitmap[0])-1):
            for j in range(len(bitmap[0][0])-1):
                look_up = str(treshold(bitmap[L + 1][i+1][j], "binary"))
                look_up = str(treshold(bitmap[L + 1][i + 1][j + 1], "binary")) + look_up
                look_up = str(treshold(bitmap[L + 1][i][j+1], "binary")) + look_up
                look_up = str(treshold(bitmap[L + 1][i][j], "binary")) + look_up

                look_up = str(treshold(bitmap[L][i+1][j], "binary")) + look_up
                look_up = str(treshold(bitmap[L][i + 1][j + 1], "binary")) + look_up
                look_up = str(treshold(bitmap[L][i][j+1], "binary")) + look_up
                look_up = str(treshold(bitmap[L][i][j], "binary")) + look_up

                indice_look_up = int("0b"+look_up, 2)
                situation = table[indice_look_up]

                if(situation[0] != -1):
                    P = 0
                    while(P < 5):
                        if(situation[3*P] != -1):
                            point_a = make_point_offset(i, j, L, situation[3 * P + 0], GO, z_values, size)
                            point_b = make_point_offset(i, j, L, situation[3 * P + 1], GO, z_values, size)
                            point_c = make_point_offset(i, j, L, situation[3 * P + 2], GO, z_values, size)
                            triangle_queue.append(Triangle(point_a, point_b, point_c))
                            P+=1
                        else:
                            P = 50
    write_file(triangle_queue,f, fichier)

def marching_cubes(bitmap, new_path, z_values,fichier):
    triangle_queue = []

    for L in range(len(bitmap)-1):
        if(bitmap[L].any() or bitmap[L+1].any()):
            for i in range(len(bitmap[0])-1):
                for j in range(len(bitmap[0][0])-1):
                    #On itère sur chaque cube
                    #On récupère les points pour savoir lesquels appartiennent au modèle ou non
                    #on regarde alors dans le modèle les points dont on a besoin, on les créér puis on stock/écrit les triangles ainsi formé
                    look_up = str(treshold(bitmap[L + 1][i+1][j],"binary"))
                    look_up = str(treshold(bitmap[L + 1][i + 1][j + 1], "binary")) + look_up
                    look_up = str(treshold(bitmap[L + 1][i][j+1], "binary")) + look_up
                    look_up = str(treshold(bitmap[L + 1][i][j], "binary")) + look_up

                    look_up = str(treshold(bitmap[L][i+1][j], "binary")) + look_up
                    look_up = str(treshold(bitmap[L][i + 1][j + 1], "binary")) + look_up
                    look_up = str(treshold(bitmap[L][i][j+1], "binary")) + look_up
                    look_up = str(treshold(bitmap[L][i][j], "binary")) + look_up

                    indice_look_up = int("0b"+look_up,2)
                    situation = table[indice_look_up]

                    if(situation[0] != -1):
                        P = 0
                        while(P <5):
                            if(situation[3*P] != -1):
                                point_a = make_point(i, j, L, situation[3 * P + 0], z_values)
                                point_b = make_point(i, j, L, situation[3 * P + 1], z_values)
                                point_c = make_point(i, j, L, situation[3 * P + 2], z_values)
                                triangle_queue.append(Triangle(point_a, point_b, point_c))
                                P+=1
                            else:
                                P = 50
    if(len(triangle_queue) != 0):
        if(fichier==0):
            f = open(new_path, "wb")
            f.write(struct.pack('80s', b'nothing'))
            f.write(struct.pack('I',len(triangle_queue)))
            for T in triangle_queue:
                write_triangle_binary(T.a, T.b, T.c, f)
            f.close()
        else:
            f = open(new_path, "w")
            f.write("solid test\n")
            for T in triangle_queue:
                write_triangle_ascii(T.a,T.b,T.c,f)
            f.write("endsolid")
            f.close()
        return True
    return False
