from random import randint
from IATF_Runner import IATF_Runner
from IATF import IATF
import numpy as np
import matplotlib.pyplot as plt

from operator import itemgetter

class Feedback_Multi_Run:
    """ A class for generating multiple lists
        of output from IATF_Runners, each
        starting with a unique start_point,
        and consolidating the information from
        those lists.
    """

    def __init__(self,
                 num_elems,
                 exponent,
                 num_runs,
                 iters,
                 max_value=None
                ):
        """
        num_elems:    Int, the length of the array that will
                      become the differences and transfer_function
                      in the IATF object.
        exponent:     Int or float, the exponent to which
                      the differences in the IATF object
                      will be raised before the transfer_
                      function is calculated.
        num_runs:     Int, the number of different lists to be
                      produced (each by an IATF_Runner).
        iters:        Int, the number of iterations each IATF_
                      Runner should do before stopping.
        max_value:    Int, The maximum value any of the differences
                      in the start_point.
        ---
        list_of_runs: List, dicts containing all the state information
                      from each run (of an IATF_Runner), plus an int to
                      which loop in list_loops that run falls into.
        list_of_start_points:
                      List, numpy arrays describing the complete state
                      of an IATF object: current driver (int) and current
                      differences (ints) concatenated into numpy array.
        list_loops:   A list containing a list of each unique loop
                      encountered in list_of_runs.
        num_unique_loops:
                      The number of loops in list_loops.
        lengths_of_unique_loops:
                      A list of the lengths of the loops in
                      list_loops.
        lens_pre_loops:
                      A list of the lengths of the pre_loops,
                      one for each run in list_of_runs.
        avg_length_of_pre_loop:
                      The mean of lens_pre_loops.
        num_looping_vs_not:
                      List, ints describing how many runs
                      ended in a loop and how many didn't.
        ---
        starts_by_loop:
                      List, sublists of start_points collated
                      by which loop they end up in.
        starts_by_loop_driver:
                      List, same as starts_by_loop, but with
                      post-first-iteration driver as
                      index 0.
        starts_by_loop_driver_diffs:
                      List, same as starts_by_loop_driver but
                      with diffs for [2:] rather than cumsums.
        """

        self.num_elems = num_elems
        self.exponent = exponent
        self.num_runs = num_runs
        self.iters = iters

        if max_value == None:
            self.max_value = num_elems
        else:
            self.max_value = max_value

        self.list_of_runs = []

        self.list_of_start_points = []
        self.generate_unique_start_points()

        self.list_loops = []
        self.num_looping_vs_not = [0, 0]

        # Crunch Numbers variables
        self.num_unique_loops = 0
        self.lens_unique_loops = []
        self.lens_pre_loops = []
        self.avg_len_pre_loop = None
        #---
        self.starts_by_loop_driver = []
        self.max_length_list_start_points = (self.max_value+1)**self.num_elems

    def run_it(self):
        """  Split start_point into driver and
             array.  Use array to build IATF and
             pass it to IATF_Runner, then run.
             While running, check for loops and
             determine which loop each run falls
             into.  Save data from each run in
             list_of_runs.  When finished,
             crunch_numbers() to get general
             info about list_of_runs.
        """

        for i in range(self.num_runs):
            self.do_one_run(i)

        self.crunch_numbers()


    def do_one_run(self, index):
        
        start_point = self.list_of_start_points[index][1:]
        my_init_driver = float(self.list_of_start_points[index][0])/(self.num_elems-1)

        my_IATF = IATF(start_point_differences=start_point, exponent=self.exponent)
        my_IATF_Runner = IATF_Runner(my_IATF, self.iters, init_driver=my_init_driver, driver_species='feedback', stop_if_looping=True)
        my_IATF_Runner.run_it()

        loop_index = my_IATF_Runner.loop_index

        loop_status = my_IATF_Runner.loop_status_boolean

        if loop_status is False:
            self.num_looping_vs_not[1] += 1
            the_loop = [None]
            loop_number = None
        else:
            self.num_looping_vs_not[0] += 1
            the_loop = my_IATF_Runner.list_concat_differences[loop_index:]
            loop_number = self.check_add_loop_list(the_loop)

        pre_loop = my_IATF_Runner.list_concat_differences[:loop_index]

        self.list_of_runs.append({'run_index':index,
                                  'start_point':self.list_of_start_points[index],
                                  'the_loop':the_loop,
                                  'pre_loop':pre_loop,
                                  'loop_index':loop_index,
                                  'len_loop':len(the_loop),
                                  'len_pre_loop':len(pre_loop),
                                  'loop_status':loop_status,
                                  'loop_number':loop_number})



    def generate_unique_start_points(self):
        """ Create a list of unique start_points, including an init_driver at
            index 0; driver selected from range 0 to num_elems.
        """

        while len(self.list_of_start_points) < self.num_runs:

            # Can't create more unique start_points than mathematically possible:
            max_num_runs_possible = self.max_value**self.num_elems+1

            if self.num_runs > max_num_runs_possible:
                raise ValueError("num_runs larger that max possible list of start_points")
            else:

                temp_start_point = [randint(0, self.max_value) for _ in range(self.num_elems)]
                temp_init_driver = randint(0, self.num_elems-1)
                temp_start_point.insert(0, temp_init_driver)

                if temp_start_point not in self.list_of_start_points:  # No repeats
                    self.list_of_start_points.append(temp_start_point)


    def check_add_loop_list(self, loop):
        """If no loops are in list_loops, add the current one
           Otherwise, check if one element of a loop is already
           in one of the existing loops.  If so, loop has
           already been encountered, so return index of
           that loop.  If not, add new loop to list_loops
           and return index of new loop.
        """

        temp_length = len(self.list_loops)

        if temp_length < 1:
            self.list_loops.append(loop)
            return 0
        else:
            for i in range(temp_length):
                for j in self.list_loops[i]:
                    if np.array_equal(j, loop[0]):
                        return i
        self.list_loops.append(loop)
        return temp_length-1


    def crunch_numbers(self):
        """ Using data in list_loops, determine
            how many unique loops have been found,
            how long each is, how long each of the
            pre_loops is (all pre-loops will be unique,
            so there will be one for each run), and
            what the average length of the pre_loops
            is.
        """
        self.num_unique_loops = len(self.list_loops)
        self.lens_unique_loops = [len(loop) for loop in self.list_loops]
        self.lens_pre_loops = [len(run['pre_loop']) for run in
                          self.list_of_runs]

        self.avg_len_pre_loop = sum(self.lens_pre_loops)/(len(self.lens_pre_loops) + 0.01)
        # to prevent dividing by zero for cases in which the pre_loop length is 0


#-----------------------------------------------------------------


class Feedback_Multi_Run_with_Condition(Feedback_Multi_Run):

    def run_it(self, multiplier, run_max, init_batch):
        """  Split start_point into driver and
             array.  Use array to build IATF and
             pass it to IATF_Runner, then run.
             While running, check for loops and
             determine which loop each run falls
             into.  Save data from each run in
             list_of_runs.  When finished,
             crunch_numbers() to get general
             info about list_of_runs.
        """

        run_counter = 0
        temp_num_unique_loops = 0

        for i in range(init_batch):
            self.do_one_run(i)
        self.crunch_numbers()
        run_counter += init_batch

        
        while (self.num_unique_loops > temp_num_unique_loops) and (run_counter < run_max):
              temp_num_unique_loops = self.num_unique_loops
              print("Loops so far: " + str(temp_num_unique_loops))
              temp_batch = temp_num_unique_loops * multiplier
              for i in range(temp_batch):
                  self.do_one_run(i)
              run_counter += temp_batch
              self.crunch_numbers()


    def do_one_run(self, index):

        self.generate_one_new_start_point()
        current_index = len(self.list_of_start_points)-1
        start_point = self.list_of_start_points[current_index][1:]
        my_init_driver = float(self.list_of_start_points[current_index][0])/(self.num_elems-1)

        my_IATF = IATF(start_point_differences=start_point, exponent=self.exponent)
        my_IATF_Runner = IATF_Runner(my_IATF, self.iters, init_driver=my_init_driver, driver_species='feedback', stop_if_looping=True)
        my_IATF_Runner.run_it()

        loop_index = my_IATF_Runner.loop_index

        loop_status = my_IATF_Runner.loop_status_boolean

        if loop_status is False:
            self.num_looping_vs_not[1] += 1
            the_loop = [None]
            loop_number = None
        else:
            self.num_looping_vs_not[0] += 1
            the_loop = my_IATF_Runner.list_concat_differences[loop_index:]
            loop_number = self.check_add_loop_list(the_loop)

        pre_loop = my_IATF_Runner.list_concat_differences[:loop_index]

        self.list_of_runs.append({'run_index':index,
                                  'start_point':self.list_of_start_points[current_index],
                                  'the_loop':the_loop,
                                  'pre_loop':pre_loop,
                                  'loop_index':loop_index,
                                  'len_loop':len(the_loop),
                                  'len_pre_loop':len(pre_loop),
                                  'loop_status':loop_status,
                                  'loop_number':loop_number})


    def generate_random_start_point(self):
        temp_point = [randint(0, self.max_value) for i in range(self.num_elems)]
        temp_point.insert(0, randint(0, self.num_elems-1))
        return temp_point


    def generate_one_new_start_point(self):

        if len(self.list_of_start_points) < self.max_length_list_start_points:
        
            temp_start_point = self.generate_random_start_point()

            while(temp_start_point in self.list_of_start_points):
                temp_start_point = self.generate_random_start_point()

            self.list_of_start_points.append(temp_start_point)

        else:
            raise ValueError("WARNING!  MAXIMUM STARTING POINTS REACHED!")

