import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, filedialog

import os
import threading
from pathlib import Path
from logger import EVAL_LOG
from logger import QUERY_LOG


class GUI:
    def __init__(self, on_submit, on_upload):
        self.root = tk.Tk()
        self.root.title("GuardRag")
        self.root.minsize(600, 400)

        self.tabControl = ttk.Notebook(self.root)

        self.mainFrame = tk.Frame(self.tabControl)
        self.logFrame = tk.Frame(self.tabControl)

        self.tabControl.add(self.mainFrame, text='Main', padding=5)
        self.tabControl.add(self.logFrame, text='Logs')
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.pack_propagate(False)

        #mainFrame
        self.on_submit = on_submit
        self.on_upload = on_upload

        self.upload_button = tk.Button(self.mainFrame, text="New File", command=self.upload)
        self.upload_button.pack(anchor="w")

        self.entry = tk.Entry(self.mainFrame, width=70)
        self.entry.pack(padx=10, pady=10, fill="x")

        self.submit = tk.Button(self.mainFrame, text="Submit", command=self.submit_query)
        self.submit.pack()

        self.entry.bind("<Return>", lambda e: self.submit_query())

        self.txt = scrolledtext.ScrolledText(self.mainFrame, height=15, wrap="word")
        self.txt.pack(padx=10, pady=10, expand=True, fill="both")

        self.evalChecked = tk.IntVar()
        self.sourceChecked = tk.IntVar()

        tk.Checkbutton(self.mainFrame, text="Run DeepEval Check",
                       variable=self.evalChecked).pack(anchor="w", side="left", pady=5)

        tk.Checkbutton(self.mainFrame, text="Show Sources",
                       variable=self.sourceChecked).pack(anchor="w", side="left", pady=5)
        
        #logFrame
        self.logContainer = tk.Frame(self.logFrame)
        self.logContainer.pack(expand=True, fill="both")



        self.txtLogQ = scrolledtext.ScrolledText(self.logContainer, height=15, wrap="word", width=40)
        self.txtLogQ.pack(side="left", expand=True, fill="both")

        self.txtLogE = scrolledtext.ScrolledText(self.logContainer, height=15, wrap="word", width=40)
        self.txtLogE.pack(side="left", expand=True, fill="both")
        
        self.txt.config(state="disabled")
        self.txtLogQ.config(state="disabled")
        self.txtLogE.config(state="disabled")

        self.logContainer.pack_propagate(False)



#functions
    def load_logs(self):
        if os.path.isfile(QUERY_LOG):
            with open(QUERY_LOG) as f:
                self.txtLogQ.config(state="normal")
                self.txtLogQ.delete("1.0", tk.END)
                self.txtLogQ.insert("end", f.read() + "\n")
                self.txtLogQ.config(state="disabled")
                self.root.update_idletasks()
        if os.path.isfile(EVAL_LOG):
            with open(EVAL_LOG) as f:
                self.txtLogE.config(state="normal")
                self.txtLogE.delete("1.0", tk.END)
                self.txtLogE.insert("end", f.read() + "\n")
                self.txtLogE.config(state="disabled")
                self.root.update_idletasks()

    def upload(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.on_upload(filepath)

    def submit_query(self):
        question = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        self.is_loading()

        self.submit["state"] = "disabled"
        self.entry["state"] = "disabled"

        run_eval=self.evalChecked.get()
        show_sources=self.sourceChecked.get()
        t1 =  threading.Thread(
            target=self.on_submit, 
            args=(
                question, 
                run_eval,
                show_sources
            )
        )

        t1.start()
        

    def print(self, text):
        self.txt.config(state="normal")
        self.txt.insert("end", text + "\n")
        self.txt.see("end")
        self.txt.config(state="disabled")
        self.root.update_idletasks()

    def run(self):
        self.root.mainloop()

    def progressive_bar(self):
        self.progressbar = ttk.Progressbar(self.mainFrame, orient=tk.HORIZONTAL, length=300)
        self.progressbar.pack(anchor="w", side="left", padx=10, fill="x")

    def update_bar(self, x):
        self.progressbar.step(x)


    def is_loading(self):
        self.progressbar = ttk.Progressbar(self.mainFrame, orient=tk.HORIZONTAL, mode="indeterminate", length=200)
        self.progressbar.pack(anchor="w", side="left", padx=10, fill="x")
        print("loading bar")
        self.progressbar.start()


    def delete_bar(self):
        self.progressbar.destroy()