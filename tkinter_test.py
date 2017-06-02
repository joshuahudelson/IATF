from PIL import Image, ImageTk

from tkinter import Tk, Label, BOTH, X, Y, RIGHT, LEFT, N, Text, BooleanVar, END
from tkinter.ttk import Frame, Style, Entry, Checkbutton, Button, Scale

from IATF import IATF

class IATF_Tester:

    def __init__(self, master):
        master.title('IATF_Tester')

        self.my_IATF2 = IATF([2, 2, 2, 2])

        self.state = '[1, 1, 1, 1]'
        self.exponent = '1'
        self.driver_value = '0.75'
        self.location_value = '0'

        frame_1 = Frame(master)
        frame_1.pack(fill=X)

        label_1 = Label(frame_1, text="Starting State", width=15)
        label_1.pack(side=LEFT, padx=5, pady=5)

        self.entry_1 = Entry(frame_1)
        self.entry_1.pack(fill=X, padx=5, expand=True)
        self.entry_1.insert(0, str(self.state))
#--------
        frame_2 = Frame(master)
        frame_2.pack(fill=X)

        label_2 = Label(frame_2, text="Exponent", width=9)
        label_2.pack(side=LEFT, padx=5, pady=5)

        self.entry_2 = Entry(frame_2)
        self.entry_2.pack(fill=X, padx=5, expand=True)
        self.entry_2.insert(0, str(self.exponent))
#--------
        frame_3 = Frame(master)
        frame_3.pack(fill=X)

        label_3 = Label(frame_3, text="Input", width=6)
        label_3.pack(side=LEFT, padx=5, pady=5)

        self.entry_3 = Entry(frame_3)
        self.entry_3.pack(fill=X, padx=5, expand=True)
        self.entry_3.insert(0, str(self.driver_value))
#--------
        frame_4 = Frame(master)
        frame_4.pack(fill=X)

        label_4 = Label(frame_4, width=6)
        label_4.pack(side=LEFT, padx=5, pady=5)

        run_button = Button(master, text="Run", command=self.run_it)
        run_button.pack()
#--------
        frame_5 = Frame(master)
        frame_5.pack(fill=X)

        label_5 = Label(frame_5, text="Current State", width=15)
        label_5.pack(side=LEFT, padx=5, pady=5)

        self.entry_5 = Entry(frame_5)
        self.entry_5.pack(fill=X, padx=5, expand=True)
        self.entry_5.insert(0, str(self.state))
#--------
        frame_6 = Frame(master)
        frame_6.pack(fill=X)

        label_6 = Label(frame_6, text="Output", width=9)
        label_6.pack(side=LEFT, padx=5, pady=5)

        self.entry_6 = Entry(frame_6)
        self.entry_6.pack(fill=X, padx=5, expand=True)
        self.entry_6.insert(0, str(self.exponent))
#--------
        run_button = Button(master, text="Repeat", command=self.repeat_it)
        run_button.pack()
        frame_1 = Frame(master)
        frame_1.pack(fill=X)


    def run_it(self):

        temp_start_state = []

        self.state = self.entry_1.get()
        self.exponent = self.entry_2.get()
        self.driver_value = self.entry_3.get()

        # make own function:
        for element in self.state:
            if (element != ',') & (element != ' ') & (element != '[') & (element != ']'):
                temp_start_state.append(int(element))

        self.my_IATF = IATF(start_point_differences=temp_start_state, exponent=float(self.exponent))
        self.my_IATF.compute_next(float(self.driver_value))

        self.state = self.my_IATF.differences
        self.driver_value = self.my_IATF.index/float(len(self.state)-1)

        self.entry_5.delete(0, END)
        self.entry_5.insert(0, str(self.state))

        self.entry_6.delete(0, END)
        self.entry_6.insert(0, str(self.driver_value))

    def repeat_it(self):
        temp_start_state = []

        self.state = self.entry_5.get()
        self.exponent = self.entry_6.get()

        # make own function:
        for element in self.state:
            if (element != ',') & (element != ' ') & (element != '[') & (element != ']'):
                temp_start_state.append(int(element))

        self.my_IATF.compute_next(float(self.driver_value))

        self.state = self.my_IATF.differences
        self.driver_value = self.my_IATF.index/float(len(self.state)-1)

        self.entry_5.delete(0, END)
        self.entry_5.insert(0, str(self.state))

        self.entry_6.delete(0, END)
        self.entry_6.insert(0, str(self.driver_value))



def main():
    root = Tk()
    obj=IATF_Tester(root) #object instantiated
    root.mainloop()

if __name__ == '__main__':
    main()
