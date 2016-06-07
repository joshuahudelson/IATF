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


    def run_it(self):
        
        for i in range(self.num_runs):
            
            start_point = self.list_of_start_points[i][1:]
            my_init_driver = float(self.list_of_start_points[i][0])/(self.num_elems-1)
            
            my_IATF = IATF(start_point_differences=start_point, exponent=self.exponent)
            my_IATF_Runner = IATF_Runner(my_IATF, self.iters, init_driver=my_init_driver, driver_species='feedback', stop_if_looping=True)
            my_IATF_Runner.run_it()
            
            loop_index = my_IATF_Runner.loop_index
            the_loop = my_IATF_Runner.list_concat_differences[loop_index:]
            pre_loop = my_IATF_Runner.list_concat_differences[:loop_index]
            
            self.list_of_runs.append({'run_index':i,
                                      'start_point':self.list_of_start_points[i],
                                      'the_loop':the_loop,
                                      'pre_loop':pre_loop,
                                      'loop_index':loop_index,
                                      'len_loop':len(the_loop),
                                      'len_pre_loop':len(pre_loop),
                                      'unique_loop_point':the_loop[0]})
    
    
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
                     
"""         
    def crunch_numbers(self):
        unique loops
        lengths of unique loops
        unique points in those loops
        
        longest pre-loop lenghth
        shortest pre-loop length
        
        And THEN it needs to go through the original list of dictionaries and designate which loop (0, 1, 2...)
        each belongs to.  No, actually, do this AS it's running...by keeping an ongoing list of the loops and
        checking each time.
"""
if __name__=='__main__':
    x = Feedback_Multi_Run(5, 1, 3, 30, max_value=10, stop_if_looping=True)
    print(x.list_of_start_points)
    x.run_it()
    for i in x.list_of_runs:
        print(i)
