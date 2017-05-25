from IATF import IATF
from IATF_Runner import IATF_Runner


elems = [5]

exp = 1

starting_points = [[1, 1, 1, 1, 1]]
init_drivers = [0.5]

# starting_points and init_drivers must be the same length

driver_species = 'feedback'
     
driver_list = None

iters = 200

stop_if_looping = True

#-----------------

test_iatfs = [IATF(s_p, exp) for s_p in starting_points]

list_list_concat_diffs = []
list_loop_indices = []

for _ in range(len(test_iatfs)):
    tester = IATF_Runner(test_iatfs[_], iters, init_drivers[_], driver_species, stop_if_looping, driver_list)
    tester.run_it()
    list_list_concat_diffs.append(tester.list_concat_differences)
    list_loop_indices.append(tester.loop_index)

for _ in range(len(list_list_concat_diffs)):
    counter = 0
    print()
    print("Test Run #" + str(_))
    for element in list_list_concat_diffs[_]:
        if counter == list_loop_indices[_]:
            print("Loop:")
        print(str(element[0]) + '\t' + str(element[1:]))
        counter += 1
