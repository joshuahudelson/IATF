# IATF_Runner

from random import random
import numpy as np

class IATF_Runner:
    """ A class for generating lists of IATF output. 
    """

    def __init__(self, 
                 IATF,
                 iters,
                 init_driver=None,
                 driver_species='random',
                 stop_if_looping=False,
                 driver_list=None,
                 location_species='single_value',
                 init_location=0,
                 location_list=None
                ):
        """
        IATF:             Object, passed from outside, so it can be any 
                          sub-class of this object that we want 
                          to test.
        iters:            Int, number of times we want to compute 
                          the next value before we return the list.
        init_driver:      Float, needed for 'single_value' and 
                          'feedback' species.
        driver_species:   String, what kind of numbers are driving the 
                          IATF (as arguments to its 
                          compute_next() function)
        stop_if_looping:  Boolean, if True, stop iterating when current
                          state is already in the list being
                          generated.
        driver_list:      List, only used for 'sequence' species.
                          Used for driving IATF with a
                          specific sequence of numbers (i.e. sinusoid)
        location_species: String, what index to treat as 0 when
                          searching the Transfer Function in find_index().
                          'Feedback' means it uses the last index returned.
        location_list:    List, similar to driver_list when 'sequence' is
                          species.  I might not ever get around to using it.
        loop_index:       Int, index at which the sequence begins being in a
                          a loop that it will never leave (if driver_species
                          is set to 'feedback.'
        """

        self.IATF = IATF
        self.iters = iters
        self.loop_index = None
        
        self.SPECIES_FEEDBACK = 'feedback'
        self.SPECIES_SEQUENCE = 'sequence'
        self.SPECIES_SINGLE_VALUE = 'single_value'
        self.SPECIES_RANDOM = 'random'

        if ((driver_species == self.SPECIES_FEEDBACK) & 
           (init_driver == None)):
               raise ValueError("Must provide an init_value!")

        self.init_driver = init_driver

        if ((driver_species == self.SPECIES_SEQUENCE) &
           ((driver_list == None) or
            (len(driver_list) != iters))):
            raise ValueError("Driver_list lacking or of wrong length!")
        if ((driver_species == self.SPECIES_SINGLE_VALUE) &
            (init_driver == None)):
            raise ValueError("Init_driver missing!")

        self.driver_species = driver_species
        self.stop_if_looping = stop_if_looping
        self.driver_list = self.make_driver_list(driver_list)

        self.list_differences = [self.IATF.differences]
        temp_cumsum = np.cumsum(self.list_differences)
        
        # Not sure about this, below, but will leave it for now. 
        self.list_indices = [self.IATF.find_index(self.driver_list[0], init_location)]
        self.list_scaled_indices = [self.list_indices[0] / float(len(self.list_differences[0]))]
        self.list_transfer_functions = [self.IATF.transfer_function]

        temp_index = self.driver_list[0]
        temp_scaled_index = float(temp_index)/len(self.IATF.transfer_function)
        self.list_concat_differences = [np.insert(self.IATF.differences, 0, temp_index)]
        self.list_concat_transfer_function = [np.insert(self.IATF.transfer_function, 0, temp_scaled_index)]

    def run_it(self):
        """ Obvious?
        """
        
        self.loop_index = self.generate_lists()  # No reason to have this returned, really...

        
    def generate_lists(self):
        """ Drives the IATF some number of times.  
            Stops iterating if the current state has been 
            reached previously. Adds values to all the 
            lists.  Returns the number of iterations that 
            have been performed.
        """

        loop_index_counter = 0

        for i in range(self.iters):
            self.IATF.compute_next(self.driver_list[i])

            if self.stop_if_looping==True:
                if self.IATF.concat_differences in self.list_concat_differences:
                    return loop_index_counter
                else:
                    loop_index_counter += 1

            self.list_indices.append(copy.deepcopy(self.IATF.index))
            self.list_differences.append(copy.deepcopy(self.IATF.differences))
            self.list_scaled_indices.append(copy.deepcopy(self.IATF.scaled_index))
            self.list_transfer_functions.append(copy.deepcopy(self.IATF.transfer_function))
            self.list_concat_transfer_function.append(copy.deepcopy(self.IATF.concat_transfer_function))
            self.list_concat_differences.append(copy.deepcopy(self.IATF.concat_differences))

            # Feedback driver list needs latest index choice in
            # order to drive the next iteration.
            if self.driver_species == self.SPECIES_FEEDBACK:
                self.driver_list.append(copy.deepcopy(self.IATF.scaled_index))
        
        return loop_index_counter

    
    def make_driver_list(self, list):
        """ Depending on the driver_species, make a list of
            values ('iters' in length) that will be used to
            drive the IATF.  If species is 'feedback'
            the subsequent values will be generated as the
            object iterates.
        """

        if self.driver_species == self.SPECIES_RANDOM:
            return(self.make_random_list())
        elif self.driver_species == self.SPECIES_FEEDBACK:
            return([self.init_driver])
        elif self.driver_species == self.SPECIES_SINGLE_VALUE:
            return(np.ones(self.iters)*self.init_driver)
        elif self.driver_species == self.SPECIES_SEQUENCE:
            return(self.driver_list)

    def make_random_list(self):
        """ Make a list of random floats between 0 and 1
        """

        temp_list = [np.random.rand() for _ in range(self.iters)]
        return temp_list

if __name__ == '__main__':
    test_object = IATF([1, 1, 1, 1])
    test_runner = IATF_Runner(test_object, 10, init_driver=0, driver_species='single_value')
    test_runner.run_it()
    
    for i in test_runner.list_concat_differences:
        print(i)
