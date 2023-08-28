import csv
import numpy as np
import matplotlib.pyplot as plt
import pprint
import sys

lookup = {"drone":8000}


if __name__ == "__main__":

    input_params = sys.argv[1:]

    print(input_params)
    with open(input_params[0]) as file:
        l = list(csv.reader(file))

    data = np.array(l) # now data holds the cnr range tables

    top_row = data[0,:]
    print(top_row)
    first_row = True
    for row in data:

        if first_row:           # skip the first row
            first_row = False
            continue
    

        # if top_row name contains a lookup key AND first element of row is greater than the lookup value
        # set CNR to ''

        for i in range(1, len(row)):
            for key in lookup.keys():
                if key in top_row[i] and float(row[0]) > lookup[key]:
                    row[i] = ''

    with open(input_params[1], 'w', newline ='') as output:
        writer = csv.writer(output)
        writer.writerows(data)

