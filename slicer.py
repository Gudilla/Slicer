import tkinter as tk
from tkinter import messagebox
from meshcut import Slicer, Figure3D 

class MainWindow:
    SPACER = 5

    def loop(self):
        self.window.mainloop()
    
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()

    def slice_button_pressed(self):
        self.lbl_info.config(text='      PLEASE WAIT.....     ')
        slicer = Slicer()
        slicer.filename = self.ent_filename.get()
        slicer.step = int(self.ent_step.get())
        slicer.dpi = int(self.ent_dpi.get())
        slicer.slice_stl()
        del slicer
        self.lbl_info.config(text='Successfully sliced! :)')

    def show_btn_pressed(self):
        figure = Figure3D(self.ent_filename.get())
        figure.show_figure()

    def __init__(self):
        self.window = tk.Tk()
        self.window.title('SLICER beta')
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        frm_form = tk.Frame(master=self.window)
        frm_form.grid(row=0)

        lbl_filename = tk.Label(master=frm_form, text='Filename:')
        self.ent_filename = tk.Entry(master=frm_form, width=30)
        lbl_filename.grid(row=0, column=0, sticky='w')
        self.ent_filename.grid(row=0, column=1)

        lbl_step = tk.Label(master=frm_form, text='Step:')
        self.ent_step = tk.Entry(master=frm_form, width=30)
        self.ent_step.insert(string='10', index=0)
        lbl_step.grid(row=1, column=0, sticky='w')
        self.ent_step.grid(row=1, column=1)

        lbl_dpi = tk.Label(master=frm_form, text='DPI:')
        self.ent_dpi = tk.Entry(master=frm_form, width=30)
        self.ent_dpi.insert(string='1000', index=0)
        lbl_dpi.grid(row=2, column=0, sticky='w')
        self.ent_dpi.grid(row=2, column=1)

        frm_buttons = tk.Frame(master=self.window)
        frm_buttons.grid(row=1, column=0)

        btn_slice = tk.Button(master=frm_buttons, text='SLICE !', command=self.slice_button_pressed)
        btn_slice.grid(row=0, column=0, padx=self.SPACER, pady=self.SPACER)

        btn_show = tk.Button(master=frm_buttons, text='Show figure', command=self.show_btn_pressed)
        btn_show.grid(row=0, column=1, padx=self.SPACER, pady=self.SPACER)

        #btn_save_settings = tk.Button(master=frm_buttons, text='Save settings')
        #btn_save_settings.grid(row=0, column=2, padx=self.SPACER, pady=self.SPACER)

        self.lbl_info = tk.Label(master=frm_buttons, text='Input filename and step')
        self.lbl_info.grid(row=1, column=0, columnspan=3)
    
main = MainWindow()
main.loop()