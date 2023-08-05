colours = ['B','R','G','Y','P','C']
pegs = 5
codes = []
code = []
for i in range(0,pegs):
    code.append(0)


def find_groups(colours):
    code = colours.copy()
    code.sort()
    groupings = []
    temp = code[0]
    groupings.append(0)
    index = 0
    for num in code:
        if num != temp:
            index  += 1
            groupings.append(1)
            temp = num
        else:
            groupings[index] += 1
    groupings.sort()
    return groupings

for i in range(0, len(code)):
    code[0] += 1
    print(code)
    print(find_groups(code))    

