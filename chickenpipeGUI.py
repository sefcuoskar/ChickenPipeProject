###################################################################
# 05.2022 - by Oskar Šefců 
# Graphical user interface in Tkinter lib. for chickenpipe.py project
#
# anything with extr_ in the beginning = extraction beacause tkinter doesn't like just straight input into functions
# often variables are distinguished by ___0/____01... because global/local diff to not make it confusing
###################################################################
from tkinter import *
from tkinter import ttk
import chickenpipe as cp # original file - look into documentation for list of commands
###################################################################
root = Tk() # basic setup of tkinter with title
root.title("ChickenPipeProject (CPP)") # title for the app, might be changed later

# TODO: Framing of the window, adjust to change the size 
mainframe = ttk.Frame(root, padding = "4 4 12 12")
mainframe.grid(column = 0, row = 0, sticky = (N, W, E, S))
mainframe.columnconfigure(0,weight = 1)
root.rowconfigure(0, weight = 1)

# TODO: Fetch PDB prompt if you don't have it 
def extr_get_pdb():  # extraction of str from entry using global variable
    global entry0
    entry0 = pdb_entry.get()
    cp.get_pdb(entry0)

ttk.Label(mainframe, text = 'Input pdb code:').grid(column = 1, row = 2, sticky = W)
pdb_entry = Entry(mainframe, width = 5); pdb_entry.grid(column=2, row = 2, sticky = (W,E))
ttk.Button(mainframe, text = 'Fetch PDB', command =lambda: extr_get_pdb()).grid(column = 4, row = 2, sticky = W)

# TODO: Button to a lign all fasta
ttk.Button(mainframe, text = 'Align .fasta', command = lambda: cp.muscle_alignment()).grid(column = 4, row = 4, sticky = W)

# TODO: Align two pdb into ali files
ttk.Label(mainframe, text = 'Input pdb1:pdb2'). grid(column = 1, row = 5, sticky = W)
pdb01_entry = Entry(mainframe, width = 5); pdb02_entry = Entry(mainframe, width = 5)
pdb01_entry.grid(column = 2, row = 5, sticky = (W,E)); pdb02_entry.grid(column = 3, row = 5, sticky = (W,E))

def extr_pdb_align():
    global entry01, entry02
    entry01 = pdb01_entry.get(); entry02 = pdb02_entry.get()
    cp.pdb_alignment(entry01, entry02)

ttk.Button(mainframe, text = 'Create .ali', command = lambda: extr_pdb_align()).grid(column = 4, row = 5, sticky = W)

# TODO: Automodeller inputs 
ttk.Label(mainframe, text = 'Automodeller: ').grid(row = 6,column = 1, columnspan = 2, sticky = W)
def extr_automodeller():
    global alnfile0, knowns0, end_model0, model0, result
    knowns0 = str(knowns.get()); end_model0 = int(end_model.get()); model0 = str(model.get())
    alnfile0 = str('seq-'+(model0)+'-'+(knowns0)+'.ali')
    cp.automodeller(alnfile0, knowns0, end_model0, model0)
    cp.organ(model0) # organiser, puts all pdb output from automodeller into results file

# Alnfile - input name of seq-___-___.ali file from pdb_align - might change the system later to auto input this based of pdb
# ttk.Label(mainframe, text = 'Aln_file (.ali)').grid(column = 2, row = 7, columnspan = 2, sticky = W)
# alnfile = Entry(mainframe, width = 20); alnfile.grid(column = 1, row = 7, columnspan = 1)

# Knowns_in - input pdb template name (essentialy one pdb here, the other in model)
ttk.Label(mainframe, text = 'Knowns_in pdb').grid(column = 2, row = 8, columnspan = 2, sticky = W)
knowns = Entry(mainframe, width = 20); knowns.grid(column = 1, row = 8, columnspan = 1)

# End_model - number of models you want to make - recommended 2-5 increases precision and time - the app might freeze while doing the calculation
ttk.Label(mainframe, text = 'End_model [2-5]').grid(column = 2, row = 9, columnspan = 2, sticky = W)
end_model = Entry(mainframe, width = 20); end_model.grid(column = 1, row = 9, columnspan = 1)

# Model - the second pdb file used as the modeled one 
ttk.Label(mainframe, text = 'Model pdb').grid(column = 2, row = 10, columnspan = 2, sticky = W)
model  = Entry(mainframe, width = 20); model.grid(column = 1, row = 10, columnspan = 1)

ttk.Button(mainframe, text = 'Run Automodeller', command = lambda: extr_automodeller()).grid(row = 6, column = 3, columnspan = 2, sticky = E)

# TODO: Sort all .fasta from one file into - multifiles of template + one other [1 + n]


# TODO: Text widget to output best .pdb result based of DOPE 



for child in mainframe.winfo_children():
    child.grid_configure(padx = 5, pady = 5)
root.mainloop()