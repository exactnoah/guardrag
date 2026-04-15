import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext, filedialog
from tkinter.messagebox import showinfo

import os
import threading
from pathlib import Path
from logger import EVAL_LOG
from logger import QUERY_LOG
from evaluation import set_metrics


class GUI:
    def __init__(self, on_submit, on_upload, on_start):
        self.root = tk.Tk()
        self.root.title("GuardRag")
        self.root.minsize(600, 400)

        #Menubar
        self.menubar = tk.Menu(self.root)

        self.file = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.file)
        self.file.add_command(label="Add File", command=self.upload)
        self.file.add_command(label="Delete File", command=self.delete_file)


        self.root.config(menu=self.menubar)

        #tabs initialization
        self.tabControl = ttk.Notebook(self.root)

        self.mainFrame = tk.Frame(self.tabControl)
        self.logFrame = tk.Frame(self.tabControl)
        self.docsFrame = tk.Frame(self.tabControl)
        self.evalFrame = tk.Frame(self.tabControl)

        self.tabControl.add(self.mainFrame, text='Main', padding=5)
        self.tabControl.add(self.logFrame, text='Logs', padding=5)
        self.tabControl.add(self.docsFrame, text='Docs', padding=5)
        self.tabControl.add(self.evalFrame, text='Settings')
        self.tabControl.pack(expand=1, fill="both")

        #mainFrame
        self.on_submit = on_submit
        self.on_upload = on_upload
        self.on_start = on_start

        self.entry = tk.Entry(self.mainFrame, width=70)
        self.entry.pack(padx=10, pady=10, fill="x")

        self.submit = tk.Button(self.mainFrame, text="Submit", command=self.submit_query)
        self.submit.pack()

        self.entry.bind("<Return>", lambda e: self.submit_query())

        self.txt = scrolledtext.ScrolledText(self.mainFrame, height=15, wrap="word")
        self.txt.pack(padx=10, pady=10, expand=True, fill="both")
        self.txt.config(state="disabled")

        self.evalChecked = tk.IntVar()
        self.sourceChecked = tk.IntVar()

        tk.Checkbutton(self.mainFrame, text="Run DeepEval Check",
                       variable=self.evalChecked).pack(anchor="w", side="left", pady=5)

        tk.Checkbutton(self.mainFrame, text="Show Sources",
                       variable=self.sourceChecked).pack(anchor="w", side="left", pady=5)
        
        #logFrame
            #
        self.logTabControl = ttk.Notebook(self.logFrame)

        self.queryLogFrame = tk.Frame(self.logTabControl)
        self.evalLogFrame = tk.Frame(self.logTabControl)
        self.logTabControl.add(self.queryLogFrame, text='Queries', padding=5)
        self.logTabControl.add(self.evalLogFrame, text='Evaluations', padding=5)

        self.logTabControl.pack(expand=1, fill="both")



        

        self.queryLabel = tk.Label(self.queryLogFrame, text="Query Log", font=("Arial", 14))
        self.queryLabel.pack()

        self.evalLabel = tk.Label(self.evalLogFrame, text="Eval Log", font=("Arial", 14))
        self.evalLabel.pack()

        self.txtLogQ = scrolledtext.ScrolledText(self.queryLogFrame, height=15, wrap="word", width=40)
        self.txtLogQ.pack(expand=True, fill="both")

        self.txtLogE = scrolledtext.ScrolledText(self.evalLogFrame, height=15, wrap="word", width=40)
        self.txtLogE.pack(expand=True, fill="both")
        
        self.txtLogQ.config(state="disabled")
        self.txtLogE.config(state="disabled")


        #docs pag

        self.docLabel = tk.Label(self.docsFrame, text="Loaded Documents", font=("Arial", 14)).pack()
    
        self.txtDocs = scrolledtext.ScrolledText(self.docsFrame, height=15, wrap="word", width=40, state="disabled")
        self.txtDocs.pack(expand=True, fill="both")


        #evalFrame
        tk.Label(self.evalFrame, text="Faithfulness Threshold").pack(anchor="w", padx=10, pady=(10,0))
        self.faithfulnessScale = tk.Scale(self.evalFrame, from_=0, to=1, resolution=0.05, orient="horizontal", length=300)

        self.faithfulnessScale.set(0.75)
        self.faithfulnessScale.pack(anchor="w", padx=10)
        faithfulness_hint = tk.Frame(self.evalFrame, width=300, height=30)
        faithfulness_hint.pack(anchor="w", padx=10)
        faithfulness_hint.pack_propagate(False)
        tk.Label(faithfulness_hint, text="← More hallucinations allowed", fg="gray").pack(side="left")
        tk.Label(faithfulness_hint, text="Stricter →", fg="gray").pack(side="right")

        tk.Label(self.evalFrame, text="Answer Relevancy Threshold").pack(anchor="w", padx=10, pady=(10,0))
        self.relevancyScale = tk.Scale(self.evalFrame, from_=0, to=1, resolution=0.05, orient="horizontal", length=300)

        self.relevancyScale.set(0.75)
        self.relevancyScale.pack(anchor="w", padx=10)
        relevancy_hint = tk.Frame(self.evalFrame, width=300, height=30)
        relevancy_hint.pack(anchor="w", padx=10)
        relevancy_hint.pack_propagate(False)
        tk.Label(relevancy_hint, text="← Off-topic answers allowed", fg="gray").pack(side="left")
        tk.Label(relevancy_hint, text="Stricter →", fg="gray").pack(side="right")

        tk.Button(self.evalFrame, text="Apply", command=self.apply_thresholds).pack(anchor="w", padx=10, pady=10)





#functions
    def print_docs(self, docsList):
        self.txtDocs.config(state="normal")
        for doc in docsList:
            filename = doc.meta.get("filename", "Unknown")
            self.txtDocs.insert("end", filename + "\n")
            
        self.txtDocs.config(state="disabled")
        


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

            filename = os.path.basename(filepath)
            showinfo("File Added", f"File: '{filename}' added to docs folder successfully. New doc will be integrated alongside next query.")

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

    def start_load(self):
        t = threading.Thread(target= self.on_start)
        t.start()

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
    

    def apply_thresholds(self):
        set_metrics(
            faithfulness=self.faithfulnessScale.get(),
            relevancy=self.relevancyScale.get()
        )


    def delete_file(self):
        print("gui.delete_file")
        DIR = LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "docs")
        if DIR:
            print(DIR)
            filename = filedialog.askopenfilename(initialdir=DIR)
            print(filename)
            os.remove(filename)