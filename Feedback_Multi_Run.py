from random import randint

class Feedback_Multi_Run:
    
    def __init__(self, num_elems, exponent, num_runs, iters, max_value=None, stop_if_looping=True):
        
        self.num_runs = num_runs
        self.num_elems = num_elems
        self.iters = iters
        self.exponent = exponent
        
        if max_value == None:
            self.max_value = num_elems
        else:
            self.max_value = max_value
        
        self.list_of_runs = []
        self.list_of_start_points = []
        self.generate_unique_start_points()
        
        self.list_loops = []

        # Crunch Numbers variables
        self.num_unique_loops = None
        self.lengths_of_unique_loops = []
        self.lengths_of_pre_loops = []
        self.avg_length_of_pre_loop = None


    def run_it(self):
        
        for i in range(self.num_runs):
            
            start_point = self.list_of_start_points[i][1:]
            my_init_driver = float(self.list_of_start_points[i][0])/(self.num_elems-1)
            
            my_IATF = IATF(start_point_differences=start_point, exponent=self.exponent)
            my_IATF_Runner = IATF_Runner(my_IATF, self.iters, init_driver=my_init_driver, driver_species='feedback', stop_if_looping=True)
            my_IATF_Runner.run_it()
            
            loop_index = my_IATF_Runner.loop_index
            
            loop_status = my_IATF_Runner.loop_status_boolean
            
            if loop_status is False:
                the_loop = [None]
                loop_number = None
            else:
                the_loop = my_IATF_Runner.list_concat_differences[loop_index:]
                loop_number = self.check_add_loop_list(the_loop)

            pre_loop = my_IATF_Runner.list_concat_differences[:loop_index]
            
            self.list_of_runs.append({'run_index':i,
                                      'start_point':self.list_of_start_points[i],
                                      'the_loop':the_loop,
                                      'pre_loop':pre_loop,
                                      'loop_index':loop_index,
                                      'len_loop':len(the_loop),
                                      'len_pre_loop':len(pre_loop),
                                      'loop_status':loop_status,
                                      'loop_number':loop_number})
            
        self.crunch_numbers()
    
    
    def generate_unique_start_points(self):
        """ Create a list of unique start_points, including an init_driver at
            index 0; driver selected from range 0 to num_elems.
        """
        
        while len(self.list_of_start_points) < self.num_runs: # Will need to raise exception if num_runs
                                                              # is larger than possible permutations
            
            temp_start_point = [randint(0, self.max_value) for _ in range(self.num_elems)]
            temp_init_driver = randint(0, self.num_elems-1)
            temp_start_point.insert(0, temp_init_driver)
            
            if temp_start_point not in self.list_of_start_points:  # No repeats
                self.list_of_start_points.append(temp_start_point)

                
    def check_add_loop_list(self, loop):
        
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
        
        self.num_unique_loops = len(self.list_loops)
        
        for i in self.list_loops:
            self.lengths_of_unique_loops.append(len(i))
        
        for i in self.list_of_runs:
            self.lengths_of_pre_loops.append(len(i['pre_loop']))
        
        self.avg_length_of_pre_loop = sum(self.lengths_of_pre_loops)/len(self.lengths_of_pre_loops)


if __name__=='__main__':
    x = Feedback_Multi_Run(6, 20, 10, 100, max_value=10, stop_if_looping=True)
    x.run_it()
    print("---")
    for i in x.list_loops:
        print i
    print("-----")
    print(x.num_unique_loops)
    print(x.lengths_of_unique_loops)
    print(x.lengths_of_pre_loops)
    print(x.avg_length_of_pre_loop)
