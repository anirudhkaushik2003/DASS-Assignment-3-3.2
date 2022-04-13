import os
import numpy as np
import config as conf

###### WORLD DATA LOADER #####################
rows, cols = os.popen("stty size", "r").read().split()
height = int(rows) - conf.BUFFER_DOWN
width = int(cols) - conf.BUFFER_RIGHT


def gen_new_level1():
    data1 = np.array(
        [[[0, True] for j in range(width * 2)] for i in range(height)],
        dtype="object",
    )
    
    data1[0][0] = [4, True]
    data1[0][50] = [4, True]
    data1[0][100] = [4, True]
    data1[0][150] = [4, True]
    data1[0][200] = [4, True]
    data1[0][250] = [4, True]
    # town hall
    data1[11][90] = [3, True]
    # turrets
    # data1[14][68] = [6, True]
    # data1[17][158] = [6, True]

    # data1[12][30] = [9,True]
    # data1[12][230] = [9,True]


    # buildings
    data1[17][50] = [2, True]
    data1[27][50] = [2, True]
    data1[24][68] = [2, True]
    data1[24][208] = [2, True]
    data1[11][208] = [2, True]

    # spwn points
    data1[conf.SPAWN1_Y][conf.SPAWN1_X] = [7, False]
    data1[conf.SPAWN2_Y][conf.SPAWN2_X] = [7, False]
    data1[conf.SPAWN3_Y][conf.SPAWN3_X] = [7, False]

    # place walls
    for i in range(10, height - 12):
        data1[i][48] = [8, True]
    for i in range(48, 148):
        data1[height - 12][i] = [8, True]
    for i in range(25, height - 11):
        data1[i][148] = [8, True]

    for i in range(148, 200):
        data1[25][i] = [8, True]
    for i in range(10, 26):
        data1[i][200] = [8, True]


    last_j = 0
    for i in range(0, height, 10):
        for j in range(301, width * 2 - 1, 20):
            data1[i][j] = [1, False]
            last_j = j

    for i in range(0, height, 10):
        for j in range(last_j, width * 2, 20):
            data1[i][j] = [1, True]


    for i in range(height - 2, height):
        for j in range(width * 2):
            data1[i][j] = [5, True]
    for i in range(1, height - 2):
        data1[i][0] = [5, True]
    
    return data1


def gen_new_level2():
    data2 = np.array(
        [[[0, True] for j in range(width * 2)] for i in range(height)],
        dtype="object",
    )
    
    data2[0][0] = [4, True]
    data2[0][50] = [4, True]
    data2[0][100] = [4, True]
    data2[0][150] = [4, True]
    data2[0][200] = [4, True]
    data2[0][250] = [4, True]
    # town hall
    data2[11][90] = [3, True]
    # turrets
    data2[14][68] = [6, True]
    data2[17][158] = [6, True]
    data2[12][30] = [9,True]
    data2[12][230] = [9,True]


    # buildings
    data2[17][50] = [2, True]
    data2[27][50] = [2, True]
    data2[24][68] = [2, True]
    data2[24][208] = [2, True]
    data2[11][208] = [2, True]

    # spwn points
    data2[conf.SPAWN1_Y][conf.SPAWN1_X] = [7, False]
    data2[conf.SPAWN2_Y][conf.SPAWN2_X] = [7, False]
    data2[conf.SPAWN3_Y][conf.SPAWN3_X] = [7, False]

    # place walls
    for i in range(10, height - 12):
        data2[i][48] = [8, True]
    for i in range(48, 148):
        data2[height - 12][i] = [8, True]
    for i in range(25, height - 11):
        data2[i][148] = [8, True]

    for i in range(148, 200):
        data2[25][i] = [8, True]
    for i in range(10, 26):
        data2[i][200] = [8, True]


    last_j = 0
    for i in range(0, height, 10):
        for j in range(301, width * 2 - 1, 20):
            data2[i][j] = [1, False]
            last_j = j

    for i in range(0, height, 10):
        for j in range(last_j, width * 2, 20):
            data2[i][j] = [1, True]


    for i in range(height - 2, height):
        for j in range(width * 2):
            data2[i][j] = [5, True]
    for i in range(1, height - 2):
        data2[i][0] = [5, True]
    
    return data2

def gen_new_level3():
    data3 = np.array(
        [[[0, True] for j in range(width * 2)] for i in range(height)],
        dtype="object",
    )
    
    data3[0][0] = [4, True]
    data3[0][50] = [4, True]
    data3[0][100] = [4, True]
    data3[0][150] = [4, True]
    data3[0][200] = [4, True]
    data3[0][250] = [4, True]
    # town hall
    data3[11][90] = [3, True]
    # turrets
    # data3[14][68] = [6, True]
    # data3[17][158] = [6, True]

    # data3[12][30] = [9,True]
    # data3[12][230] = [9,True]


    # buildings
    data3[17][50] = [2, True]
    data3[27][50] = [2, True]
    data3[24][68] = [2, True]
    data3[24][208] = [2, True]
    data3[11][208] = [2, True]

    # spwn points
    data3[conf.SPAWN1_Y][conf.SPAWN1_X] = [7, False]
    data3[conf.SPAWN2_Y][conf.SPAWN2_X] = [7, False]
    data3[conf.SPAWN3_Y][conf.SPAWN3_X] = [7, False]

    # place walls
    for i in range(10, height - 12):
        data3[i][48] = [8, True]
    for i in range(48, 148):
        data3[height - 12][i] = [8, True]
    for i in range(25, height - 11):
        data3[i][148] = [8, True]

    for i in range(148, 200):
        data3[25][i] = [8, True]
    for i in range(10, 26):
        data3[i][200] = [8, True]


    last_j = 0
    for i in range(0, height, 10):
        for j in range(301, width * 2 - 1, 20):
            data3[i][j] = [1, False]
            last_j = j

    for i in range(0, height, 10):
        for j in range(last_j, width * 2, 20):
            data3[i][j] = [1, True]


    for i in range(height - 2, height):
        for j in range(width * 2):
            data3[i][j] = [5, True]
    for i in range(1, height - 2):
        data3[i][0] = [5, True]
    
    return data3
#############################################
data1 = gen_new_level1()
data2 = gen_new_level2()
data3 = gen_new_level3()




