from IATF_Feedback_Lab import IATF_Feedback_Lab

class Feedback_Data:
    """A class for collating/representing fed-back IATF runs.
    """

    def __init__(self,
                 start_point_species,
                 list_num_elems,
                 list_exps,
                 iters,
                 max_value=None,
                 threshold=0.1,
                 constant_state=None
                 ):

        self.start_point_species = start_point_species
        self.list_num_elems = list_num_elems
        self.list_exps = list_exps
        self.iters = iters
        self.max_value = max_value
        self.threshold = threshold
        self.constant_state = constant_state

        self.the_Lab = None
        self.list_of_multi_runs = []

        self.loop_output_pattern = []

    def run_it(self):
        for num_elems in self.list_num_elems:
            for exp in self.list_exps:

                self.make_lab(num_elems, exp)

                self.run_lab()

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


    def run_lab(self):

        self.the_Lab.run_it()
        # Need to add the elems and exp here, and also the stuff below...
        self.current_list_of_runs = self.the_Lab.list_of_runs

        self.list_loops = self.the_Lab.list_loops
        self.num_unique_loops = self.the_Lab.num_unique_loops
        self.lens_unique_loops = self.the_Lab.lens_unique_loops
        self.lens_pre_loops = self.the_Lab.lens_pre_loops


    def crunch_numbers(self):

        self.make_loop_output_patterns()

        self.collate_start_points_by_loop()


    def make_text_file(self):
        pass


#--------------------------------------------

    def make_loop_output_patterns(self):

        self.loop_output_patterns = []

        for loop in self.list_loops:
            len_loop = len(loop)
            output_loop = [state[0] for state in loop]
            difference_loop = [(output_loop[element] - (output_loop[(element - 1) % len_loop])) for element in range(len_loop)]
            binary_loop = [int(element > 0) for element in difference_loop]

            self.loop_output_pattern.append({'output_loop':output_loop,
                                             'difference_loop':difference_loop,
                                             'binary_loop':binary_loop})

        for _ in range(len(self.list_loops)):
            print('Output Loop:')
            print(self.loop_output_pattern[_]['output_loop'])
            print('State Loop:')
            for state in self.list_loops[_]:
                print(state)


    def collate_start_points_by_loop(self):
        pass


def test():
    new_feedback_data = Feedback_Data('random',
                                      [8],
                                      [1],
                                      1000,
                                      threshold=0.001)
    new_feedback_data.run_it()
#    for element in new_feedback_data.list_of_multi_runs[0][0]:
#        print(str(element) + " : " + str(new_feedback_data.list_of_multi_runs[0][0][element]))


if __name__=='__main__':
    test()
