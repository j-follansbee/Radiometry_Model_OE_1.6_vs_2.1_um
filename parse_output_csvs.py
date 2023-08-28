import csv
import glob
import sys
import numpy as np

if __name__ == "__main__":

    if len(sys.argv) == 3:
        input_argument = sys.argv[1]
        output_filename = sys.argv[2]
    else: 
        print("Must pass exactly two arguments to this script, an input file glob and an output filename.")

    input_file_list = glob.glob(input_argument)
    run_names = list()

    with open(output_filename, 'w', newline ='') as output:
        
        writer = csv.writer(output)
        x_dim = len(input_file_list)
        first_file = True
        data_index = 1

        for file in input_file_list: # loop through individual files

            # open a particular input file
            with open(file, 'r', newline='') as working_file:
                reader = csv.reader(working_file)
                
                if first_file:

                    # if the first file, set up the data array
                    data = list(reader)
                    first_file = False

                else:                   

                    # loop through remaining files. Append the last element of each row
                    # to the corresponding row in the main data array.
                    temp_data = list(reader)
                    ind = 0
                    for elt in temp_data:
                        data[ind].append(elt[1])
                        ind += 1

        writer.writerows(data) # write the combined output file to csv









