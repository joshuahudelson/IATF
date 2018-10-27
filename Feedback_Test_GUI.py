from Tkinter import *
from Feedback_Display import Feedback_Data

class Feedback_Test_GUI:
    """ Class for displaying data from from a Feedback_Data object.
    """

    def __init__(self, master):
        """ Create all the variables for the GUI and assign them to entries,
            labels, buttons, etc.

            NOTE: The elems-by-exps grid on the left-hand side that holds the
                  numbers of unique runs per test is poorly-named--"grid."
                  Widgets are also assigned to the screen via the ".grid()"
                  method.  Change this in a future version.

            self.entry_values: the current state of the entry fields.
            self.entry_labels: the labels for the entry fields.
            self.entries: the entry field objects themselves.

            self.run_button: obvious.
            self.next_loop_button: also obvious.

            self.num_u_loops: variable for data displayed by label_unique_loops.
            self.label_unique_loops: display this run's number of unique loops.
        """

        master.title('IATF Feedback Tester')
        master.minsize(width=900, height=650)
        master.maxsize(width=900, height=650)

        self.font = ('Times', 15)
        self.font_small = ('Times', 10)
        self.font_medium = ('Times', 11)

        self.GRID_WIDTH = 4
        self.GRID_HEIGHT = 4
        self.NUM_LOOP_STATES = 10
        self.LOOP_STATES_LENGTH = 10

        self.curr_loc = (0, 0)

        # LEFT SIDE OF SCREEN --------------------------------------------------

        # Create entry fields, run button, axes, and loop-number grid
        self.names_entry_fields = ["Species", "Number of Elements", "Exponent",
                                   "Iterations", "Maximum Value", "Threshold",
                                   "Constant State", "Location"]

        self.entry_values = {"Species":"random", "Number of Elements":"4, 5, 6",
                             "Exponent":"1, 1.5, 2", "Iterations":1000, "Maximum Value":10,
                             "Threshold": 0.01, "Constant State": None, "Location":'single_value'}

        self.entry_labels = [Label(
        master, text=name, font=self.font, width=20) for name in self.names_entry_fields]

        self.entries = [Entry(master, font=self.font, width=20) for name in self.names_entry_fields]

        self.run_button = Button(master, text="Run", command= lambda : self.run_it())

        self.elem_axis = [StringVar() for i in range(self.GRID_WIDTH)]
        self.labels_elem_axis = [Label(master,
                                       textvariable=elem,
                                       font=self.font) for elem in self.elem_axis]

        self.exp_axis = [StringVar() for i in range(self.GRID_HEIGHT)]
        self.labels_exp_axis = [Label(master,
                                       textvariable=exp,
                                       font=self.font,
                                       pady=5) for exp in self.exp_axis]

        self.grid_values = [[StringVar() for i in range(self.GRID_HEIGHT)] for j in range(self.GRID_WIDTH)]

        self.grid_labels = [[Label(master,
                                   textvariable=self.grid_values[i][j],
                                   font=self.font) for j in range(self.GRID_HEIGHT)] for i in range(self.GRID_WIDTH)]

        self.custom_update = Text(master, font=self.font_small, height=6)
        temp_text = "self.differences += 1\nself.differences[value] = 0\nself.transfer_function = self.compute_transfer_function(self.differences)"
        self.custom_update.insert(END, temp_text)

        # Set the values and place the widgets on the screen.

        for i in range(len(self.entry_labels)):
            self.entry_labels[i].grid(row=i, column=0, columnspan=3)
            self.entries[i].grid(row=i, column=3, columnspan=3)
            self.entries[i].insert(0, str(self.entry_values[self.names_entry_fields[i]]))

        self.run_button.grid(row=8, column=4, columnspan=1)

        for i in range(len(self.elem_axis)):
            self.elem_axis[i].set(i)
            self.labels_elem_axis[i].grid(row=9, column=i+1)
        for i in range(len(self.exp_axis)):
            self.exp_axis[i].set(i)
            self.labels_exp_axis[i].grid(row=10+i, column=0)

        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                self.grid_values[i][j].set("_")
                self.grid_labels[i][j].grid(row=j+10, column=i+1)
                self.grid_labels[i][j].configure(width = 5, background="light gray")

        self.custom_update.grid(row=17, column=1, columnspan=5)

        # RIGHT SIDE OF SCREEN -------------------------------------------------

        # Create variables for labels.
        self.elems_in_this_test = StringVar()
        self.exp_in_this_test = StringVar()
        self.num_u_loops = StringVar()
        self.current_loop = StringVar()

        self.elems_in_this_test.set("Element: __")
        self.exp_in_this_test.set("Exponent: __")
        self.num_u_loops.set("Unique Loops: __")
        self.current_loop.set("Current Loop: 0")

        # Create the labels and buttons
        self.label_elems_in_this_test = Label(master,
                                        font=self.font,
                                        padx = 5,
                                        textvariable=self.elems_in_this_test)
        self.label_exp_in_this_test = Label(master,
                                        font=self.font,
                                        padx = 5,
                                        textvariable=self.exp_in_this_test)
        self.label_unique_loops = Label(master,
                                        font=self.font,
                                        textvariable=self.num_u_loops)
        self.label_current_loop = Label(master,
                                        font=self.font,
                                        textvariable=self.current_loop)

        self.next_test_button = Button(master, text="Next Test", command= lambda : self.display_next_test())
        self.prev_test_button = Button(master, text="Prev. Test", command= lambda : self.display_prev_test())
        self.next_loop_button = Button(master, text="Next Loop", command= lambda : self.display_next_loop())
        self.prev_loop_button = Button(master, text="Prev. Loop", command= lambda : self.display_prev_loop())

        self.loop_states = [StringVar() for i in range(self.NUM_LOOP_STATES)]
        self.loop_states_labels = [Label(master,
                                   font=self.font,
                                   textvariable=the_state) for the_state in self.loop_states]

        self.loop_indices = [StringVar() for i in range(self.NUM_LOOP_STATES)]
        self.loop_indices_labels = [Label(master, font=self.font, textvariable=the_output) for the_output in self.loop_indices]

        # Place labels and buttons.
        self.label_elems_in_this_test.grid(row=1, column=6)
        self.label_exp_in_this_test.grid(row=1, column=7)
        self.next_test_button.grid(row=2, column=7)
        self.prev_test_button.grid(row=2, column=6)
        self.label_unique_loops.grid(row=3, column=6, columnspan=2)
        self.label_current_loop.grid(row=5, column=6, columnspan=2)
        self.next_loop_button.grid(row=6, column=7)
        self.prev_loop_button.grid(row=6, column=6)

        for index, label in enumerate(self.loop_states_labels):
            label.grid(row=index+9, column = 7, columnspan=3)
        for index, label in enumerate(self.loop_indices_labels):
            label.grid(row=index+9, column = 6)

        # Helper variables
        self.test_counter = 0
        self.loop_counter = 0

    # FUNCTIONS ----------------------------------------------------------------

    def run_it(self):

        self.clear_axis_values()
        self.clear_grid_values()
        self.clear_grid_background()
        self.get_entry_values()
        self.initialize_Feedback_Data()
        self.FD.run_it()
        self.show_results()

    def clear_axis_values(self):
        for i in range(self.GRID_WIDTH):
            self.elem_axis[i].set("")
        for i in range(self.GRID_HEIGHT):
            self.exp_axis[i].set("")

    def clear_grid_values(self):
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                self.grid_values[i][j].set("")

    def clear_grid_background(self):
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                self.grid_labels[i][j].configure(background="light gray")

    def reset_stuff(self):
        pass

    def show_results(self):
        self.test_counter = 0
        self.loop_counter = 0

        self.display_elem_axis()
        self.display_exp_axis()
        self.update_grid_loc()
        self.update_by_test()
        self.display_grid()
        self.highlight_current()
        self.import_loop_states()

    def display_elem_axis(self):
        temp_len = len(self.FD.list_num_elems)
        for i in range(temp_len):
            if i < self.GRID_WIDTH:
                self.elem_axis[i].set(self.FD.list_num_elems[i])

    def display_exp_axis(self):
        temp_len = len(self.FD.list_exps)
        for i in range(temp_len):
            if i < self.GRID_HEIGHT:
                self.exp_axis[i].set(self.FD.list_exps[i])

    def update_by_test(self):
        self.elems_in_this_test.set("Element = " + str(self.entry_values["Number of Elements"][self.curr_loc[0]]))
        self.exp_in_this_test.set("Exponent = " + str(self.entry_values["Exponent"][self.curr_loc[1]]))
        self.num_u_loops.set("Unique Loops = " + \
                             str(self.FD.table_of_tests[self.curr_loc[0]]\
                                                       [self.curr_loc[1]]\
                                                       ['number unique loops']))
        print(str(self.FD.table_of_tests[self.curr_loc[0]]\
                                        [self.curr_loc[1]]\
                                        ['runs per loop percentage']))

    def display_grid(self):
        """ In each grid box, display the number of unique loops
            in that test.
        """
        temp_elems = len(self.entry_values["Number of Elements"])
        temp_exps = len(self.entry_values["Exponent"])
        for i in range(temp_elems):
            for j in range(temp_exps):
                # Entry values could exceed grid space:
                if (i < self.GRID_WIDTH) & (j < self.GRID_HEIGHT):
                    self.grid_values[i][j].set(self.FD.table_of_tests[i][j]['number unique loops'])
                else:
                    print("Number of elems or exps exceeded grid width or length!")

    def highlight_current(self):
        self.clear_grid_background()
        self.update_grid_loc()
        self.grid_labels[self.curr_loc[0]][self.curr_loc[1]].configure(background="yellow")

    def import_loop_states(self):
        """ Put the loops associated with the currently-highlighted test into
            an array for sequential viewing.
        """
        self.clear_loop_states()
        for index, state in enumerate(self.FD.table_of_tests[self.curr_loc[0]][self.curr_loc[1]]['list of loops'][self.loop_counter]):
            if index < self.LOOP_STATES_LENGTH: # Decision needed here?
                self.loop_states[index].set(state[1:])
                self.loop_indices[index].set(state[0])

    def update_grid_loc(self):
        temp_xpos = self.test_counter % len(self.entry_values["Number of Elements"])
        temp_ypos = int(self.test_counter/len(self.entry_values["Number of Elements"])) \
                    % len(self.entry_values["Exponent"])

        self.curr_loc = (temp_xpos, temp_ypos)

    def get_entry_values(self):
        print("Getting entry values...")
        for index, entry in enumerate(self.entries):
            if self.names_entry_fields[index] == "Threshold":
                self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_float(entry.get())
            elif self.names_entry_fields[index] == "Number of Elements":
                pseudolist = self.convert_string_to_int_list(entry.get())
                self.entry_values[self.names_entry_fields[index]] = pseudolist[:self.GRID_WIDTH]
            elif self.names_entry_fields[index] == "Exponent":
                pseudolist = self.convert_string_to_float_list(entry.get())
                self.entry_values[self.names_entry_fields[index]] = pseudolist[:self.GRID_HEIGHT]
            elif (self.names_entry_fields == "Iterations") | (self.names_entry_fields == "Maximum Value"):
                self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_int(entry.get())
            elif (self.names_entry_fields == "Species") | (self.names_entry_fields == "Location"):
                self.entry_values[self.names_entry_fields[index]] = entry.get()

    def initialize_Feedback_Data(self):
        self.FD = Feedback_Data(self.entry_values["Species"],
                               self.entry_values["Number of Elements"],
                               self.entry_values["Exponent"],
                               self.entry_values["Iterations"],
                               self.entry_values["Maximum Value"],
                               self.entry_values["Threshold"],
                               self.entry_values["Constant State"],
                               location_species=self.entry_values["Location"],
                               custom_update=self.custom_update.get(1.0, END))

    def clear_loop_states(self):
        """ Clear the grid entries associated with loop state sequences.
        """
        for state in self.loop_states:
            state.set("")
        for index in self.loop_indices:
            index.set("")

    def display_next_test(self):
        self.test_counter += 1
        self.update_grid_loc()
        self.highlight_current()
        self.zero_loop_counter()
        self.update_by_test()

    def display_prev_test(self):
        self.test_counter -= 1
        self.update_grid_loc()
        self.highlight_current()
        self.zero_loop_counter()
        self.update_by_test()

    def display_next_loop(self):
        """ Increment the loop counter to display the index of the new loop
            being shown.
        """
        self.loop_counter = (self.loop_counter + 1) % self.FD.table_of_tests[self.curr_loc[0]][self.curr_loc[1]]['number unique loops']
        self.current_loop.set("Current Loop: " + str(self.loop_counter) + "   "\
                               + str(self.FD.table_of_tests[self.curr_loc[0]][self.curr_loc[1]]['runs per loop percentage'][self.loop_counter]*100) + "%")
        self.import_loop_states()

    def display_prev_loop(self):
        """ Decrement the loop counter to display the index of the new loop
            being shown.  (But this doesn't show the loop yet, does it??)
        """
        self.loop_counter = (self.loop_counter - 1) % self.FD.table_of_tests[self.curr_loc[0]][self.curr_loc[1]]['number unique loops']
        self.current_loop.set("Current Loop: " + str(self.loop_counter))
        self.import_loop_states()

    def zero_loop_counter(self):
       self.loop_counter = 0
       self.current_loop.set("Current Loop: " + str(self.loop_counter) + "   "\
                              + str(self.FD.table_of_tests[self.curr_loc[0]][self.curr_loc[1]]['runs per loop percentage'][self.loop_counter]*100) + "%")
       self.import_loop_states()

    # Conversion functions -----------------------------------------------------

    def convert_string_to_int(self, string_input):
        if string_input == 'None':
            return None
        else:
            return int(string_input)

    def convert_string_to_float(self, string_input):
        if string_input == 'None':
            return None
        else:
            return float(string_input)

    def convert_string_to_int_list(self, string_input):
        temp_list = [int(i) for i in string_input.split(',')]
        print(temp_list)
        return(temp_list)

    def convert_string_to_float_list(self, string_input):
        temp_list = [float(i) for i in string_input.split(',')]
        print(temp_list)
        return(temp_list)

# END --------------------------------------------------------------------------

def main():
    root = Tk()
    obj=Feedback_Test_GUI(root) #object instantiated
    root.mainloop()

if __name__ == '__main__':
    main()
