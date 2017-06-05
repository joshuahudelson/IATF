# IATF_Demo_GUI
from tkinter import *
from IATF import IATF


class IATF_Tester:

    def __init__(self, master):
        master.title('IATF_Tester')

        self.font = ('Times', 20)

        self.list_of_entry_names = ['Starting State', 'Exponent', 'Input',
                                    'Location', 'Epsilon', 'Output']

        self.list_of_button_names = ['Initialize', 'Run', 'Feedback', 'Clear']

        self.list_of_entry_order = [0, 1, 3, 4, 5, 7]

        self.list_of_button_order = [2, 6, 8, 9]

        self.list_of_values = {'Starting State':[1, 1, 1, 1],
                               'Exponent':1,
                               'Input':0,
                               'Location':0,
                               'Epsilon':0.0,
                               'Output':None}

        self.entries = []
        self.buttons = []
        self.labels_left = []

        for i in range(len(self.list_of_entry_names)):
            self.labels_left.append(Label(master, text=self.list_of_entry_names[i],
                                     width=15, font=self.font, padx=5, pady=10))
            self.labels_left[i].grid(row=self.list_of_entry_order[i], column=0)

            self.entries.append(Entry(master, font=self.font))
            self.entries[i].grid(row=self.list_of_entry_order[i], column = 1)

        for i in range(len(self.list_of_button_names)):
            self.buttons.append(Button(master, text=self.list_of_button_names[i]))
            self.buttons[i].grid(row=self.list_of_button_order[i], column = 1)

        self.buttons[0].configure(command = lambda: self.initialize_it(master))
        self.buttons[1].configure(command = lambda: self.run_it(master))
        self.buttons[2].configure(command = lambda: self.feedback(master))
        self.buttons[3].configure(command = lambda: self.clear_list_of_states())



        self.list_of_states = [StringVar() for _ in range(len(self.list_of_entry_names) + \
                                                          len(self.list_of_button_names))]

        self.list_of_output = [StringVar() for _ in range(len(self.list_of_entry_names) + \
                                                          len(self.list_of_button_names))]

        self.list_of_labels_right = []
        self.list_of_labels_right_right = []


        # This binds the state to the label
        for i, state in enumerate(self.list_of_states):
            self.list_of_labels_right.append(Label(master, textvariable=state,
                                 width=15, font=self.font, padx=5, pady=10))
            self.list_of_labels_right[i].grid(row=i, column=3)

        for i, output in enumerate(self.list_of_output):
            self.list_of_labels_right_right.append(Label(master, textvariable=output,
                                 width=10, font=self.font, padx=5, pady=10))
            self.list_of_labels_right_right[i].grid(row=i, column=4)

        self.update(master)


    def update(self, master):

        for i, entry in enumerate(self.entries):
            entry.delete(0, END)
            entry.insert(0, str(self.list_of_values[self.list_of_entry_names[i]]))


    def get_values(self):
        self.list_of_values['Starting State'] = self.convert_string_to_list(self.entries[0].get())
        self.list_of_values['Exponent'] = self.convert_string_to_float(self.entries[1].get())
        self.list_of_values['Input'] = self.convert_string_to_int(self.entries[2].get())
        self.list_of_values['Location'] = self.convert_string_to_int(self.entries[3].get())
        self.list_of_values['Epsilon'] = self.convert_string_to_float(self.entries[4].get())
        self.list_of_values['Output'] = self.convert_string_to_int(self.entries[5].get())


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


    def convert_string_to_list(self, string_input):
        if string_input == 'None':
            return None
        else:
            temp_string = []
            for element in string_input:
                if (element != ',') & (element != ' ') & (element != '[') & (element != ']'):
                    temp_string.append(int(element))
            return temp_string


    def push_to_output(self, output):
        for i in range(len(self.list_of_output)):
            if i == len(self.list_of_output)-1:
                self.list_of_output[i].set(output)
            else:
                self.list_of_output[i].set(self.list_of_output[i+1].get())

    def push_to_states(self, state):
        for i in range(len(self.list_of_states)):
            if i == len(self.list_of_states)-1:
                self.list_of_states[i].set(state)
            else:
                self.list_of_states[i].set(self.list_of_states[i+1].get())

    def initialize_it(self, master):
        self.get_values()

        temp_state = self.convert_string_to_list(self.list_of_values['Starting State'])

        self.my_IATF = IATF(start_point_differences=temp_state,
                            exponent=float(self.list_of_values['Exponent']))

        self.push_to_states(self.my_IATF.differences)
        self.push_to_output(self.list_of_values['Input'])


    def run_it(self, master):
        self.get_values()

        self.my_IATF.compute_next(float(self.list_of_values['Input']/float(len(self.list_of_values['Starting State']) - 1)),
                                  location = self.list_of_values['Location'],
                                  epsilon=self.list_of_values['Epsilon'])

        self.list_of_values['Output'] = self.my_IATF.index

        self.update(master)

        self.push_to_states(self.my_IATF.differences)
        self.push_to_output(self.my_IATF.index)


    def feedback(self, master):
        self.get_values()

        self.my_IATF.compute_next(float(self.list_of_values['Output']/float(len(self.list_of_values['Starting State']) - 1)),
                                  location = self.list_of_values['Location'],
                                  epsilon=self.list_of_values['Epsilon'])

        self.list_of_values['Output'] = self.my_IATF.index

        self.update(master)

        self.push_to_states(self.my_IATF.differences)
        self.push_to_output(self.my_IATF.index)


    def clear_list_of_states(self):
        for element in self.list_of_states:
            element.set('')
        for output in self.list_of_output:
            element.set('')


#-----------------

def main():
    root = Tk()
    obj=IATF_Tester(root) #object instantiated
    root.mainloop()

if __name__ == '__main__':
    main()
