# Iteratively-Adjusted Transfer Functions
-------------------------

## Introduction

The goal of this project is to investigate how different initial states end up in different periodic orbits, and also to investigate how this changes when different adjustment algorithms are used.

Consider a point in n-dimensional space `[a, b, ..., z]` that describes the state of a system. The term at index 0 ("a") will be called the "driver," while the remaining terms ("b" through "z") will be called the "differences."

The driver will always be a value between 0 and the number of elements in differences minus 1. The values of differences, are non-negative reals.

The system arrives at subsequent states by treating the driver as some percentage of the cumulative sum of the differences, and returning the indices of differences at which that value can be found.

Specifically, driver is turned into a fraction by dividing it by its maximum possible value (the number of elements in differences minus 1) and then multiplying it with the total sum of differences.  The resulting value is then "found" within the array of cumulative sums of differences, and the index is returned.

The previous discussion is mainly relevant to the `Feedback_Multi_Runs` class.

## Example run

Start with the point [2, 1, 1, 3, 1], where

```
driver = 2
num_differences = 4
differences = [1, 1, 3, 1]
total_diff_sum = 6
cumulative_diff_sum = [1, 2, 5, 6]
```

The fractional value derived from `driver` is
```
frac_driver = driver / num_differences # 0.5.
```

The percentage of cumulative differences is then
```
percentage = frac_driver * total_diff_sum # 3
```

Now we look for the first element in `cumulative_diff_sum` whose corresponding value is greater than `percentage`, in this case it's `2`.

This process yields a new driver: `2`.  What remains to be done is to adjust the differences in some way.  Here, I borrow from the "Statistical Feedback" algorithm, which increments each element of differences by 1 and sets the chosen index to zero.  The resulting state of the system would then be: `[2, 2, 2, 0, 2]`.

Typically, the system eventually ends up in a periodic orbit of some small number of states.
