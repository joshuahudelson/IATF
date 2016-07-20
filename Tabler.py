import matplotlib.pyplot as plt
from Feedback_Multi_Run import Feedback_Multi_Run
import numpy as np


"""
- number of unique loops
- number of differen loop lengths
- list of loop lengths
- average pre-loop length

"""

def Tabler_Num_Loops(num_elems_low, num_elems_high, exp_low, exp_high, exp_step,
           num_runs, num_iters, max_value):

    num_unique_loops = []
    unique_lengths = []
    len_unique_lengths = []
    avg_len_pre_loop = []

    col_labels=[]
    row_labels=[]

    for exp in np.arange(exp_low, exp_high, exp_step):

        row_labels.append(str(exp))

        num_unique_loops.append([])
        #unique_lengths.append([])   CHANGE TO AVG. LENGTH OF LOOP (and add a standard deviation?)
        len_unique_lengths.append([])
        avg_len_pre_loop.append([])  #ADD STANDARD DEVIAITON?

        for num_elem in range(num_elems_low, num_elems_high):
            
            col_labels.append(str(num_elem))

            result = Feedback_Multi_Run(num_elem, exp, num_runs, num_iters, max_value=max_value)
            result.run_it()
            
            num_unique_loops[len(num_unique_loops)-1].append(result.num_unique_loops)
            #unique_lengths[len(unique_lengths)-1].append(result.lens_unique_loops)
            len_unique_lengths[len(len_unique_lengths)-1].append(len(result.lens_unique_loops))
            avg_len_pre_loop[len(avg_len_pre_loop)-1].append(round(result.avg_len_pre_loop, 3))
            
    list_of_data = [num_unique_loops, #unique_lengths,
                    len_unique_lengths, avg_len_pre_loop]

    list_of_titles = ['Number of Unique Loops',
                      'Number of Unique Loop Lengths',
                      'Average Length of Pre-Loop']

    for i in range(3):
        temp_exp = exp_low
        textfile = open('File' + str(i), 'w')
        textfile.write(list_of_titles[i])
        textfile.write('\n')
        textfile.write('\n')
        textfile.write('\t\t')
        for j in range(num_elems_low, num_elems_high):
            textfile.write(str(j) + '\t\t')
        textfile.write('\n')   
        for row in list_of_data[i]:
            textfile.write('\n')
            textfile.write(str(temp_exp) + '\t\t')
            temp_exp += exp_step
            for item in row:
                textfile.write(str(item) + '\t\t')
    textfile.close()

                


"""
    for i in range(3):
        
        fig = plt.figure(i)
        ax=plt.gca()

        plt.plot()
        fig.suptitle(list_of_titles[i], fontsize=20)

        the_table = plt.table(cellText=list_of_data[i],
                  colWidths = [0.1]*20,
                  rowLabels=row_labels,
                  colLabels=col_labels,
                  loc='center')
        plt.text(12,3.4,'Table Title',size=8)

    plt.show()
"""

def run_test():
    num_elem_low = 4
    num_elem_high = 11

    exp_low = 1
    exp_high = 15
    exp_step = 0.25

    num_runs = 100
    num_iters = 10000
    max_value = 10

    Tabler_Num_Loops(num_elem_low, num_elem_high, exp_low, exp_high,
                     exp_step, num_runs, num_iters, max_value)


if __name__ == '__main__':
    run_test()

