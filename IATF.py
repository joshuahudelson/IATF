# IATF.py

import copy
import numpy as np

class IATF:
    """ A class for Iteratively-Adjusted Transfer Functions.  The
        object takes an n-dimensional starting array and an exponent,
        then generates subsequent arrays based on the input values it
        receives in the compute_next function.
    """

    def __init__(self,
                 start_point_differences=None,
                 start_point_transfer_function=None,
                 exponent=1
                 ):
        """ If differences given, compute transfer_function.
            If transfer_function given, no differences are computed
            (for now).  Check type in both cases.  Assign
            exponent and number of elements to state variables.
            Create variables for index and scaled_index, to be
            used later.

            Note: If both differences and transfer function are given,
            differences override transfer function.

            STATE VARIABLES:

            self.exponent: the exponent to which elements get raised.

            self.num_elems: the number of elements in the state.


            self.differences: the integer representation of the state.

            self.transfer_function: the scaled, floating point representation
                                    of the state.


            self.index: the current 'input' integer.

            self.scaled_index: self.index normalized.


            self.concat_differences: (property) differences concatenated with the integer index.

            self.concat_transfer_function: (property) transfer function concatenated with scaled index.
        """
        self.exponent = exponent

        if ((start_point_differences == None) and
           (start_point_transfer_function == None)):
            raise ValueError('Must provide either differences \
                              or transfer function.')

        elif start_point_differences != None:
            if type(start_point_differences[0]) != int:  # Numpy checks all values
                raise TypeError('Array must be of type int.')
            elif sum(start_point_differences) == 0:
                raise ValueError('Array cannot contain only zeros.')
            else:
                self.differences = np.array(start_point_differences)
                self.num_elems = len(self.differences)
                self.transfer_function = self.compute_transfer_function(self.differences)

        else:
            if type(start_point_transfer_function[0]) != float:  # Numpy checks all values
                raise TypeError('Array must be of type float.')
            else:
                self.transfer_function = np.array(start_point_transfer_function)
                self.differences = self.compute_differences()
                self.num_elems = len(start_point_transfer_function)

        self.index = None
        self.scaled_index = None


    def compute_next(self, input_value, location=0, epsilon=0.00000):
        """ If input is zero, use epsilon value (whose default is
            zero).  Look up index of input_value in
            transfer_function (and also make scaled_index
            with it), then use it to drive update
            method.
        """

        if round(input_value, 5) == 0.00000:
            input_value = epsilon

        self.index = self.find_index(input_value, location)
        self.update(self.index)

        self.scaled_index = float(self.index)/(self.num_elems-1)


    def find_index(self, value, location):
        """ Re-compute transfer_function based on given starting
            location (default is zero).  Compensate for boundary
            cases (if value==1, etc.) and return index of value.
            This function returns a value; if this gets changed,
            IATF_Runner will also need to be changed, as it calls
            this function to prime its list_indices list.
        """

        amount_to_roll = self.num_elems - location
        temp_differences = np.roll(self.differences, amount_to_roll)
        temp_differences = temp_differences**self.exponent
        temp_transfer_function = self.compute_transfer_function(temp_differences)

        if value > 1.0 or value < 0.0:
            raise ValueError('Input value must be between 0 and 1')

        # If the input value is 1.0, the transfer function will always return the highest
        # index, even if the difference between the last and second to last is zero.
        # Subtracting the smallest difference in the transfer function from the input value
        # ensures that it will choose the 2nd-to-last if this is the case, but won't return
        # a lower index if this is not the case...
        temp_transfer_differences = np.diff(np.insert(temp_transfer_function, 0, 0))
        min_diff = np.min(temp_transfer_differences[temp_transfer_differences.nonzero()])

        # ...unless the smallest difference is the entire magnitude of the transfer
        # function (i.e., all values but one are zero), in which case, just make it
        # arbitrarily smaller.
        if min_diff > 0.99999:
            min_diff = 0.99999   # Need to make this bigger?  See what happens with elem=3 and exp=10...50...100 (changes output pattern)

        if int(value) == 1:
            value = 1.0 - min_diff  # So that it chooses 2nd-to-last.  See above.

        index = np.sum(value >= temp_transfer_function)
        # Calculate index in terms of the pre-roll array.
        index = (index + location) % self.num_elems
        return index

    def update(self, value):
        """ This is the "Iterative Adjustment" of the class.
            Increment all indices by one and set the most-
            recently chosen index to zero.  Then compute the
            new resulting transfer_function.
        """

        self.differences += 1
        self.differences[value] = 0
        self.transfer_function = self.compute_transfer_function(self.differences)


    @property
    def concat_transfer_function(self):
        """ Insert most-recently-chosen index in transfer_function
            Useful for comparisons, as this contains complete data
            about state of the object.
        """

        return np.insert(self.transfer_function, 0, self.scaled_index)


    @property
    def concat_differences(self):
        """ Insert most-recently-chosen index in differences
            Useful for comparisons, as this contains complete data
            about state of the object.
        """

        return np.insert(self.differences, 0, self.index)


    def compute_transfer_function(self, array):
        """ Use Differences to generate transfer_function
        """

        cumsum = np.cumsum(array)
        denominator = cumsum[(self.num_elems - 1)]
        return cumsum/float(denominator)


    def compute_differences(self):
        """ Use Transfer_Function to generate differences.
            Normalize so that smallest value == 1.0.
        """

        # Needs to convert list of floats to ints,
        # but keeping proportions the same via
        # greatest common denominator.
        # But I might not use this at all.
        # Least Common Multiple function

        pass


# TESTS:

if __name__ == '__main__':

    tally = 0

    print("Diagnostic Test for IATF... \n")

    print("Test 1: Compute Transfer Function from Differences.")
    test_iatf = IATF([1, 1, 1, 1])
    check_1 = [0.25, 0.5, 0.75, 1.0]
    print("Starting Differences = [1, 1, 1, 1]")
    print("Transfer Function should be " + str(check_1))
    result_1 = test_iatf.transfer_function
    print(result_1)
    answer_1 = (list(check_1) == list(result_1))
    print(answer_1)
    tally += answer_1
    print("")

    print("Test 2: Check close-call on first input.")
    print("Input = 0.2499999")
    check_2 = 0.000
    print("Output should be " + str(check_2))
    test_iatf.compute_next(0.24999)
    result_2 = test_iatf.scaled_index
    print(result_2)
    answer_2 = (check_2 == result_2)
    print(answer_2)
    tally += answer_2
    print("")

    print("Test 3: Check second close-call.")
    print("Current Differences are: " + str(test_iatf.differences))
    print("Input = 0.3333333333333334")
    check_3 = 0.6666666666666666
    print("Output should be " + str(check_3))
    test_iatf.compute_next(0.3333333333333334)
    result_3 = test_iatf.scaled_index
    print(result_3)
    answer_3 = (check_3 == result_3)
    print(answer_3)
    tally += answer_3
    print("")

    print("Test 4: Check epsilon.")
    start_diffs = [1, 1, 1, 1]
    print("Starting Differences = " + str([1, 1, 1, 1]))
    test_epsilon = 0.1
    print("Epsilon = " + str(test_epsilon))
    test_iatf = IATF(start_diffs)
    check_4 = [0.0,
               0.333,
               0.0,
               0.333,
               0.667,
               0.0,
               0.333,
               0.667,
               0.0,
               0.333]
    answer_list = []
    for i in range(10):
        test_iatf.compute_next(0.0, epsilon = 0.1)
        result_4 = test_iatf.scaled_index
        print(str(check_4[i]) + " == " + str(round(result_4, 3)))
        answer_4 = check_4[i] == round(result_4, 3)
        answer_list.append(answer_4)
    final_4 = sum(answer_list) == 10
    print(final_4)
    tally += final_4
    print("")

    print("Test 5: Check zero starting state.")
    start_diffs = [0, 0, 0, 0]
    print("Starting differences = " + str(start_diffs))
    test_iatf = IATF(start_diffs)
    test_iatf.compute_next(0.0)
    result5 = test_iatf.transfer_function
    result52 = test_iatf.differences
    print(str(result5) + " | " + str(result52))
