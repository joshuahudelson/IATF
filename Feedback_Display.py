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

        self.table_of_tests = []

    def run_it(self):
        for index_elems, num_elems in enumerate(self.list_num_elems):

            self.table_of_tests.append([])

            for index_exp, exp in enumerate(self.list_exps):

                self.make_lab(num_elems, exp)
                self.run_lab(index_elems, index_exp)


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

        temp_dict = {'total number of runs' : self.the_Lab.number_of_runs_completed,
                     'list of loops' : self.the_Lab.list_loops,
                     'number looping vs not' : self.the_Lab.num_looping_vs_not,
                     'number unique loops' : self.the_Lab.num_unique_loops,
                     'lengths unique loops' : self.the_Lab.lens_unique_loops,
                     'average preloop per loop' : self.the_Lab.avg_preloop_per_loop,
                     'runs per loop' : self.the_Lab.runs_per_loop,
                     'runs per loop percentage' : self.the_Lab.runs_per_loop_per_total}

        self.table_of_tests[index_elems].append(temp_dict)

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
