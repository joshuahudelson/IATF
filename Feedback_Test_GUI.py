from tkinter import *
from Feedback_Display import Feedback_Data

class Feedback_Test_GUI:
    """ Class for displaying data from from a Feedback_Data object.
    """

    def __init__(self, master):
        """
            self.entry_values: the current state of the entry fields.
            self.entry_labels: the labels for the entry fields.
            self.entries: the entry field objects themselves.

            self.run_button: obvious.
            self.next_loop_button: also obvious.

            self.num_u_loops: variable for data displayed by label_unique_loops.
            self.label_unique_loops: display this run's number of unique loops.
        """

        master.title('IATF_Tester')

        self.font = ('Times', 15)
        self.font_small = ('Times', 10)

        self.GRID_WIDTH = 5
        self.GRID_HEIGHT = 15

# LEFT SIDE OF SCREEN:

        # Create entry fields, run button, axes, and loop-number grid

        self.names_entry_fields = ["Species", "Number of Elements", "Exponent",
                                   "Iterations", "Maximum Value", "Threshold",
                                   "Constant State"]

        self.entry_values = {"Species":"random", "Number of Elements":4,
                             "Exponent":1, "Iterations":1000, "Maximum Value":10,
                             "Threshold": 0.001, "Constant State": None}

        self.entry_labels = [Label(
        master, text=name, font=self.font, width=20) for name in self.names_entry_fields]

        self.entries = [Entry(master, font=self.font, width=20) for name in self.names_entry_fields]

        self.run_button = Button(master, text="Run It", command= lambda : self.run_it())

        self.elem_axis = [StringVar() for i in range(5)]
        self.labels_elem_axis = [Label(master,
                                       textvariable=elem,
                                       font=self.font) for elem in self.elem_axis]

        self.exp_axis = [StringVar() for i in range(15)]
        self.labels_exp_axis = [Label(master,
                                       textvariable=exp,
                                       font=self.font, pady=5) for exp in self.exp_axis]

        self.grid_values = [[StringVar() for i in range(5)] for j in range(15)]

        self.grid_labels = [[Label(master, textvariable=self.grid_values[i][j],
                                   font=self.font) for j in range(5)] for i in range(15)]

# Set the values and place the stuff.

        for i in range(len(self.entry_labels)):
            self.entry_labels[i].grid(row=i, column=0, columnspan=3)
            self.entries[i].grid(row=i, column=3, columnspan=3)
            self.entries[i].insert(0, str(self.entry_values[self.names_entry_fields[i]]))

        self.run_button.grid(row=7, column=0, columnspan=3)

        for i in range(len(self.elem_axis)):
            self.elem_axis[i].set(i)
            self.labels_elem_axis[i].grid(row=8, column=i+1)
        for i in range(len(self.exp_axis)):
            self.exp_axis[i].set(i)
            self.labels_exp_axis[i].grid(row=9+i, column=0)

        for i in range(15):
            for j in range(5):
                self.grid_values[i][j].set("_")
                self.grid_labels[i][j].grid(row=i+9, column=j+1)
                self.grid_labels[i][j].configure(width = 5, background="red")

#RIGHT SIDE OF SCREEN:
    # TOP:
        # Create variables for labels.
        self.test_number = StringVar()
        self.elems_in_this_test = StringVar()
        self.exp_in_this_test = StringVar()
        self.num_u_loops = StringVar()
        self.current_loop = StringVar()

        self.test_number.set("Test #: ")
        self.elems_in_this_test.set("Elements: ")
        self.exp_in_this_test.set("Exponent: ")
        self.num_u_loops.set("Unique Loops: ")
        self.current_loop.set("Current Loop: ")

        # Create the labels and buttons
        self.label_test_number = Label(master,
                                        font=self.font,
                                        textvariable=self.test_number)
        self.label_elems_in_this_test = Label(master,
                                        font=self.font,
                                        textvariable=self.elems_in_this_test)
        self.label_exp_in_this_test = Label(master,
                                        font=self.font,
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

        self.loop_states = [StringVar() for i in range(20)]
        self.loop_states_labels = [Label(master,
                                   font=self.font,
                                   textvariable=the_state) for the_state in self.loop_states]

        # Place labels and buttons.
        self.label_test_number.grid(row=0, column=6, columnspan=2)
        self.label_elems_in_this_test.grid(row=1, column=6)
        self.label_exp_in_this_test.grid(row=1, column=7)
        self.label_unique_loops.grid(row=2, column=6, columnspan=2)
        self.next_test_button.grid(row=3, column=6)
        self.prev_test_button.grid(row=3, column=7)
        self.label_current_loop.grid(row=5, column=6, columnspan=2)
        self.next_loop_button.grid(row=6, column=6)
        self.prev_loop_button.grid(row=6, column=7)

        for index, label in enumerate(self.loop_states_labels):
            label.grid(row=index+9, column = 6, columnspan=4)

#--------------------------------

        self.test_counter = 0
        self.loop_counter = 0

    def clear_grid_values(self):
        for i in range(self.GRID_HEIGHT):
            for j in range(self.GRID_WIDTH):
                self.grid_values[i][j].set("")

    def clear_grid_background(self):
        for i in range(self.GRID_HEIGHT):
            for j in range(self.GRID_WIDTH):
                self.grid_labels[i][j].configure(background="gray")

    def clear_axis_values(self):
        for i in range(self.GRID_WIDTH):
            self.elem_axis[i].set("")
        for i in range(self.GRID_HEIGHT):
            self.exp_axis[i].set("")

    def reset_stuff(self):
        pass

    def run_it(self):

        self.clear_axis_values()
        self.clear_grid_values()
        self.clear_grid_background()
        self.get_entry_values()
        self.initialize_Feedback_Data()
        self.FD.run_it()
        self.show_results()

    def show_results(self):
        self.num_u_loops.set("Unique Loops = " + str(self.FD.num_unique_loops))
        self.display_elem_axis()
        self.display_exp_axis()
        self.display_grid()
        self.test_counter = 0
        self.loop_counter = 0
        self.highlight_current()
        self.import_loops()



    def highlight_current(self):
        self.clear_grid_background()

        temp_ypos = int(self.test_counter/len(self.FD.list_num_elems)) % len(self.FD.list_exps)
        temp_xpos = self.test_counter % len(self.FD.list_num_elems)

        self.grid_labels[temp_ypos][temp_xpos].configure(background="yellow")

        self.grid_loc_tuple = (temp_ypos, temp_xpos)

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

    def display_grid(self):
        temp_rows = len(self.entry_values["Exponent"])
        temp_cols = len(self.entry_values["Number of Elements"])
        for i in range(temp_rows):
            for j in range(temp_cols):
                if (i < self.GRID_HEIGHT) & (j < self.GRID_WIDTH):
                    self.grid_values[i][j].set(self.FD.mem_list_num_loops[j][i]) # j and i reversed in Feedback Display because dumb coding.

    def clear_loop_states(self):
        for state in self.loop_states:
            state.set("")

    def import_loops(self):
        self.clear_loop_states()
        for index, state in enumerate(self.FD.mem_list_loops[self.grid_loc_tuple[1]][self.grid_loc_tuple[0]][self.loop_counter]):
            if index < 18:
                self.loop_states[index].set(state)

    def display_next_loop(self):
        self.loop_counter = (self.loop_counter + 1) % len(self.loop_states)
        self.current_loop.set(self.loop_counter)

    def display_prev_loop(self):
        self.loop_counter = (self.loop_counter - 1) % len(self.loop_states)
        self.current_loop.set(self.loop_counter)

    def display_next_test(self):
        self.test_counter += 1
        self.highlight_current()

    def display_prev_test(self):
        self.test_counter -= 1
        self.highlight_current()

    def get_entry_values(self):
        for index, entry in enumerate(self.entries):
            print("did it")
            if self.names_entry_fields[index] == "Threshold":
                self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_float(entry.get())
            elif self.names_entry_fields[index] == "Number of Elements":
                self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_int_list(entry.get())
            elif self.names_entry_fields[index] == "Exponent":
                self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_float_list(entry.get())
            elif (self.names_entry_fields == "Iterations") | (self.names_entry_fields == "Maximum Value"):
                self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_int(entry.get())


    def initialize_Feedback_Data(self):
        self.FD = Feedback_Data(self.entry_values["Species"],
                               self.entry_values["Number of Elements"],
                               self.entry_values["Exponent"],
                               self.entry_values["Iterations"],
                               self.entry_values["Maximum Value"],
                               self.entry_values["Threshold"],
                               self.entry_values["Constant State"])


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
#--------------

def main():
    root = Tk()
    obj=Feedback_Test_GUI(root) #object instantiated
    root.mainloop()

if __name__ == '__main__':
    main()
