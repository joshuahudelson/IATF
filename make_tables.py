import matplotlib.pyplot as plt
from Feedback_Multi_Run import Feedback_Multi_Run_with_Condition
import numpy as np
import os


def make_tables(num_elems_low, num_elems_high, exp_low, exp_high, exp_step,
           num_runs, num_iters, max_value, threshold):
    """ This function generates text files that collect the
        output of numerous Feedback_Multi_Runs, one for each
        combination of num_elems and exponent.  Each text
        file contains data for a different aspect of the
        output (the number of unique loops found, the
        average length of the pre-loop, etc.).  The data
        is displayed as a chart, with exponent values as the
        rows and num_elems values as the columns.
    """

    num_unique_loops = []
    unique_lengths = []
    len_unique_lengths = []
    avg_len_loop = []
    std_loop = []
    avg_len_pre_loop = []
    std_pre_loop = []
    did_it_loop = []

    col_labels=[]
    row_labels=[]

    temp_counter = 0

    list_of_titles = ['Number of Unique Loops', 'Average Length of Loop',
                      'Standard Deviation of Length of Loop',
                      'Number of Unique Loop Lengths',
                      'Average Length of Pre-Loop',
                      'Standard Deviation of Length of Pre-Loop',
                      'Did It Loop?']

    for exp in np.arange(exp_low, exp_high, exp_step):

        print("EXPONENT: " + str(exp))

        num_unique_loops.append([])
        avg_len_loop.append([])
        std_loop.append([])
        len_unique_lengths.append([])
        avg_len_pre_loop.append([])
        std_pre_loop.append([])
        did_it_loop.append([])

        for num_elem in range(num_elems_low, num_elems_high):

            print("Elem: " + str(num_elem))
            
            col_labels.append(str(num_elem))

            max_possible_runs = max_value**num_elem

            if num_runs > max_possible_runs:
                num_runs = max_possible_runs

            result = Feedback_Multi_Run_with_Condition(num_elem, exp, num_runs, num_iters, max_value=max_value)
            result.run_it(threshold)
            
            num_unique_loops[temp_counter].append(result.num_unique_loops)
            avg_len_loop[temp_counter].append(round(np.mean(result.lens_unique_loops), 3))
            std_loop[temp_counter].append(round(np.std(result.lens_unique_loops), 3))
            len_unique_lengths[temp_counter].append(len(result.lens_unique_loops))
            avg_len_pre_loop[temp_counter].append(round(result.avg_len_pre_loop, 3))
            std_pre_loop[temp_counter].append(round(np.std(result.lens_pre_loops), 3))
            did_it_loop[temp_counter].append(result.num_looping_vs_not[1])  # If it's 0, then all runs ended up looping

        temp_counter += 1

    list_of_data = [num_unique_loops, avg_len_loop, std_loop,
                    len_unique_lengths, avg_len_pre_loop, std_pre_loop, did_it_loop]

    folder_name = 'IATF_Run_Data/'

    try:
        os.stat(folder_name)
    except:
        os.mkdir(folder_name)

    for i in range(7):
        temp_exp = exp_low
        textfile = open(folder_name + str(i) + ' - ' + str(list_of_titles[i]), 'w')
        textfile.write(list_of_titles[i])
        textfile.write('\n')
        textfile.write('\t\t\t\t\t\t\t Number of Elements \n\n')
        textfile.write('Exponent \t')
        for j in range(num_elems_low, num_elems_high):
            textfile.write(str(j) + '\t')
        textfile.write('\n')   
        for row in list_of_data[i]:
            textfile.write('\n')
            textfile.write(str('%.1f' % temp_exp) + '\t\t')
            temp_exp += exp_step
            for item in row:
                textfile.write(str(item) + '\t')
            textfile.write('\n')
    textfile.close()


def run_test():
    num_elem_low = 4
    num_elem_high = 7

    exp_low = 1
    exp_high = 5
    exp_step = 0.2

    num_runs = 1000
    num_iters = 10000
    max_value = 10

    threshold = 0.001

    make_tables(num_elem_low, num_elem_high, exp_low, exp_high,
                    exp_step, num_runs, num_iters, max_value, 
                    threshold)


if __name__ == '__main__':
    run_test()

