import pandas as pd
from Feedback_Multi_Run import Feedback_Multi_Run_with_Condition


num_elems = 4
exp = 1
num_runs = 0
iters = 300

FMRwC_1 = Feedback_Multi_Run_with_Condition(num_elems, exp, num_runs, iters, max_value=10)

FMRwC_1.run_it(0.1)

x = pd.Series(FMRwC_1.list_of_runs[0])

print(x)
