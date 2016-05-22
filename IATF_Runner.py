# IATF_Runner

from random import random

class IATF_Runner:
    """ A class for generating lists of IATF output. 
    """

    def __init__(self, 
                 IATF_Object,
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
        IATF_Object:      Object, passed from outside, so it can be any 
                          sub-class of this object that we want 
                          to test.
        iters:            Int, number of times we want to compute 
                          the next value before we return the list.
        init_driver:      Float, needed for 'single_value' and 
                          'feedback' species.
        driver_species:   String, what kind of numbers are driving the 
                          IATF_Object (as arguments to its 
                          compute_next() function)
        stop_if_looping:  Boolean, if True, stop iterating when current
                          state is already in the list being
                          generated.
        driver_list:      List, only used for 'sequence' species.
                          Used for driving IATF_Object with a
                          specific sequence of numbers (i.e. sinusoid)
        location_species: String, what index to treat as 0 when
                          searching the Transfer Function in find_index().
                          'Feedback' means it uses the last index returned.
        location_list:    List, similar to driver_list when 'sequence' is
                          species.  I might not ever get around to using it.
        """

        self.IATF_Object = IATF_Object
        self.iters = iters
        
        if ((driver_species == 'feedback') & 
           (init_driver == None)):
               raise ValueError("Must provide an init_value!")

        self.init_driver = init_driver

        if ((driver_species == 'sequence') &
           ((driver_list == None) or
            (len(driver_list) != iters))):
            raise ValueError("Driver_list lacking or of wrong length!")
        if ((driver_species == 'single_value') &
            (init_driver == None)):
            raise ValueError("Init_driver missing!")

        self.driver_species = driver_species
        self.stop_if_looping = stop_if_looping
        self.driver_list = self.make_driver_list(driver_list)

        self.list_Differences = [self.IATF_Object.Differences]
        temp_cumsum = np.cumsum(self.list_Differences)
        
        # Not sure about this, below, but will leave it for now. 
        self.list_indices = [self.IATF_Object.find_index(self.driver_list[0], init_location)]
        self.list_scaled_indices = [self.list_indices[0]/float(len(self.list_Differences[0]))]
        self.list_Transfer_Functions = [self.IATF_Object.Transfer_Function]
        self.list_concat_TF = [self.IATF_Object.concat_TF(self.list_scaled_indices[0])]
        self.list_concat_Diff = [self.IATF_Object.concat_Diff(self.list_indices[0])]

    def run_it(self):
        """ Obvious?
        """
        
        loop_index = self.generate_lists()

        return({
                'list_indices':self.list_indices,
                'list_Differences':self.list_Differences,
                'list_scaled_indices':self.list_scaled_indices,
                'list_Transfer_Functions':self.list_Transfer_Functions,
                'list_concat_TF':self.list_concat_TF,
                'list_concat_Diff':self.list_concat_Diff,
                'loop_index':loop_index
              })


    def generate_lists(self):
        """ Drives the IATF_Object some number of times.  
            Stops iterating if the current state has been 
            reached previously. Adds values to all the 
            lists.  Returns the number of iterations that 
            have been performed.
        """

        loop_index_counter = 0

        for i in range(self.iters):
            x = copy.deepcopy(self.IATF_Object.compute_next(self.driver_list[i]))

            if self.stop_if_looping==True:
                if x['list_concat_Diff'] in self.list_concat_Diff:
                    return loop_index_counter
                else:
                    loop_index_counter += 1

            self.list_indices.append(x['index'])
            self.list_Differences.append(x['Differences'])
            self.list_scaled_indices.append(x['scaled_index'])
            self.list_Transfer_Functions.append(x['Transfer_Function'])
            self.list_concat_TF.append(x['concat_TF'])
            self.list_concat_Diff.append(x['concat_Diff'])

            # Feedback driver list needs latest index choice in
            # order to drive the next iteration.
            if self.driver_species == 'feedback':
                self.driver_list.append(x['scaled_index'])
        
        return loop_index_counter

    
    def make_driver_list(self, list):
        """ Depending on the driver_species, make a list of
            values ('iters' in length) that will be used to
            drive the IATF_Object.  If species is 'feedback'
            the subsequent values will be generated as the
            object iterates.
        """

        if self.driver_species == 'random':
            return(self.make_random_list())
        elif self.driver_species == 'feedback':
            return([self.init_driver])
        elif self.driver_species == 'single_value':
            return(np.ones(self.iters)*self.init_driver)
        elif self.driver_species == 'sequence':
            return(self.driver_list)

    def make_random_list(self):
        """ Make a list of random floats between 0 and 1
        """

        temp_list = [np.random.rand() for _ in range(self.iters)]
        return temp_list

if __name__ == '__main__':
    #from IATF import IATF
    x = IATF([1, 1, 1, 1])
    test_runner = IATF_Runner(x, 10, init_driver=0, driver_species='single_value')
    results = test_runner.run_it()
    
    for i in results['list_concat_Diff']:
        print(i)
