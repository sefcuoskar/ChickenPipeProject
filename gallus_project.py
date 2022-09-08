#####################################################################################
# Python 3.X - Oskar Šefců
#####################################################################################
# imported libraries - modeller lib and muscle.exe+lib in bin folder
# url for modeller: https://salilab.org/modeller/download_installation.html + add to PATH
# url for muscle-5.1: https://drive5.com/muscle5/manual/install.html - get bash-file from Github and muscle.exe into the same file
import os
import sys
import shutil
from Bio.PDB import *
from modeller import *
from modeller.automodel import *
#####################################################################################
# TODO: cmd/terminal commands to estabilish working dir and global variables 
path = os.getcwd() #get a path to your current directory - .py and all fasta in same dir
#####################################################################################
def sort_n_align():# TODO: merge between sorting_hat() and muscle_alignment() - works
    # TODO: SORTING_HAT - sort .fasta into separeta files  template with model and name
    for file in os.listdir(path):
        if file.endswith('.fasta'):
            ext = open(file, 'r')

            seq = ext.read() # reads file into string
            seq_split = seq.split('>'); seq_split.pop(0) # translates str into list of fasta seq

            allcode = [] # create list for all names - for naming etc.
            for x in seq_split:
                code = x.split('|', 1) # extract names between start of item in seq_split and '|' - maybe alter later
                allcode.append(code[0])

            base = len(seq_split); i = 1 # things we need for while loop; base is used for different lengths of lists

            while i < base:
                name = 'sor_' + allcode[i] # names file as the code in .fasta - might change later
                f_file = open(name, 'w')
                f_file.write('>' + seq_split[0] + '>' + seq_split[i]) # puts template seq and model seq in one file
                f_file.close()
                i += 1
    # TODO: MUSCLE_ALIGNMENT - all the .fasta files in current dir and align them + remove sor_ files
    for file in os.listdir(path):
        if file.startswith("sor_"): # sorted by 'sor_' marker from sorting_hat()
            in_file = file
            out_file = file.replace('sor_', 'ali_')
            #command itself, can be tweaked - based on https://drive5.com/muscle5/manual/index.html
            command = path + r'\bin\muscle.exe' + " -align " + in_file + " -output " + out_file
            # command tweaked to take muscle.exe from bin file - "file with stuff to do stuff"
            os.system(command) # runs commmand in cmd
            os.remove(in_file) # removes the sor_ files from dir.

# TODO: Organizer after automodeller, puts .pdb into results and deletes most of the useless files + ADD renaming based of zoo
def organ(thing):    
    for file in os.listdir(path):
        if file.startswith(thing): # all file from automodeller mover into results
            shutil.move(path+'\\'+file, path+r'\results'+'\\'+file)       
                
    path00 = path+'\\results'
    os.chdir(path00) # change dir into results
    for file in os.listdir(path00): # if it isn't pdb - i.e. results we want delete it here 
        if not file.endswith('pdb'):
            os.remove(file)

def pdb_alignment(code):
    # TODO: to obtain structure code for template - not the actual .ali file we will use
    # inspiration from modeller website url: https://salilab.org/modeller/8v2/manual/node176.html#MEMB:alignment_x_.code
    # Set Modeller environment (including search patch for model.read())
    env = Environ()
    env.io.atom_files_directory =['./', '../atom_files/']

    # Create a new empty alignment and model:
    aln = Alignment(env); mdl = Model(env)
    # Read the whole atom file - both can be tweaked inside the code - here - start to end
    mdl.read(file = code, model_segment = ('FIRST:@', 'END:'))
    # Add the model sequence to the alignment
    aln.append_model(mdl,align_codes = code, atom_files = code)
    aln.write(file = str(code) + '.ali')

    info = [] # list of all lines from .pir created - provides structural information
    with open(str(code)+'.ali', 'r') as extr:
        for line in extr:
            info.append(line)

    struct_info = info[1:3] # limits the information extracted to first 2 lines
    info = "".join(info)
    info.strip('\n')
    for file in os.listdir():

        if file.startswith('ali_'):             
            with open(file, "r") as c:
                context = c.read()
                context = ['>'+x+'*\n' for x in context.split('>') if x]
                context[0] = info
            with open (file, 'w') as d:
                context = "".join(context)
                context.strip('\n')
                d.write(context)
            outfile1 = file.replace('ali_', 'seq-')
            outfile2 = outfile1 + '-' + code + '.ali'
            os.rename(file, outfile2)               

    for file in os.listdir():
        if file.startswith('seq-'):
            with open(file, 'r') as e:
                stuff = e.readlines()  
                del stuff[0]
                name = file.replace('seq-','')
                name = name.replace('-' + code + '.ali', '')
                print(name); print(stuff)
                pos = stuff.index('>' + name + '|f\n')
                stuff[pos] = '>P1;'+name+'\n'+'sequence:::::::::\n'
                
            with open(file, 'w') as f:
                stuff = ''.join(stuff)
                f.write(stuff)

                
# TODO: get pdb if none is present
def get_pdb(code):
    pdb1 = PDBList()
    pdb1.retrieve_pdb_file(code, pdir = './', file_format = 'pdb')

def cmp(a, b): # needed cmp from py2, don't touch - for automodeller function
    return (a > b) - (a < b)

# TODO: Automodeller - adapted from website - tweaked for DOPE
def automodeller(alnfile_in, knowns_in, end_model, model): 
    # alnfile_in - input of .ali file for modeling; knowns_in - string name of pdb template file
    # end_model - number of models you want to create - generally - 5 is a good number - more takes more time...
    # model - name of the second seq in .ali file - modelled seq - will change or can be standardized to 'model' in every file.

    os.chdir(path)                                  # set work.dir. to current dir. 
    log.verbose()                                   # request verbose output
    env = Environ()                                 # create a new MODELLER environment to build this model in

    env.io.atom_files_directory = ['.', '../atom_files']
    
    a = AutoModel(
                env,
                alnfile  = alnfile_in,              # alignment filename
                knowns   = knowns_in,               # codes of the templates
                sequence = model,                   # code of the target
                assess_methods=(assess.DOPE)        # assess_methods - now DOPE, can add other - guide url: https://salilab.org/modeller/9v8/manual/node42.html
                )                                         
    a.starting_model= 1                             # index of the first model 
    a.ending_model  = end_model                     # index of the last model - input from function
                                                   
    a.make(exit_stage = 0)                          # do the actual homology modeling; exit_stage can be changed - 0 - full modeling
                                                    # 1 - partial, creater .ini and .rsr; 2 - basic - creates only .ini file
    
    ok_models = [x for x in a.outputs if x['failure'] is None]
 
    key = 'DOPE score'                              # Rank the models by DOPE score - copy pasted from modeller doc.
                                                    # key can be changed based of assess_methods used 
    if sys.version_info[:2] == (2,3):
        ok_models.sort(lambda a,b: cmp(a[key], b[key]))
    else:
        ok_models.sort(key=lambda a: a[key])

    
    m = ok_models[0]
    return ("Top model: %s (DOPE score %.3f)" % (m['name'], m[key]))
#! TEST ENVIRONMENT !#
# pdb_alignment('3s94')

# automodeller(alnfile_in = "seq-1b5f-3S94.ali", knowns_in = '1b5f', end_model = 2, model = '3S94')

# organ('1b5f')