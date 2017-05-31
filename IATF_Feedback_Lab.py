# IATF_Feedback_Lab

from random import randint
from IATF_Runner import IATF_Runner
from IATF import IATF
import numpy as np
import copy


class IATF_Feedback_Lab:
    """ A class for generating multiple lists
        of output from IATF_Runners, each
        starting with a unique start_point,
        and consolidating the information from
        those lists.
    """

    def __init__(self,
                 start_point_species,
                 num_elems,
                 exponent,
                 iters,
                 max_value=None,
                 threshold=0.1,
                 constant_state=None
                ):
        """
        num_elems:    Int, the length of the array that will
                      become the differences and transfer_function
                      in the IATF object.

        exponent:     Int or float, the exponent to which
                      the differences in the IATF object
                      will be raised before the transfer_
                      function is calculated.

        iters:        Int, the number of iterations each IATF_
                      Runner should do before stopping.

        max_value:    Int, The maximum value any of the differences
                      in the start_point.

        FILL IN REST HERE.

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

        num_looping_vs_not:
                      List, ints describing how many runs
                      ended in a loop and how many didn't.
        """

        self.start_point_species = start_point_species

        self.START_POINT_SPECIES_RANDOM = 'random'
        self.START_POINT_SPECIES_ALL = 'all'
        self.START_POINT_SPECIES_CONSTANT = 'constant'
        self.START_POINT_SPECIES_PATTERN = 'pattern'

        self.num_elems = num_elems
        self.exponent = exponent
        self.iters = iters

        if max_value == None:
            self.max_value = num_elems
        else:
            self.max_value = max_value

        self.list_of_runs = []

        self.list_of_start_points = []

        self.list_loops = []
        self.num_looping_vs_not = [0, 0]

        # Crunch Numbers variables
        self.num_unique_loops = 0
        self.lens_unique_loops = []
        self.lens_pre_loops = []

        self.max_length_list_start_points = (self.max_value+1)**self.num_elems

        self.start_points_repeated = 0

        self.threshold = threshold

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

        run_counter = 0

        self.do_one_run(0)
        run_counter += 1
        #self.crunch_numbers()

        # Need decision tree for different species.  So make check_condition() which returns a boolean to continue or not
        # Maybe run_it should also return a value?  Or at least print "Done!"

        while (len(self.list_loops)/run_counter > self.threshold) and (run_counter < self.max_length_list_start_points):
            self.do_one_run(run_counter)

            run_counter += 1

        self.crunch_numbers()


    def do_one_run(self, index):
        """ Generate a single new start point and make an IATF
            object with it.  Make an IATF_Runner and run
            it on the IATF.
        """

        self.list_of_start_points.append(self.get_start_point())

        current_index = len(self.list_of_start_points)-1

        start_point_state = self.list_of_start_points[current_index][1:]
        start_point_driver = float(self.list_of_start_points[current_index][0])/(self.num_elems-1)

        my_IATF = IATF(start_point_differences=start_point_state, exponent=self.exponent)
        my_IATF_Runner = IATF_Runner(my_IATF,
                                     self.iters,
                                     init_driver=start_point_driver,
                                     driver_species='feedback',
                                     stop_if_looping=True,
                                     output_type='integer')

        my_IATF_Runner.run_it()

        loop_index = my_IATF_Runner.loop_index
        loop_status = my_IATF_Runner.loop_status_boolean

        if loop_status is False:
            self.num_looping_vs_not[1] += 1
            the_loop = [None]
            loop_number = None
        else:
            self.num_looping_vs_not[0] += 1
            the_loop = my_IATF_Runner.list_states[loop_index:]
            loop_number = self.check_add_loop_list(the_loop)

        pre_loop = my_IATF_Runner.list_states[:loop_index]

        self.list_of_runs.append({'run_index':index,
                                  'start_point':self.list_of_start_points[current_index],
                                  'the_loop':the_loop,
                                  'pre_loop':pre_loop,
                                  'loop_index':loop_index,
                                  'len_loop':len(the_loop),
                                  'len_pre_loop':len(pre_loop),
                                  'loop_status':loop_status,
                                  'loop_number':loop_number})

# doesn't need to be returned
    def get_start_point(self):
        if self.start_point_species == self.START_POINT_SPECIES_RANDOM:
            return(self.generate_random_start_point())
        elif self.start_point_species == self.START_POINT_SPECIES_ALL:
            raise ValueError("species:all, not filled in yet.")
        elif self.start_point_species == self.START_POINT_SPECIES_CONSTANT:
            raise ValueError("species:constant, not filled in yet.")
        elif self.start_point_species == self.START_POINT_SPECIES_PATTERN:
            raise ValueError("species:pattern, not filled in yet.")
        else:
            raise ValueError("start_point_species not recognized!")


    def generate_random_start_point(self):

        if len(self.list_of_start_points) < self.max_length_list_start_points:

            temp_start_point = [randint(0, self.max_value) for i in range(self.num_elems)]
            temp_start_point.insert(0, randint(0, self.num_elems-1)) # this should probably be max_value!

            while((temp_start_point in self.list_of_start_points) | (sum(temp_start_point[1:]) == 0)):
                self.start_points_repeated += 1
                print('Repeats: ' + str(self.start_points_repeated) + \
                ' vs. ' + str(len(self.list_of_start_points)))
                temp_start_point = self.generate_random_start_point()

            #self.list_of_start_points.append(copy.deepcopy(temp_start_point))
            return(copy.deepcopy(temp_start_point))

        else:
            raise ValueError("WARNING!  MAXIMUM STARTING POINTS REACHED!")


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
            so there will be one for each run).
        """
        self.num_unique_loops = len(self.list_loops)
        self.lens_unique_loops = [len(loop) for loop in self.list_loops]
        self.lens_pre_loops = [len(run['pre_loop']) for run in
                          self.list_of_runs]


def run_test():
    test_runner = IATF_Feedback_Lab('random',
                 6,
                 2,
                 500,
                 max_value=None,
                 threshold=0.001,
                 constant_state=None)

    test_runner.run_it()

    print(test_runner.num_unique_loops)


if __name__ == '__main__':
    run_test()
