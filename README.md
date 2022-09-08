# ChickenPipeProject
Author: Oskar Šefců ; sefcuo@natur.cuni.cz

Program developed to create homology models using Modeller extension, what is currently
in here is manual version, part of explanation is in the code itself. 
On a later date I will hopefully add a guide on how to operate the whole program and
how to modify parametrs. 

Basic setup:
create a directory in which you will have - 
bin - a directory containing Muscle and Modeller - exact instructions to install both are on their 
      respective web pages, but at least muscle.exe file needs to be in. 
results - a directory for final .pdb results after modeling is done - rest of temporary files will be 
          deleted, this is just organizational so results and used files don't mix
gallus_project.py - 'brains' behind the operation, allow modularity - this i will add later, 
                      DO NOT touch for now...
gallus_projectGUI.py - graphical user interface using tkinter, start the program using this, several functions
                      Fetch pdb - downloads pdb just by code so you don't have to search simply input pdb code
                      Sort and align - main function - aligns files of data using muscle and sorts them into separete files
                      Create .ali - creates template.ali file and sub files containg aligned sequence and template sequence
                                    into ready to use .ali/.pir format
                      Run automodeller - last part, homology modeling itself - name of template - pdb code of template sequence;
                                          end model - number of models you want to do - min is 2 max is whatever you want - 5 is 
                                          suggestion because beyond that is kind od useless and takes too long;
                                          Modeled sequence - name/code or whatever that you find in the .ali file as 
                                          P1 sequence name - don't create complicated names they tend to break stuff
DATA - you start with simple .fasta file, first sequence has to be the template on, the one you have a pdb of
       or will download using fetch pdb of. Naming in the file is also kinda given but is one of the modular things
       Basically the name is anything between '>' and '|f' in the header of sequence... don't ask I am still working on 
       improving this part
       
HOW TO USE:
Well... you get your fasta nice and setup as the one shown in here, all programs and files donwloaded. 
I suggest also getting Pymol/vmd or alternative to view resulting pdb.
You start the program by clicking on gallus_projectGUI.py at which point a small interactiv window should pop-up
instructions on what does what are above, so you start making your way down, next to this a terminal will open up 
I suggest working with window+terminal+open file directory triple setup so you can see what is happening
Also the terminal is good for diagnosing problems with either program or the input sequence. 
When you finish the homology modeling it will also print a little prompt on which file has the best 
DOPE score - usefull info - don't know hot show it in the GUI yet.. :( 

So yeah that is basically it, you get the results - check which has the best DOPE, open it up in your pdb viewer of choice
and you are done. Hope this was somewhat helpfull. 
        





