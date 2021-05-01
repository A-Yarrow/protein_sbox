#
import sys
import csv
infile = sys.argv[1]
targeted = []
new_library = []
with open('POL6-144-highly-targeted.csv', 'r') as csvfile:
    reader= csv.reader(csvfile)
    for i in reader:
        for j in i:
            targeted.append(j[1:])
print (targeted)
    
with open(infile, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for i in reader:
        for j in i:
            new_library.append(j)
print (new_library)
for i in new_library:
    if i in targeted:
        print('This residue has been targted:'+' '+i)

         
        
    
    
    