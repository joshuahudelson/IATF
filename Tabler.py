import matplotlib.pyplot as plt
from Feedback_Multi_Run import Feedback_Multi_Run
import numpy as np



def Tabler_Num_Loops(num_elems_low, num_elems_high, exp_low, exp_high, exp_step,
           num_runs, num_iters, max_value):

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

    for exp in np.arange(exp_low, exp_high, exp_step):

        row_labels.append(str(exp))

        num_unique_loops.append([])
        avg_len_loop.append([])
        std_loop.append([])
        len_unique_lengths.append([])
        avg_len_pre_loop.append([])
        std_pre_loop.append([])
        did_it_loop.append([])


        for num_elem in range(num_elems_low, num_elems_high):
            
            col_labels.append(str(num_elem))

            result = Feedback_Multi_Run(num_elem, exp, num_runs, num_iters, max_value=max_value)
            result.run_it()
            
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

    list_of_titles = ['Number of Unique Loops', 'Average Length of Loop',
                      'Standard Deviation of Length of Loop',
                      'Number of Unique Loop Lengths',
                      'Average Length of Pre-Loop',
                      'Standard Deviation of Length of Pre-Loop',
                      'Did It Loop?']

    for i in range(7):
        temp_exp = exp_low
        textfile = open(str(i) + ' - ' + str(list_of_titles[i]), 'w')
        textfile.write(list_of_titles[i])
        textfile.write('\n')
        textfile.write('\t\t\t\t\t\t\t Number of Elements \n\n')
        textfile.write('Exponent \t')
        for j in range(num_elems_low, num_elems_high):
            textfile.write(str(j) + '\t')
        textfile.write('\n')   
        for row in list_of_data[i]:
            textfile.write('\n')
            textfile.write(str(temp_exp) + '\t\t')
            temp_exp += exp_step
            for item in row:
                textfile.write(str(item) + '\t')
            textfile.write('\n')
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
    num_elem_high = 10

    exp_low = 1
    exp_high = 12
    exp_step = 0.2

    num_runs = 200
    num_iters = 10000
    max_value = 10

    Tabler_Num_Loops(num_elem_low, num_elem_high, exp_low, exp_high,
                     exp_step, num_runs, num_iters, max_value)


if __name__ == '__main__':
    run_test()

