from tkinter import *
from Feedback_Display import Feedback_Data

class Feedback_Test_GUI:

    def __init__(self, master):

        master.title('IATF_Tester')

        self.font = ('Times', 15)
        self.font2 = ('Times', 10)
        """
                self,
                 species,
                 num_elems,
                 exponent,
                 iters,
                 max_value,
                 threshold,
                 constant_state):
                 """

        self.names_entry_fields = ["Species", "Number of Elements", "Exponent",
                                   "Iterations", "Maximum Value", "Threshold",
                                   "Constant State"]

        self.entry_values = {"Species":"random", "Number of Elements":4, "Exponent":1,
                      "Iterations":1000, "Maximum Value":10, "Threshold": 0.001,
                      "Constant State": None}

        self.entry_labels = [Label(
        master, text=name, font=self.font) for name in self.names_entry_fields]

        self.entries = [Entry(master, font=self.font) for name in self.names_entry_fields]

        for i in range(len(self.entry_labels)):
            self.entry_labels[i].grid(row=i, column=0)
            self.entries[i].grid(row=i, column=1)
            self.entries[i].insert(0, str(self.entry_values[self.names_entry_fields[i]]))


        self.x = Button(master, text="Run It", command= lambda : self.run_it())
        self.x.grid(row=7, column=0)

        self.loop_counter = 0

        self.y = Button(master, text="Next Loop", command= lambda : self.display_next_loop())
        self.y.grid(row=7, column=1, columnspan = 2)

        self.num_u_loops = StringVar()
        self.num_u_loops.set("Unique Loops: ")

        self.label_unique_loops = Label(master,
                                        font=self.font, textvariable=self.num_u_loops)
        self.label_unique_loops.grid(row=8, column=0)

        self.current_loop = StringVar()
        self.current_loop.set(0)

        self.label_current_loop = Label(master, font=self.font, textvariable=self.current_loop)
        self.label_current_loop.grid(row=8, column = 1)

        self.list_results = [StringVar() for i in range(9)]
        self.list_result_labels = [Label(master, font=self.font, textvariable=the_result) for the_result in self.list_results]
        for index, label in enumerate(self.list_result_labels):
            label.grid(row=index+9, column=0)

        self.loop_states = [StringVar() for i in range(18)]
        self.loop_states_labels = [Label(master, font=self.font, textvariable=the_state) for the_state in self.loop_states]
        for index, label in enumerate(self.loop_states_labels):
            label.grid(row=index+9, column = 1)

    def run_it(self):
        self.get_entry_values()
        print(self.entry_values["Species"])
        self.initialize_Feedback_Data()
        self.FD.run_it()
        self.show_results()
        self.display_next_loop()

    def show_results(self):
        self.num_u_loops.set("Unique Loops = " + str(self.FD.num_unique_loops))
        counter = 0
        for index, loop in enumerate(self.FD.list_loops):
            self.list_results[counter].set("Loop " + str(index) + ": " + str(self.FD.lens_unique_loops[index]))
            counter += 1

    def display_next_loop(self):
        self.loop_counter = (self.loop_counter + 1) % len(self.FD.list_loops)
        self.current_loop.set(self.loop_counter)
        for state in self.loop_states:
            state.set("")
        for index, state in enumerate(self.FD.list_loops[self.loop_counter]):
            if index < 18:
                self.loop_states[index].set(self.FD.list_loops[self.loop_counter][index][1:])


    def get_entry_values(self):
        for index, entry in enumerate(self.entries):
            if self.names_entry_fields[index] != "Species":
                if self.names_entry_fields[index] == "Threshold":
                    self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_float(entry.get())
                else:
                    self.entry_values[self.names_entry_fields[index]] = self.convert_string_to_int(entry.get())


    def initialize_Feedback_Data(self):
        self.FD = Feedback_Data(self.entry_values["Species"],
                               [self.entry_values["Number of Elements"]],
                               [self.entry_values["Exponent"]],
                               self.entry_values["Iterations"],
                               self.entry_values["Maximum Value"],
                               self.entry_values["Threshold"],
                               self.entry_values["Constant State"])
        print(self.FD.iters)


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

#--------------

def main():
    root = Tk()
    obj=Feedback_Test_GUI(root) #object instantiated
    root.mainloop()

if __name__ == '__main__':
    main()
