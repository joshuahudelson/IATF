# IATF.py

import copy
import numpy as np

class IATF:
    """ A class for Iteratively-Adjusted Transfer Functions.
        The object takes an n-dimensional starting array and
        an exponent, then generates subsequent arrays based 
        on the input values it receives.
    """

    def __init__(self, starting_point, exponent=1):
        """ If starting point content is of type float, assume it's
            a transfer function normalized to between 0 and 1.
            If it's of type int, assume it's an array of
            differences and generate transfer function.
        """

        self.exponent = exponent
        self.num_elems = len(starting_point)

        if type(starting_point[0]) == float:
            self.Transfer_Function = np.array(starting_point)
            self.Differences = None
        elif type(starting_point[0]) == int:
            self.Differences = np.array(starting_point)
            self.Transfer_Function = self.compute_Transfer_Function(self.Differences)
        else:
            raise TypeError('Array must be of type float or int.')

    def compute_next(self, input_value, location=0, epsilon=0.00000):
        """ Look up index of input_value in Transfer_Function.
            Update Transfer_Function.  Return scaled index,
            Transfer_Function, un-scaled index, Differences,
            and concatenated arrays of these two pairs.
        """ 
        if round(input_value, 5) == 0.00000:
            input_value = epsilon

        index = self.find_index(input_value, location)
        self.update(index)

        scaled_index = float(index)/self.num_elems
        concat_TF = self.concat_TF(scaled_index)
        concat_Diff = self.concat_Diff(index)

        return({'scaled_index': scaled_index,
                'Transfer_Function': self.Transfer_Function,
                'index': index,
                'Differences': self.Differences,
                'concat_TF':concat_TF,
                'concat_Diff':concat_Diff
               })

    def find_index(self, value, location):
        """ Re-compute Transfer_Function based on given starting location,
            compensate for boundary cases, and return index of value.
        """
        amount_to_roll = self.num_elems - location
        temp_Diff = np.roll(self.Differences, amount_to_roll)
        temp_Diff = temp_Diff**self.exponent
        temp_TF = self.compute_Transfer_Function(temp_Diff)
        min_diff = np.min(temp_TF[temp_TF.nonzero()])

        if int(min_diff) == 1:
            min_diff = 0.99999

        if int(value) == 1:
            value = 1.0 - min_diff  # So that it chooses 2nd-to-last.

        if value < 0.0:
            raise

        index = np.sum(value >= temp_TF)
        # Un-roll.  Index is now in terms of original array.
        index = (index + location) % self.num_elems

        return index

    def update(self, value):
        """ This is the "Iterative Adjustment" of the class.
            Increment all indices by one and set the most-
            recently chosen index to zero.  Then compute the
            new resulting Transfer_Function
        """
        self.Differences += 1
        self.Differences[value] = 0
        self.Transfer_Function = self.compute_Transfer_Function(self.Differences)

    def concat_TF(self, term):
        """ Insert most-recently-chosen index in Transfer_Function
            Useful for comparisons, as this contains complete data
            about state of the object.
        """
        return np.insert(self.Transfer_Function, 0, term)

    def concat_Diff(self, term):
        """ Insert most-recently-chosen index in Differences
            Useful for comparisons, as this contains complete data
            about state of the object.
        """
        return np.insert(self.Differences, 0, term)

    def compute_Transfer_Function(self, array):
        """ Use Differences to generate Transfer_Function
        """
        cumsum = np.cumsum(array)
        denominator = cumsum[(self.num_elems - 1)]
        return cumsum/float(denominator)

    def compute_Differences(self):
        """ Use Transfer_Function to generate Differences.
            Normalize so that smallest value == 1.0.
        """
        # Needs to convert list of floats to ints,
        # but keeping proportions the same via
        # greatest commond denominator.
        # But I might not use this at all.
        pass


if __name__ == '__main__':
    test_iatf = IATF([1, 1, 1, 1])
    print("Should print 0.25, 0.5, 0.75, 1.0")
    print(test_iatf.Transfer_Function)
    x = test_iatf.compute_next(0.25)
    print("Should print 1")
    print(x['index'])

