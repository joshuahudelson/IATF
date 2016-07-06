"""
Grapher.py
==========

Define Grapher class, with routines for graphing results from
Feedback_Multi_Runs.

"""

from Feedback_Multi_Run import Feedback_Multi_Run
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages



class Grapher:
    """ A class for using the data produced by
        Feedback_Multi_Runs to make graphs of
        starting points based on which loops they
        end up in.
    """

    def __init__(self, fmr_object):
        self.feedback_multi_runs = fmr_object

    def make_graphs(self, num_elems):
        """ For each unique loop, a figure is generated.
            Each subplot on the figure contains graphs of
            each start_point that has that subplot index as
            its initial driver.
            It also shows which element of each graph will
            be chosen by that driver on the first iteration
            (as a scatter-plot point).
        """
        pdf = PdfPages('multipage.pdf')

        temp_range = np.arange(num_elems)
        for i in self.feedback_multi_runs.list_of_runs:
            plt.figure(i['loop_number'])
            plt.subplot(num_elems, 1, i['start_point'][0])
            plt.plot(temp_range, i['start_point'][1:])
            plt.ylabel(str(i['start_point'][0]))
            temp_x_val = i['pre_loop'][1][0]
            plt.scatter(temp_x_val, i['start_point'][temp_x_val+1])

        for i in range(self.feedback_multi_runs.num_unique_loops-1):
            plt.figure(i)
            plt.savefig(pdf, format='pdf')

        plt.show()
        pdf.close()


def main(num_elems, exponent, num_runs, num_iters, max_value):
    """Run stuff."""
    result = Feedback_Multi_Run(num_elems, exponent, num_runs, num_iters,
                                max_value=max_value)
    result.run_it()

    new_grapher = Grapher(result)
    new_grapher.make_graphs(num_elems)



if __name__ == '__main__':
    main(6, 4, 50, 300, 10)
