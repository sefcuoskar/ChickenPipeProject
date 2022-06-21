#####################################################################################
# 03.2022 - Oskar Šefců
# .fasta of protein to multisequence alignement .fasta to something ...............
# TODO: finish docum. once finished 
#####################################################################################
# imported libraries - modeller lib and muscle.exe+lib in bin folder 
# url for modeller: https://salilab.org/modeller/download_installation.html + add to PATH
# url for muscle-5.1: https://drive5.com/muscle5/manual/install.html - get bash-file from Github and muscle.exe into the same file
import os
import shutil
import sys
from Bio.PDB import *
from modeller import *
from modeller.automodel import *
#####################################################################################
# TODO: cmd/terminal commands to estabilish working dir and global variables
path = os.path.dirname(__file__) #get a path to your current directory - .py and all fasta in same dir
os.chdir(path)
#####################################################################################
def sorting_hat(): #!not finished - might be useless
# TODO: sort .fasta in file based on different parameters and copy into a new file, possibly use blast
    for file in os.listdir(path):
        if file.startswith('ali_') and file.endswith('.fasta'):
            with open (file, "r") as open_file:
                contents = open_file.read()
                separ = contents.split('>')
                print('>' + separ[1])
                pdb_code = separ[1]
                print(pdb_code[0:4])
               
def muscle_alignment(): # for-cycle to itirate through all the .fasta files in current dir and align them
    for file in os.listdir(path):
        if file.endswith(".fasta") and not file.startswith("ali_"): # exludes all aligned files based on ali_ 
            in_file = file
            out_file = "ali_" + file 
            #command itself, can be tweaked - based on https://drive5.com/muscle5/manual/index.html
            command = path + r'\bin\muscle.exe' + " -align " + in_file + " -output " + out_file 
            # command tweaked to take muscle.exe from bin file - "file with stuff to do stuff"
            os.system(command) # runs commmand in cmd

def extract_from_fasta(position): # extracting names from fasta files - change position based on place in first line of fasta
# TODO: FILE RE-NAMING and structure changes - organization - NEED TO FINISH based on specs by ZOO
    for file in os.listdir(path):
        if file.startswith("ali_") and file.endswith(".fasta"):
            rename = open(file, "r")
            for line in rename:
                if line.startswith(">"):
                    linelst = line.split(" ")
                    print(linelst[position])
            rename.close()

# TODO: extracts DOPE numbers from all - for now is kinda useless. 
def extract_DOPE(): # extracts DOPE num from all pdb files after  automodel run 
    os.chdir(path+r'\results')
    for file in os.listdir():
        if file.endswith(".pdb"):
            extract = open(file, "r")
            for line in extract:
                if line.startswith('REMARK'):
                    lst = line.split(" ")
                    if lst[4] == 'DOPE':
                        lst1 = lst
                        DOPE = lst1[4] +" "+ lst1[6] 
                        print(str(extract.name) +' '+ DOPE)
            extract.close()

def cmp(a, b): # needed cmp from py2, don't touch - for automodeller function
    return (a > b) - (a < b)

# TODO: tweak automodeller from christos
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
                                                   
    a.make(exit_stage = 0)                                        # do the actual homology modeling; exit_stage can be changed - 0 - full modeling
                                                    # 1 - partial, creater .ini and .rsr; 2 - basic - creates only .ini file
    os.chdir(r'..\chicken_proj\results')
    ok_models = [x for x in a.outputs if x['failure'] is None]
 
    key = 'DOPE score'                              # Rank the models by DOPE score - copy pasted from modeller doc.
                                                    # key can be changed based of assess_methods used 
    if sys.version_info[:2] == (2,3):
        ok_models.sort(lambda a,b: cmp(a[key], b[key]))
    else:
        ok_models.sort(key=lambda a: a[key])

    os.chdir(path)
    m = ok_models[0]
    return ("Top model: %s (DOPE score %.3f)" % (m['name'], m[key])) 
                                                                                                         

# TODO: creation of .ali files based on 2 .pdb - can then be transformed to new .ali file with aligned .fasta seq
def pdb_alignment(code1, code2): # copy-paste from modeller website url: https://salilab.org/modeller/8v2/manual/node176.html#MEMB:alignment_x_.code
    # This demonstrates one way to generate an initial alignment between two pdb files.
    # code1 and code2 are supposed to be strings of pdb files names which are in current directory. 

    # Set Modeller environment (including search patch for model.read())
    env = Environ()
    env.io.atom_files_directory =['./', '../atom_files/']

    # Create a new empty alignment and model:
    aln = Alignment(env)
    mdl = Model(env)

    # Read the whole atom file - both can be tweaked inside the code - here - start to end
    mdl.read(file = code1, model_segment = ('FIRST:@', 'END:'))

    # Add the model sequence to the alignment
    aln.append_model(mdl, align_codes = code1, atom_files = code1)

    # Read atom file and add to alignment - same, can be tweaked here - start to end
    mdl.read(file = code2, model_segment = ('FIRST:@', 'END:'))
    aln.append_model(mdl, align_codes = code2, atom_files = code2)

    # Align them by sequence
    aln.malign(gap_penalties_1d = (-500, -300))
    aln.write(file = 'seq-' + str(code1) + '-' +str(code2) + '.ali')

    # Align them by structure
    aln.malign3d(gap_penalties_3d = (0.0, 2.0))

    # check the alignment for its suitability for modeling
    # aln.check() #? COMMENTED for now, because we shouldn't need it?? 
    # aln.write(file ='str-' + str(code1) + '-' + str(code2) + '.ali')

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
        
        # os.rmdir("obsolete") # deletes the folder obsolete which for some reason generates wiht nothing inside

# TODO: get pdb if none is present - for future but should have one 
def get_pdb(code):
    pdb1 = PDBList()
    pdb1.retrieve_pdb_file(code, pdir = './', file_format = 'pdb')
    

   
#! TEST ENVIRONMENT !#
# muscle_alignment()

# pdb_alignment(code1 = '1b5f',code2 = '1m8x')

# automodeller(alnfile_in = "seq-1b5f-1m8x.ali", knowns_in = '1m8x', end_model = 2, model = '1b5f')

# organ('1b5f')

#otestovat různě dlouhé sekvence proteinů