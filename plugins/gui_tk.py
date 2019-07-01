import sys
import argparse
import tkinter as tk
from plugins.ui_base import UIBase


class LogOut(object):
    
    def __init__(self, btn_text, std, err):
        self.btn_text = btn_text
        self.std = std
        self.err = err

class GUI(tk.Tk):
    
    _config = None
    _options = {}

    def __init__(self, config, args):

        super().__init__()
        
        self._config = config
        
        self.log_out_index = 0
        self.log_out = []
             
#         self.geometry('700x500')
        self.title(self.get_config().get_app())
        
        row = 0
        for key, value in args.items():
            self._options[key] = tk.BooleanVar()
            self._options[key].initialize(value)
            self.chk_e_option = tk.Checkbutton(self, text=key, variable=self._options[key])
            self.chk_e_option.grid(row=row, columnspan=2, sticky=tk.W, padx=5)        
            row += 1

        height=6
    # create a Frame for the Text and Scrollbar
        self.txt_frm = tk.Frame(self)
        self.txt_frm.grid(row=row, column=0, columnspan=4)
        # ensure a consistent GUI size
#         self.txt_frm.grid_rowconfigure(0, weight=1)
#         self.txt_frm.grid_columnconfigure(0, weight=1)

        self.txt_log = tk.Text(self.txt_frm, height=height, width=80, borderwidth=3, relief="sunken")
        self.txt_log.trace('w', 'txt_log_changed')
        self.txt_log.grid(row=row, column=0, sticky=tk.W+tk.E+tk.N+tk.S, padx=2, pady=2)
#         self.txt_log.config(font=("consolas", 12), undo=True, wrap='word')
        self.txt_log.tag_configure("stderr", foreground="#b22222")
        
        self.log_out.append(
            LogOut(
                'log to window',
                sys.__stdout__,
                sys.__stderr__,
                )
            )
        self.log_out.append(
            LogOut(
                'log to console',
                TextRedirector(self.txt_log, "stdout"),
                TextRedirector(self.txt_log, "stderr"),
                )
            )
        
        # create a Scrollbar and associate it with txt
        self.scrollb = tk.Scrollbar(self.txt_frm, command=self.txt_log.yview)
        self.scrollb.grid(row=row, column=4, sticky=tk.W+tk.E+tk.N+tk.S)
        self.txt_log['yscrollcommand'] = self.scrollb.set
        
        row = row + height

        self.btn_toggle_log_out_text = tk.StringVar()
        self.btn_toggle_log_out_text.set(self.log_out[self.log_out_index].btn_text)
        self.btn_toggle_log_out = tk.Button(self, height=1, width=20, textvariable=self.btn_toggle_log_out_text, command=self.on_toggle_log_out)
        self.btn_toggle_log_out.grid(row=row, column=1, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        self.btn_show = tk.Button(self, height=1, width=20, text="print", command=self.print_options)
        self.btn_show.grid(row=row, column=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
        
        self.btn_start = tk.Button(self, height=1, width=20, text="start", command=self.master_destroy)
        self.btn_start.grid(row=row, column=3, sticky=tk.W+tk.E+tk.N+tk.S, padx=5, pady=5)
       
    def get_config(self):
        return self._config

    def get_args(self):
        args = {}
        for key, value in self._options.items():     # converts checkbox variable values to dictionary
            args[key] = value.get()
        return args
    
    def on_toggle_log_out(self):
        
        self.log_out_index ^= 1         # toggle index between 0 and 1
        self.btn_toggle_log_out_text.set(self.log_out[self.log_out_index].btn_text)
        sys.stdout = self.log_out[self.log_out_index].std
        sys.stderr = self.log_out[self.log_out_index].err
        
    def txt_log_changed(self):
        print('txt_log changed')

    def print_options(self):
        print('e_option: ' + str(self._options['e_option'].get()) + ', f_option: ' + str(self._options['f_option'].get()))

 
    def master_destroy(self):
        self.destroy()

class TextRedirector(object):

    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, s):
        self.widget.configure(state="normal")
        self.widget.insert("end", s, (self.tag,))
#         self.widget.configure(state="disabled")


class UI(UIBase):
    
    def execute(self):
        
        parser = argparse.ArgumentParser()
        parser.add_argument('-e', '--e_option', help='considers option e', action='store_true')
        parser.add_argument('-f', '--f_option', help='considers option f', action='store_true')
        args = vars(parser.parse_args())            # converts argparse.Namespace object to dictionary
        
        gui = GUI(self.get_config(), args)
        gui.mainloop()

        return argparse.Namespace(**gui.get_args())  # converts dictionary to argparse.Namespace 
