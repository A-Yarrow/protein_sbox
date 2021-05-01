import sys


def convert_positions():
    file_in = sys.argv[1]

    infile = open(file_in, 'r')
    targeted = []
    for line in infile:
        line=line.rstrip()
        targeted.append(line)
        print(line)
    
    target = [str(int(i[1:4])) for i in targeted]
    #target2 = [str(x) for x in target]
    print ((('+').join(target)))

convert_positions()