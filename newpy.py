#!/usr/bin/python3 

VV=False;
###<HEADER_>==================================================================#
__doc__='''
#==============================================================================
* File:    FILENAME
* Purpose: 
* Options:
    [-doc] 
    [-log] 
    [-inp] 

# @author: Daniel.Collins@
# @last:   2026-10-19-0000s
# Keywords: #Python; #Keywords 
#==============================================================================
'''
__version__={
  261019.0000:'''+ initial ''',
}
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In[000.002]: Load packages
####  Import configurations
import platform;
import os;
from   os import listdir;
import shutil; 
import string ;
import math ;
import re ;
import linecache ;
import argparse ;
import statistics ;
import pandas as pd ;
import numpy as np ;
import matplotlib as mpl ;
import matplotlib.pyplot as plt ;
import matplotlib.font_manager as fontmgr ;

import lib_tcpro as tcpro ;
import lib_wiskdac as wisk ;
import tcpro_tempstat as tempstat;
import itertools ;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings
warnings.simplefilter(action='ignore',category=FutureWarning) # Suppress
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
from scipy import stats

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hr = 60*'==';
br = 60*'--';
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def dash(s='=',rep=80,car=True,pre=False):
    if pre:
        prefix='# '
        rep=rep-2
    out = ( ( (prefix)+('{:<s}')*rep + (car==True)*('\n')).format(s) )
    print(out)

def pbr(i=1,n=60,):
    symbols= '''#=-~''';
    br = n*symbols[i] ;
    print (br);
    return br;

def pbs(i=0,n=60,prefix="# "):
    prefix = "" + ""*(prefix==None)
    symbols = [chr(i) for i in range(32, 64) ];
    br = prefix + (n-len(prefix))*symbols[i] ;
    print (br);
    return br;
def tcenter( s, spad="#",sp = " ",n=60):
    e = (int(n/2) - int((len(s)+len(sp))/2) )//len(spad);
    return str( (e)*spad + (sp)+(s)+(sp) +(e)*spad) ;

def alphabet():
    alphabet = [chr(i) for i in range(65, 65+26) ]
    return alphabet;
def smybols():
    alphabet = [chr(i) for i in range(32, 64) ]
    return alphabet;   
def whoami( x ):
    print( type( x) )
    print( )
    return None;

######################################################################
def getFiles(inppath, 
             nfdef = 1,
             LASTFILE=True,
             ALLFILES=False,
             KW_BEG='watch_temp', 
             KW_END='csv', 
             SHOW=True , 
    ):
    inpfile = [];
    for f in listdir(inppath):
        if (KW_BEG in f):
            if (KW_END in f):
              if ('stat' not in f):
                inpfile.append( inppath +FSS + f)
    NFILES  = len(inpfile);
    if SHOW: print ( f'path : {inppath} ')
    ## if SHOW: print ( f'files found: {inpfile} ')
    inpfile = inpfile[NFILES-nfdef:NFILES];
    #if PSH[2]:
    # print(Selectinpfile);
    if SHOW: print ( f'files found: {inpfile} ')
    
    if LASTFILE:    
        if type( inpfile) == list:
              inpfile = inpfile[-1];  ## get last one found
        else: inpfile = str( inpfile) ; 
        if SHOW: print( f' Using Last File in {inppath}: {inpfile} ')

    if ALLFILES:
        infile = list ( inpfile[NFILES-nfdef:NFILES] ); 
        if SHOW: print( f' Using All Files in {inppath} ')
    return inpfile ;

def getdf(inpfile):
    DF = pd.concat(map(pd.read_csv, inpfile));
    return DF


#####################################################################
#### Set default values
EXE = {
    'doc'   : False,# prints doc/help
    'inp'   : None, # input path
    'log'   : None, # 
};
PSH =  [
 #--0--1--2--3--4--5--6--7--8--9  ##/Verbose/##
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
];
# ---------------------------------------------------------#
#  FILE PATHS
# ---------------------------------------------------------#
import os ; FSS     = os.sep; inppath = os.getcwd();
##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>##
#  Parse Command Line Arguments into EXE dict
# ---------------------------------------------------------#
def getArgs( EXE ):
    '''
    return INARGS = getArgs() ; 
    '''
  ##-----------------------------------------------------------    
    ##INARGS={};
    parser = argparse.ArgumentParser();
    parser.add_argument("-doc",
            nargs=1, type=str, default='' ,
            help="print doc and help ",
            action='store_true',)
    parser.add_argument("-inp",
            nargs=1, type=str, default='' ,
            help="__<str:>: path of inputh file ",
            action='store',)
    parser.add_argument("-log",
            nargs=1, type=str, default='run.log' ,
            help="__<str: run.log>: keyword for Run Log File",
            action='store',)
    ##-----------------------------------------------------------    
    args   = parser.parse_args();
    if (args.doc)!=None: EXE['doc'] = True
    if (args.inp)!=None: EXE['inp'] = args.inp; print("will do inp: {}".format(args.inp));
    
    return EXE ;
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##
#####################################################################


#################################################################################
if '__main__'==__name__: ## for testing purposes
 pass;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 if 0: ## TEST SAMPLE
    import sample_df;
    df = sample_df.sample_df();    
    print ( type (df))
    #my.dfcharacter(df);
    print( df.head() );
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
 if 1: ## testing dfcharacter(df)
    import sample_df;
    df = sample_df.sample_df();
    dfcharacter(df);
#################################################################################
