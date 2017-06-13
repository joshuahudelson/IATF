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




        self.x = Button(master, text="Run It")
        self.x.grid(row=7, column=0)
        self.x.configure(command = lambda : self.run_it())

        self.num_u_loops = StringVar()
        self.num_u_loops.set("Unique Loops: ")

        self.label_unique_loops = Label(master, text="Unique Loops:",
                                        font=self.font, textvariable=self.num_u_loops)
        self.label_unique_loops.grid(row=8, column=0)


    def run_it(self):
        self.get_entry_values()
        print(self.entry_values["Species"])
        self.initialize_Feedback_Data()
        self.FD.run_it()
        self.show_results()

    def show_results(self):
        self.num_u_loops.set("Unique Loops = " + str(self.FD.num_unique_loops))


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
