from IATF_Feedback_Lab import IATF_Feedback_Lab
import copy

class Feedback_Data:
    """ A class for running multiple IATF_Feedback_Lab tests,
        and collating the data for the Feedback_Test_GUI.
    """

    def __init__(self,
                 start_point_species,
                 list_num_elems,
                 list_exps,
                 iters,
                 max_value=None,
                 threshold=0.1,
                 constant_state=None,
                 location_species='single_value',
                 init_location=0
                 ):
        """
        start_point_species:
                             Random: obvious

                             All: if num_elems is small enough,
                                  do all possible combinations up to max_value.

                             Constant State: keep the initial state the same
                                             and test different initial drivers.

                            Patter: produce starting points based on some kind of
                                    pattern.

        self.list_num_elems: List of ints, one or more num_elems we want
                             to test.

        self.list_exps:      List of floats, one or more exponents we want
                             to test.

        self.iters:          Int, same as usual.

        self.max_value:      maximum value any int in a starting point can be.

        threshold:           Float, the percentage at which the lab will stop
                             testing new points.  Calculated by:
                             (number of unique loops)/(total number of runs)

        constant_state:      List of ints, to be used if the constant_state
                             species is chosen (some day).
        """

        self.start_point_species = start_point_species
        self.list_num_elems = list_num_elems
        self.list_exps = list_exps
        self.iters = iters
        self.max_value = max_value
        self.threshold = threshold
        self.constant_state = constant_state

#---------------------
        """ Collate everything.  One big 2D array: num_elems by exps.

            - the loops
            - number of loops
            - percentage of runs per loops
            - average pre-length per loop
            -


        """


        self.loop_output_pattern = []

        self.mem_list_loops = []
        self.mem_list_num_loops = [] # do I need this?  And what about other info, like pre-loop data?

    def run_it(self):
        for index_elems, num_elems in enumerate(self.list_num_elems):
            print("index elems: " + str(index_elems))

            self.mem_list_loops.append([])
            self.mem_list_num_loops.append([])

            for index_exp, exp in enumerate(self.list_exps):
                print("index exp: " + str(index_exp))

                self.mem_list_loops[index_elems].append([])
                self.mem_list_num_loops[index_elems].append([])

                self.make_lab(num_elems, exp)

                self.run_lab(index_elems, index_exp)

                self.crunch_numbers()

                self.make_text_file()


    def make_lab(self, num_elems, exp):
        self.the_Lab = IATF_Feedback_Lab(self.start_point_species,
                                         num_elems,
                                         exp,
                                         self.iters,
                                         self.max_value,
                                         self.threshold,
                                         self.constant_state)


    def run_lab(self, index_elems, index_exp):

        self.the_Lab.run_it()

        # Need to add the elems and exp into current_list_of_runs (?), and also the stuff below...
        self.current_list_of_runs = self.the_Lab.list_of_runs # no real reason to copy this...
        self.list_loops = self.the_Lab.list_loops
        self.num_unique_loops = self.the_Lab.num_unique_loops
        self.lens_unique_loops = self.the_Lab.lens_unique_loops
        self.lens_pre_loops = self.the_Lab.lens_pre_loops

        self.mem_list_loops[index_elems][index_exp].append(self.list_loops)
        self.mem_list_num_loops[index_elems][index_exp].append(self.num_unique_loops)

    def crunch_numbers(self):

        self.make_loop_output_patterns()

        self.make_start_point_patterns()

        self.collate_start_point_mean_differences_by_loop()


    def make_loop_output_patterns(self):

        self.loop_output_patterns = [] # this is not initialized in __init__

        for loop in self.list_loops:
            len_loop = len(loop)

            # could decouple this as its own function...
            # do I need to do deep copies anywhere?  No, because lists are new?
            output_loop = [state[0] for state in loop]
            difference_loop = [(output_loop[element] - (output_loop[(element - 1) % len_loop])) for element in range(len_loop)]
            binary_loop = [int(element > 0) for element in difference_loop]



            jump_distance_loop = [abs(element) for element in difference_loop]
            mean_jump_distance = sum(jump_distance_loop)/len(jump_distance_loop)

            self.loop_output_pattern.append({'output_loop':output_loop,
                                             'difference_loop':difference_loop,
                                             'binary_loop':binary_loop,
                                             'mean_jump':mean_jump_distance})


    def make_start_point_patterns(self):

        self.start_point_patterns = [] # this is not initialized in __init__

        for run in self.current_list_of_runs:
            self.start_point_patterns.append(self.make_one_start_point_pattern(run['start_point'],
                                             run['loop_number']))


    def make_one_start_point_pattern(self, start_state, loop_number):
        """ I will want to find a way to measure the spectral 'spread' of the
            start_point eventually.  For now, I'll just do the mean (and, note
            unnormalized).
        """

        abs_difference_pattern = [abs(start_state[i] - start_state[i + 1]) for i in range(len(start_state) - 1)]
        mean_differences = sum(copy.deepcopy(abs_difference_pattern))/len(abs_difference_pattern)

        return {'loop_number':loop_number, 'difference_pattern':abs_difference_pattern,
                'mean_differences':mean_differences}


    def collate_start_point_mean_differences_by_loop(self):

        self.loop_and_start_point_mean_differences = {}
        self.num_start_points_per_loop = {}
        self.mean_mean_difference_per_loop = {}

        for i in range(len(self.list_loops)):

            num_start_points_counter = 0
            sum_mean_difference_counter = 0

            self.loop_and_start_point_mean_differences['loop_' + str(i)] = []

            for entry in self.start_point_patterns:
                if entry['loop_number'] == i:
                    self.loop_and_start_point_mean_differences['loop_' + str(i)].append(entry['mean_differences'])
                    num_start_points_counter += 1
                    sum_mean_difference_counter += entry['mean_differences']

            self.num_start_points_per_loop['loop_' + str(i)] = num_start_points_counter
            self.mean_mean_difference_per_loop['loop_' + str(i)] = sum_mean_difference_counter/num_start_points_counter


    def make_text_file(self):
        pass


#----------------------------------------------------------


def test():
    new_feedback_data = Feedback_Data('random',
                                      [6],
                                      [3],
                                      1000,
                                      threshold=0.001)
    new_feedback_data.run_it()

    print(new_feedback_data.num_start_points_per_loop)
    print(new_feedback_data.mean_mean_difference_per_loop)
    print()
    for key in new_feedback_data.loop_and_start_point_mean_differences.keys():
        print(key + ' : ' + str(new_feedback_data.loop_and_start_point_mean_differences[key]))


if __name__=='__main__':
    test()
