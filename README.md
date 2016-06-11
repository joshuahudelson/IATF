Iteratively-Adjusted Transfer Functions

The following is mainly relevant to the Feedback_ Multi_Runs object:

Consider a multidimensional point [a, b, ..., z] that describes the state of a system.  The term at index 0 ("a") will be called the "driver," while the remaining terms ("b" through "z") will be called the "differences."

The driver will always be a value between 0 and the number of elements in differences minus 1.  The values of differences, however, can be between 0 and infinity.

The system arrives at subsequent states by treating the driver as some percentage of the cumulative sum of the differences, and the returning the index of differences at which that value can be found.

Specifically, driver is turned into a fraction by dividing it by its maximum possible value (the number of elements in differences minus 1) and then multiplying it with the total sum of differences.  The resulting value is then "found" within the array of cumulative sums of differences, and the index 

For example, start with the point [2, 1, 1, 3, 1]

driver = 2

differences = [1, 1, 3, 1]

total sum of differences = 6

cumulative sum of differences = [1, 2, 5, 6]

driver turned into fraction = 0.5 (2 / number of elements of differences)

driver * total sum of differences = 3

3 <= [1, 2, 5, 6] = 2 (first index at which value is greater than 3)

This process yields a new driver: 2.  What remains to be done is to adjust the differences in some way.  Here, I borrow from the "Statistical Feedback" algorithm, which increments each element of differences by 1 and sets the chosen index to zero.  The resulting state of the system would then be:

[2, 2, 2, 0, 2]

Typically, the system eventually ends up in a periodic orbit of some small number of states.

The goal of this project is to investigate how different initial states end up in difference periodic orbits, and also to investigate how this changes when different adjustment algorithms are used.





