# IATF_Runner

from random import random
import numpy as np
import copy

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
        init_location:    Int, which index the IATF object should treat as 0 
                          when doing the first call of run_it()
        location_list:    List, similar to driver_list when 'sequence' is
                          species.  I might not ever get around to using it.
        loop_index:       Int, index at which the sequence begins being in a
                          a loop that it will never leave (if driver_species
                          is set to 'feedback.'
        loop_status_boolean:
                          Boolean, whether the list being generated has
                          started looping.  Default is False.
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
        
        self.list_indices = [self.IATF.find_index(self.driver_list[0], init_location)]
        self.list_scaled_indices = [self.list_indices[0] / float(len(self.list_differences[0]))]
        self.list_transfer_functions = [self.IATF.transfer_function]

        temp_index = self.list_indices[0]
        temp_scaled_index = float(temp_index)/len(self.IATF.transfer_function)
        self.list_concat_differences = [np.insert(self.IATF.differences, 0, temp_index)]
        self.list_concat_transfer_function = [np.insert(self.IATF.transfer_function, 0, temp_scaled_index)]

        self.loop_status_boolean = False


    def run_it(self):
        """ Call generate_lists, which creates the lists
            of IATF output, and assign the loop_index with
            what it returns.  This could be collapsed into
            generate_lists.
        """
        
        self.loop_index = self.generate_lists()

        
    def generate_lists(self):
        """ Drives the IATF some number of times.  
            Stops iterating if the current state has been 
            reached previously and turns loop_status_boolean
            to True. Adds values to all the 
            lists.  Returns the number of iterations that 
            have been performed (or 0 if it doesn't loop).
        """

        for i in range(self.iters):
            self.IATF.compute_next(self.driver_list[i])

            if self.stop_if_looping==True:
                temp_loop_test = self.am_i_looping(self.IATF.concat_differences)
                if temp_loop_test[0]:
                    self.loop_status_boolean = temp_loop_test[0]
                    return temp_loop_test[1]
                
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
        
        return 0

    
    def am_i_looping(self, array):
        """ Find out if an array is already in the list of
            concat_differences.
        """
        
        for i in range(len(self.list_concat_differences)):
            if np.array_equal(self.list_concat_differences[i], array):
                return (True, i)
        return (False, 0)
    
    
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
    test_runner = IATF_Runner(test_object, 20, init_driver=0.5, driver_species='feedback')
    print(test_runner.driver_list)
    print(test_runner.list_scaled_indices)
    print(test_runner.list_concat_differences)
    print(test_runner.list_concat_transfer_function)
