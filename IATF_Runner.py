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
                 location_list=None,
                 output_type='integer'
                ):
        """
        IATF:             Object, passed from outside, so it can be any 
                          sub-class of this object that we want 
                          to test.

        iters:            Int, number of times we want to compute 
                          the next value before we return the list.

        init_driver:      Float, needed for 'single_value' and 
                          'feedback' species.  Not needed for 'random'
                          or 'sequence' species.

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


        STATE VARIABLES:
        
        self.list_states: list of the states that the IATF has iterated through,
                          beginning with the initialized one.

        self.list_outputs: list of output values the IATF has produced, beginning
                           with the init_driver
            
        self.loop_status_boolean: whether this run ended up looping or not.
            
        self.loop_index: the index at which the loop began (0 if it didn't loop)
        """

        self.IATF = IATF
        self.iters = iters
        
        self.DRIVER_SPECIES_FEEDBACK = 'feedback'
        self.DRIVER_SPECIES_SEQUENCE = 'sequence'
        self.DRIVER_SPECIES_SINGLE_VALUE = 'single_value'
        self.DRIVER_SPECIES_RANDOM = 'random'

        if ((driver_species == self.DRIVER_SPECIES_FEEDBACK) & 
           (init_driver == None)):
               raise ValueError("You must provide an init_driver for feedback-species!")

        if ((driver_species == self.DRIVER_SPECIES_SINGLE_VALUE) &
            (init_driver == None)):
            raise ValueError("Init_driver missing for single-value-species!")

        self.init_driver = init_driver

        if ((driver_species == self.DRIVER_SPECIES_SEQUENCE) &
           ((driver_list == None) or
            (len(driver_list) != iters))):
            raise ValueError("Driver_list missing or of wrong length for sequence-species!")

        self.driver_species = driver_species
        self.stop_if_looping = stop_if_looping
        
        self.driver_list = self.make_driver_list(driver_list)
        
        self.OUTPUT_TYPE_INTEGER = 'integer'
        self.OUTPUT_TYPE_SCALED = 'scaled'
        
        self.output_type = output_type

        # Create self.list_states and insert the init_driver (or its unscaled version):
        if self.output_type == self.OUTPUT_TYPE_INTEGER:
            self.list_states = [copy.deepcopy(self.IATF.differences)]
            np.insert(self.list_states[0], 0, int(round(self.init_driver * (self.IATF.num_elems-1))))             
        elif self.output_type == self.OUTPUT_TYPE_SCALED:
            # Can't make IATF concat what it doesn't have...so...
            self.list_states = [copy.deepcopy(self.IATF.transfer_function)]
            np.insert(self.list_states[0], 0, self.driver_list[0])

        self.loop_status_boolean = False

        self.loop_index = None


    def run_it(self):
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
                    self.loop_index = temp_loop_test[1]
                    return

            if self.output_type == self.OUTPUT_TYPE_INTEGER:
                self.list_states.append(copy.deepcopy(self.IATF.concat_differences))
            elif self.output_type == self.OUTPUT_TYPE_SCALED:
                self.list_states.append(copy.deepcopy(self.IATF.concat_transfer_function))

            # Feedback driver list needs latest index choice in
            # order to drive the next iteration.
            if self.driver_species == self.DRIVER_SPECIES_FEEDBACK:
                self.driver_list.append(self.IATF.scaled_index)
        
        self.loop_index = 0

        self.useful_data = {}


    def am_i_looping(self, array):
        """ Find out if an array is already in the list of
            concat_differences.
        """
        
        for i in range(len(self.list_states)):
            if np.array_equal(self.list_states[i], array):
                return (True, i)
        return (False, 0)
    
    
    def make_driver_list(self, driver_list):
        """ Depending on the driver_species, make a list of
            values ('iters' in length) that will be used to
            drive the IATF.  If species is 'feedback'
            the subsequent values will be generated as the
            object iterates.
        """

        if self.driver_species == self.DRIVER_SPECIES_RANDOM:
            return(self.make_random_list())
        elif self.driver_species == self.DRIVER_SPECIES_FEEDBACK:
            return([self.init_driver])
        elif self.driver_species == self.DRIVER_SPECIES_SINGLE_VALUE:
            return(np.ones(self.iters)*self.init_driver)
        elif self.driver_species == self.DRIVER_SPECIES_SEQUENCE:
        # Had: return(self.driver_list) before, but this can't be right.  Must be:
            return(driver_list)


    def make_random_list(self):
        """ Make a list of random floats between 0 and 1
        """

        temp_list = [np.random.rand() for _ in range(self.iters)]
        return temp_list


# TESTS-----------------------------------------------------------

from IATF import IATF

if __name__ == '__main__':
    test_object = IATF([1, 1, 1, 1, 1, 1, 1])
    test_runner = IATF_Runner(test_object, 100, init_driver=0.5, driver_species='feedback')
    test_runner.run_it()
    print(test_runner.driver_list)
    print()
    print(test_runner.list_states)
    print()
    print(test_runner.list_outputs)
