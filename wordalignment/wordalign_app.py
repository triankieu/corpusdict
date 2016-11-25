from tkinter import Tk, ttk, Label, Button, Entry, StringVar, Frame, filedialog, constants
import os
import threading


from wordalignment import run_giza

progress_marks = "|/―\\|/―\\"


def askopenfile(self, selected_file):
    file = filedialog.askopenfile(mode='r', **self.file_opt)
    if file is not None:
        selected_file.set(file.name)


def askdirectory(selected_folder):
    directory = filedialog.askdirectory(title='Select output folder',
                                        initialdir='/home/ryanhoang/PycharmProjects/corpusdictgit/data/output')

    if directory is not None:
        if not os.path.exists(directory):
            os.makedirs(directory)
        selected_folder.set(directory)


def closeform():
    global root
    root.quit()


def preprocessing():
    print('preprocessing')


def dowordalign(source, target, output):
    run_giza.dowordalignment(source, target, output)


def wordalign(master, source, target, output):
    t1 = threading.Thread(target=dowordalign, args=(master, source, target, output))
    t1.start()

    t1.join()


class WordAlignGUI:

    def __init__(self, master):
        self.master = master
        master.title("Word alignment")

        self.outlineFrame = Frame(master, relief=constants.RAISED, borderwidth=1)
        self.outlineFrame.pack(fill=constants.BOTH, expand=True)

        self.message = "Select billingual corpus"
        self.label_text = StringVar()
        self.label_text.set(self.message)
        self.label = Label(self.outlineFrame, textvariable=self.label_text)
        self.label.pack(fill=constants.X, padx=5)

        select_source_frame = Frame(self.outlineFrame)
        select_source_frame.pack(fill=constants.BOTH, padx=5)
        self.source_label = Label(select_source_frame, text='Source', width=10)
        self.source_label.pack(fill=constants.X, side=constants.LEFT, padx=5)
        self.selected_source_file = StringVar()
        self.selected_source_file.set('')
        self.source_file_entry = Entry(select_source_frame, bd=1, textvariable=self.selected_source_file)
        self.source_file_entry.pack(fill=constants.X, side=constants.LEFT, expand=True)

        button_opt = {'side': constants.LEFT, 'padx': 5, 'pady': 5}
        self.open_file_button = Button(select_source_frame, text='Select', width=7,
                                       command=lambda: askopenfile(self, self.selected_source_file)).pack(**button_opt)

        select_target_frame = Frame(self.outlineFrame)
        select_target_frame.pack(fill=constants.BOTH, padx=5)
        self.target_label = Label(select_target_frame, text='Target', width=10)
        self.target_label.pack(fill=constants.X, side=constants.LEFT, padx=5)
        self.selected_target_file = StringVar()
        self.selected_target_file.set('')
        self.target_file_entry = Entry(select_target_frame, bd=1, textvariable=self.selected_target_file)
        self.target_file_entry.pack(fill=constants.X, side=constants.LEFT, expand=True)

        button_opt = {'side': constants.LEFT, 'padx': 5, 'pady': 5}
        Button(select_target_frame, text='Select', width=7,
               command=lambda: askopenfile(self, self.selected_target_file)).pack(**button_opt)

        select_output_frame = Frame(self.outlineFrame)
        select_output_frame.pack(fill=constants.BOTH, padx=5)
        self.output_label = Label(select_output_frame, text='Output folder', width=10)
        self.output_label.pack(fill=constants.X, side=constants.LEFT, padx=5)
        self.selected_output_file = StringVar()
        self.selected_output_file.set('')
        self.output_file_entry = Entry(select_output_frame, bd=1, textvariable=self.selected_output_file)
        self.output_file_entry.pack(fill=constants.X, side=constants.LEFT, expand=True)

        button_opt = {'side': constants.LEFT, 'padx': 5, 'pady': 5}
        Button(select_output_frame, text='Select', width=7,
               command=lambda: askdirectory(self.selected_output_file)).pack(**button_opt)

        self.file_opt = options = {}
        options['defaultextension'] = '.txt'
        options['filetypes'] = [('all files', '.*'), ('text file', '.txt')]
        options['initialdir'] = '/home/ryanhoang/PycharmProjects/corpusdictgit/data'
        options['parent'] = master

        Button(master, text="Close", command=closeform).pack(side=constants.RIGHT, padx=5, pady=5)
        Button(master, text='Word align',
               command=lambda:
               wordalign(self.selected_source_file.get(), self.selected_target_file.get(),
                         self.selected_output_file.get())).pack(side=constants.RIGHT, padx=5, pady=5)
        Button(master, text='Pre-processing', command=preprocessing).pack(side=constants.RIGHT, padx=5,
                                                                          pady=5)


root = Tk()
root.update()
root.minsize(350, root.winfo_height())
my_gui = WordAlignGUI(root)
root.mainloop()
