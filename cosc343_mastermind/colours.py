indexs = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1],
            [0, 0, 0, 1, 1],
            [0, 0, 1, 1, 2],
            [0, 1, 1, 2, 2],
            [0, 1, 1, 2, 3],
            [0, 1, 2, 3, 4]
        ]
colours = ['B','R','G','Y','P','C']
codes = []
for i , code in enumerate(indexs):
    for j,  index in enumerate(code):
        codes[i][j]