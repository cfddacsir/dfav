#!/usr/bin/python3 

VV=False;
###<HEADER_>==================================================================#
__doc__='''
#======================================================================
* Code:    pystar.py                                       
* Purpose: Process the monitored field values written in the "run.log" - output from running starccm, to either: 
  [-sum] compile stat file of the monitored values
  [-fig] generate figures of the monitored values
  [-ppt] generate compilation of Slides of those figures
  [-ppc] generate compilation of Slides from the figures saved in STARCCM postprocessing. 

# @author: Daniel.Collins @wisk.aero
@ last: 2024-03-16-2011z
  #Python ; #STARCCM+ ; #star ; #run.log ; #Daniel.Collins 
#======================================================================
'''
'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

__version__={
  240131.1938:'''+ initial ''',
  240201.1515:'''       ''',
  240205.1833:'''~ inppath; ~plot, fig, plt.log   ''',
  240205.1920:'''~ inppath; ~plot, fig, plt.log   ''',
  240207.2117:'''+ postcases... ''',
  240209.2116:'''+ lots of revamp and fixing throughout ''',
  240316.1309: ''' fixing setcae and case, adding makeSlides( pptsavename=(setcase...)''',
 }
postcase__cobalt__1 = False ;
inppath = "G:\My Drive\ACT\GCS";
#inppath = r"D:\CaseFiles\Cobalt\CobCHT\TRPUMP\SIM039\SIM039qA005\plots\\";
inppath = None; 
#inppath = r"D:\CaseFiles\Cobalt\CobCHT\TRPUMP\DSQ-200\DSQ202\DSQ202b-TC40_WF0500_TB40_0QB\\";
#inppath = r"D:\CaseFiles\Cobalt\CobCHT\TRPUMP\DSQ040\WF0250_TC40_QC00\plots\\";
googledrive = r"G:\\My Drive\\Review\\" ;
# ---------------------------------------------------------
__usage__ = '''
Usage:  

'''
# =========================================================
#####################################################################
#### Set default values
EXE = {
    'sum'   : False ,
    'fig'   : False ,
    'ppt'   : False ,   
    'ppc'   : False ,      
    'plt'   : False ,
    'lez'   : False ,
    'flu'   : False  ,
    'ave'   : False  ,
    'v'     : False  ,

    'KWL'   : 'run' , ## keyword for 
    'NSA'   : 30,  # SampleSize for qualification
    'NSP'   : 10,  # number of repeats 
    'inp'   : None, # default for input path-file 
    'sim'   : None, # default for simcase name used in ppc 
};
PSH =  [
 #--0--1--2--3--4--5--6--7--8--9  ##/Verbose/##
    1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
];

#####################################################################
#==============================================================================
# In[000.002]: Load packages
####>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>###
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
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##


##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##
# ---------------------------------------------------------#
#  FILE PATHS
# ---------------------------------------------------------#
FSS = os.sep;
FSS = wisk.osfss() ;
inppath = os.getcwd();
#####################################################################

# ---------------------------------------------------------#
# Common Functions & attributes
if 1 == 1:
    numpat = '%8de%2d';
    NULL = '';
    DIVI = (
     '---------',
     '-------------------',
     '----------------------------',
     '--------------------------------------'
            );
    PDIV = DIVI[3];
    ADIV = ("{0} \n".format(PDIV));
    BDIV = ("\n {0}".format(PDIV));
    CDIV = ("\n {0} \n".format(PDIV));
    NDIV = ("<-- {0} -->".format(PDIV));
    adiv = '#'+48*'#'+'#';
    bdiv = '#'+48*'='+'#';
    ddiv = '#'+48*'-'+'#';
##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>##
#  Formatting Templates
# ---------------------------------------------------------
OFORM = {} ;
OFORM = {
0 : '''
    =================
       {0}
    -----------------''',
10: '''Field Name = {}
       Ave        = {}
       Stdev      = {}
       Min        = {}
       Max        = {}
       First      = {}
       Last       = {} ''',
20.1 :  ''' Sample   Ave''', 
21 :    ''' {0:>2}..{2:>2}  {1:1.6e}''',        
30 : ' {: >15}: {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}',
30.1: ' {: >15}: {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}\n',
31.0: ' {: >15}: {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}',
31.1: ' {: >15}: {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}\n',
330: ' {: >15}: {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}, {:^11s}',
331: ' {: >15}: {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}, {:> 1.4e}',    
}
if 1:
    PRC1 = '{: >20}:'
    PRST = '{:^11s},'
    PRFF = '{:> 1.4e},'
    # PRDV1=('='*60);
    # PRDV2=('-'*60);
    # PRDV3=('#'*60);
    # PRDV8=('*'*60);
    # PRDV5=('%'*60);

def PRDV1():  return str('='*60);
def PRDV2():  return str('-'*60);
def PRDV3():  return str('#'*60);
def PRDV8():  return str('*'*60);
def PRDV5():  return str('%'*60);

#####################################################################

##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>##
#  FUNCTIONS
# ---------------------------------------------------------#
def getArgs( EXE ):
    '''
    return INARGS = getArgs() ;
###
EXE = {
    'plt'   : 0 ,
    'fig'   : 1 ,
    'ppt'   : 1 ,   
    'prw'   : 1 ,
    'write' : 1 ,
    'laster': 0 ,
    'flu': 0 ,
    'ave'  : 0 ,
     };
EXE ={ 
    'KWL' : 'run' ,
    'NSA': 30,  # SampleSize for qualification
    'NSP': 10,  # number of repeats    
};

    '''
  ##-----------------------------------------------------------    
    ##INARGS={};
    parser = argparse.ArgumentParser();
    parser.add_argument("-inp",
            nargs=1, type=str, default='' ,
            help="__<str:>: path of inputh file ",
            action='store',);
    #SET_SIMCASE
    parser.add_argument("-sim",
            nargs=1, type=str, default='' ,
            help="__<str:>: name of simcase ",
            action='store',);
    parser.add_argument("-log",
            nargs=1, type=str, default='run.log' ,
            help="__<str: run.log>: keyword for Run Log File",
            action='store',);
    parser.add_argument("-nsa", 
            nargs=1, type=int, default=30, 
            help="__<int: 30>: sample size for qualification ",
            action='store',);
    parser.add_argument("-nsp", 
            nargs=1, type=int, default=10, 
            help="__<int: 10>: number of sampling cycles ",
            action='store',);
    parser.add_argument("-sum", 
            help=" generate and write out tabulated summary of Monitored values" ,
            action='store_true', );
    parser.add_argument("-fig", 
            help=" make Figures of Monitored values" ,
            action='store_true',);
    parser.add_argument("-ppt", 
            help=" make Slides compiled of Monitored Figures" ,
            action='store_true',);
    parser.add_argument("-ppc", 
            help=" make Slides compilation of STARCCM scenes and run postcase " ,
            action='store_true',);
    ##-----------------------------------------------------------    
    args   = parser.parse_args();
    if (args.inp)!=None: EXE['inp']  = args.inp; print("will do inp: {}".format(args.inp));
    if (args.sim)!=None: 
        EXE['sim']  = args.sim; print("will do inp: {}".format(args.sim));
        if type( EXE['sim'])==list: EXE['sim'] = EXE['sim'][0] ;
    if (args.log)!=None: EXE['KWL']  = args.log; print("will do KWL: {}".format(args.log));
    if (args.nsa)!=None: EXE['NSA']  = args.nsa; print("will do NSA: {}".format(args.nsa));
    if (args.nsp)!=None: EXE['NSP']  = args.nsp; print("will do NSP: {}".format(args.nsp));

    if (args.sum)!=None: EXE['sum']  = args.sum; print("will do sum: {}".format(args.sum));
    if (args.fig)!=None: EXE['fig']  = args.fig; print("will do fig: {}".format(args.fig));
    if (args.ppt)!=None: EXE['ppt']  = args.ppt; print("will do ppt: {}".format(args.ppt));
    if (args.ppc)!=None: EXE['ppc']  = args.ppc; print("will do ppc: {}".format(args.ppc));
    
    return EXE ;
##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def getFiles(inppath, nfdef = 1, KW_LOG='run.log' ):
    inpfile = [];
    # inpfile = [ inppath + FSS + f for \
    #             f in listdir(inppath) \
    #               if KW_LOG in f and  \
    #                  'stat' not in f  ];
    for f in listdir(inppath):
        if (KW_LOG in f):
          if ('stat' not in f):
            inpfile.append( inppath +FSS + f)
    NFILES = len(inpfile);
    Selectinpfile = inpfile[NFILES-nfdef:NFILES];
    if PSH[1]:
     print(Selectinpfile);
    return Selectinpfile
#####################################################################

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


#####################################################################

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def getdf(inpfile):
    DF = pd.concat(map(pd.read_csv, inpfile));
    return DF
#####################################################################

#####################################################################

#####################################################################
# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def cleannames(  crow ):
    crow = re.sub(r'\\', '%', crow) ;
    crow = re.sub(r'\/', '%', crow) ;
    crow = re.sub(r'\^', '%', crow) ;
    return crow; 
#####################################################################

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def cleanrow(frow):
    '''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
« crow = cleanrow( frow) : »
  « frow < str> : un-filtered raw row streated as one string
  » crow : cleaned up string
§ cleans row by removing open spaces and null etnries, ...
     as per the formatting in STARCCM's run output.
@ 2024-02-16-1636Z/DAC/Daniel.Collins@wisk.aero •
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
    crow = frow;
    crow = re.sub(' '*12 , '  ', crow);
    crow = re.sub(' '*10 , ';', crow);
    crow = re.sub(' '*11, '0.000000e+00,', crow);
    crow = re.sub(' ', ',', crow);
    crow = re.sub(' ', ',', crow);
    crow = re.sub(' ', ',', crow);
    crow = re.sub(' ', ',', crow);
    crow = re.sub(',,', ',', crow);
    crow = re.sub(',,', ',', crow);
    crow = re.sub(',,', ',', crow);
    crow = re.sub(',,', ',', crow);
    #crow = re.sub(';', ',', crow);
    crow = re.sub(';', '', crow);    
    crow = re.sub(',\n', '', crow);
    crow = re.sub('\n', '', crow);
    return crow;
#####################################################################

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def cleanheader(frow):
    crow = frow;
    # '     Iteration'
    #crow = re.sub('      Iteration', 'Iteration,', crow);
    crow = re.sub('     Iteration', 'Iteration,', crow);
    #crow = re.sub(r'Physical Time (s)',r'PhysTime(s),', crow);
    #crow = re.sub(r'Physical Time',r'PhysTime,', crow);
    crow = re.sub('Physical Time \(s\)','PhysTimes,', crow);
    crow = re.sub('Physical Time (s)','PhysTimes,', crow);
    crow = re.sub(r' \(', r'(', crow);
    crow = re.sub('  ', ',', crow);
    crow = re.sub(' ', ',', crow);
    crow = re.sub(' ', ',', crow);
    crow = re.sub(',,,', ',', crow);
    crow = re.sub(',,', ',', crow);
    crow = re.sub(',,', ',', crow);
    crow = re.sub(',\n', '', crow);
    crow = re.sub('\n', '', crow);
    return crow
#####################################################################


# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def getdatarows(inpfile):
    DSET = [];  HSET = [];  BSET = [];
    irow = 0;
    #with open(inpfile, 'r') as inp:
    with open(inpfile, newline='\n', encoding='ansi' ) as inp:
    #with open(inpfile, newline='\n'  ) as inp:    
        for getrow in inp.readlines( 0 ):
            irow +=1 ; 
            #if VV:print (irow, sep='......', end='\n\t' );
            if VV:print (irow, sep='..', end='' );
            #if irow < 1 : #and 
            if len(HSET) < 1 : #and \
              if ( 'Iteration'       in     getrow and \
                    'Initialization' not in getrow
                  ):
#                    'Continuity' in getrow and \
                crow = cleanheader(getrow);
                for bit in crow.split(','):
                    HSET.append(str(bit));
                if PSH[4]:
                    print(''' Header Names: {}'''.format(
                      HSET));
            ####if 0 : DSET.append(HSET);
            if irow>1: 
             if ( 'e-' in     getrow and \
                  'e+' in     getrow and \
                  ':'  not in getrow and \
                  'a'  not in getrow     ):
                crow = cleanrow(getrow);
                BSET = [];
                for bit in crow.split(','):
                    try:
                        BSET.append(float(bit));
                    except:
                        if bit==None:  # BSET.append(0); pass; 
                          pass;  # BSET.append(0)
                    if PSH[16]:
                     print(BSET);
                DSET.append(BSET);
                if PSH[15]:
                 print(DSET);
             #if VV: 
             # else: print('{}\n'.format(getrow)); #, sep='', end='\n') ;
        inp.close();
    return HSET, DSET ;
#####################################################################
def showheader( DICT, wf=None, ):
    for k, p in enumerate( DICT  ) : 
        if k < len( DICT  ) -1: 
              print(('{}'+1*','+0*' ').format( str( (p)) ), sep='', end=''  ,file=wf )
        else: print(('{}'+0*','+0*' ').format( str( (p)) ), sep='', end='\n',file=wf )

# --------------------------------------------------------
def wrsum( F, Fnames, inpfile, wf, EXE, ): 
    ## if EXE['prw']:
    if 1:    
        try:   LR = int(EXE['NSA']);
        except:LR = int(EXE['NSA'][0]);
        if     LR==None: LR=30;
        #print( Fnames );
        d1 = PRDV1() ;
        d2 = PRDV2() ;
        print(
          ( ('{}\n'*6 ).format( 
            str('{:>20s}: {}' .format('Input File:', inpfile)),
            d1,
            str('{:>20s}: {}' .format('Sampling Range', LR )),
            d1,
            str(('{: >20}:'+'{:^11s},'*3).format(
               'FieldName', 'Mean', '%Dev', 'Last' )),
            d2,
           )), sep='', end='\n'  ,file=wf );
        
        for yc, yt in enumerate(Fnames):
            Yf = F[-LR:, yc];
            if PSH[6]:  print (yt);
            if PSH[12]: print (Yf)
            ycap = Yf[0];
            yfin = Yf[-1];
            if Yf[1] == None: 
              #pass; # break;
              print(
                 (PRC1+PRST*3 )     .format(
               yt, 'NA','NA','NA'))
              if EXE['sum']: wf.write(
                 (PRC1+PRST*3 +'\n').format(
               yt, 'NA','NA','NA'));
            else: 
             try:
                ymin = min(Yf);
                ymax = max(Yf);
                yavg = statistics.mean(Yf);
                ydev = statistics.pstdev(Yf);
                if yavg != 0: rdev = ydev / yavg * 100 ;
                else: rdev = ydev;
             except:
                ymin = 0;
                ymax = 0;
                yavg = 0;
                ydev = 0;
                rdev = 0;
             print(
             (PRC1+PRFF*3 ).format(
              yt, yavg, rdev, yfin));
             if EXE['sum']: 
                wf.write(
                    (PRC1+PRFF*3 +'\n').format(
                       yt, yavg, rdev, yfin
                    )
                );
        print(( PRDV8() +'\n'));
#####################################################################
    if 0: ## EXE['prw']==2:
        v1=('='*110);
        v2=('='*110);
        try:    LR = int(EXE['NSA']);
        except: LR = int(EXE['NSA'][0]);
        if      LR==None: LR=30;
        print(('\n'+\
               PRDV1+'\n'+\
               OFORM [ 330 ]+'\n'+\
               PRDV2         ).format(
              'FieldName', 'Ave', 'Std', 'Rel', 'Min', 'Max', 'Capo', 'Fine'
              ));
        if EXE['sum']: wf.write((
               PRDV1+'\n'+\
               OFORM [ 330 ]+'\n'+\
               PRDV2+'\n'    ).format(
              'FieldName', 'Ave', 'Std', 'Rel', 'Min', 'Max', 'Capo', 'Fine'
              ));
        for yc, yt in enumerate(Fnames):
            Yf = F[-LR:, yc];
            if PSH[6]:  print (yt);
            if PSH[12]: print (Yf)
            ycap = Yf[0];
            yfin = Yf[-1];
            if Yf[1] == None: pass; # break;
            else: 
             try:
                ymin = min(Yf);
                ymax = max(Yf);
                yavg = statistics.mean(Yf);
                ydev = statistics.pstdev(Yf);
                if yavg != 0: rdev = ydev / yavg;
                else: rdev = ydev;
             except:
                ymin = 0;
                ymax = 0;
                yavg = 0;
                ydev = 0;
                rdev = 0;
             print(OFORM [ 331 ].format(
              yt, yavg, ydev, rdev, ymin, ymax, ycap, yfin))
             if EXE['sum']: wf.write(\
                 (OFORM [ 331 ]+'\n').format(
              yt, yavg, ydev, rdev, ymin, ymax, ycap, yfin))
        print(('\n'+PRDV1+'\n'))
#####################################################################

#####################################################################
def prlast( F, Fnames, EXE ):
    try:   LR = int(EXE['NSA']);
    except:LR = int(EXE['NSA'][0]);
    if     LR==None: LR=30;

    for yc, yt in enumerate(Fnames):
        #ys = Fnames(yc);
        Yf = F[-LR:, yc];
        ycap = Yf[0];
        yfin = Yf[-1];
        ymin = min(Yf);
        ymax = max(Yf);
        yavg = statistics.mean(Yf);
        ydev = statistics.pstdev(Yf);
        print(OFORM[ 10 ].format(yt, yavg, ydev, ymin, ymax, ycap, yfin));
#####################################################################


#####################################################################
def writewide( F, Fnames, EXE ) :
#    if EXE['ave']:
    if 1:
      try:   SA = int(EXE['NSA']);
      except:SA = int(EXE['NSA'][0]);
      if     SA==None: SA=30;
      try:   SP = int(EXE['NSP']);
      except:SP = int(EXE['NSP'][0]);
      if     SP==None: SP=30;
    if 0:
      SA = (EXE['NSA']);
      SP = (EXE['NSP']);
      NR = len(DSET)-1;
    if 1:
      for yc, yt in enumerate(Fnames):
          print(OFORM[ 0 ].format(yt));
          print(OFORM[ 20.1 ]);
          yset = [];
          for CR in range(-SA-SP, -SA, 1):
              LR = CR + SA;
              Yf = F[CR:LR, yc];
              ycap = Yf[0];
              yfin = Yf[-1];
              ymin = min(Yf);
              ymax = max(Yf);
              yavg = statistics.mean(Yf);
              ydev = statistics.pstdev(Yf);
              print(OFORM[ 21 ].format(int(-CR), yavg, int(-LR)));
              yset.append(yavg);
              print(' {} [ave] = {:1.5e} '.format(
                yt, statistics.mean(yset)));
              print('dev [ppm]: {0:1.4f}'.format(
                statistics.pstdev(yset)/statistics.mean(yset)*100000
                ));

#####################################################################
def writestream( F, Fnames, EXE ) :
####    if EXE['flu']:
    SA = 30; SP = 5; LR = SA;  NR = len(DSET)-1;
    for yc, yt in enumerate(Fnames):
        SS='''  {: >3} ... {:<15} '''
        print('''\n List of Field Values ''');
        for yc, yt in enumerate(Fnames):
          print(SS.format( yc, yt ))
        print('''\n Chose # for what Field to monitor ''');
       # inpf = int( input(' : ') );
        inpf = 12
        yc = inpf;
        yt = Fnames[yc]
        print(' Watching Field = {} '.format(yt) )
        yset = [];
        for CR in range(-SA-SP, -SA, 1):
            CR = NR + CR;
            LR = CR + SA;
            Yf = F[CR:LR, yc];
            ycap = Yf[0];
            yfin = Yf[-1];
            ymin = min(Yf);
            ymax = max(Yf);
            yavg = statistics.mean(Yf);
            ydev = statistics.pstdev(Yf);
            yset.append(yavg);
            ravg = statistics.mean(yset);  ##
            rdev = statistics.pstdev(yset)/statistics.mean(yset)*100000;     ## rolling value of yset stdev in ppm
            p = ( yavg - ravg) *100000 ;
            print(' Sample {} to {} '.format(CR,LR))
            print(OFORM[ 31 ].format(
              yt, yavg, ydev, ymin, ymax, ycap, yfin));
            print('      {2:>10}: {0: 1.4e} \t {3} {1:1.2f}ppm '.format(
              ravg, p, 'Ave', 'Diff:' ));
            print('      {1:>10}: {0: 1.2f}ppm \n'.format(
              rdev, 'rDev', 'Dev:' ));

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def makeplots( DF, Fnames, EXE ) :
  '''
ppt_framenames = makeplots( DF, Fnames, EXE )
 * DF <dataframe> :
 * fnames <list> :
 * EXE<dict>: 

// Vers: dac/2024-02-16-1636Z //
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
  if ( EXE['plt'] or EXE['fig'] or EXE['ppt'] ):
    ebeg = 10 ;
    RESIDUALKWS = ['X-momentun','Y-momentun','Z-momentun',
                   'Energy', 'Continuity','Tke','Tdr' ] ;
    RESIDUALKWS.append( 'dFnom')
    RESIDUALKWS.append( 'dPsdv')
    RESIDUALKWS.append( 'dPvar')
    RESIDUALKWS.append( 'dPcentPP')
    ppt_framenames = [] ;
    ffc = DF.shape[1] ;
    fss = wisk.osfss();
    for c in range(3, ffc+1 - 1, 1 ): 
        plt.cla();
        clab = Fnames[c] ;
        erste = DF.iloc [ ebeg, c ] ;
        leste = DF.iloc [ -1  , c ] ;
        erste = max( DF.iloc [ ebeg:-1, c ] ) ;
        leste = min( DF.iloc [ ebeg:-1 , c ] ) ;
        plt.plot( DF.iloc [ebeg :-1,c],label=clab) ;
        if(
           ( (clab in RESIDUALKWS  ) ) \
        or(( 1e-10< abs(leste) < 1e5 and 1e-10< abs(erste) < 1e5  ) \
         and ( abs(leste / erste) > 100 or abs(erste/leste) > 100   ) \
          )
        ):
            yrat = abs (leste / erste)
            print( '{:} {:} {:3e}  {:3e}  {:3e} '.format( c, clab, erste, leste, yrat));
            if (leste <0) or (erste<0):
              #plt.cla();plt.plot( math.log10( abs(DF.iloc [ebeg:-1,c])), label=clab);
              plt.cla();plt.plot( ( abs(DF.iloc [ebeg:-1,c])), label=clab);
            else: 
              plt.cla();plt.plot( ( abs(DF.iloc [ebeg:-1,c])), label=clab); 
            plt.yscale('log') ;
        else:
            plt.yscale( 'linear') ;
            # plt.plot( DF.iloc [ebeg :-1,c],label=clab) ;
        plt.title( clab  ); 
        figsavename = ""\
            + 1* str(inppath)\
            + 1* str(fss)  \
            + 1* str( 'plot_' ) \
            + 1* str( cleannames( clab ) )  \
            + 1* str('.png') ;
        if 1:
          if ( EXE['fig'] or EXE['ppt'] ):
            plt.savefig( figsavename ) ;
          if EXE['plt']:
            plt.show() ;
        ppt_framenames.append( figsavename );
    return ppt_framenames ;
#####################################################################
##################################

# In[1]: postcases ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#def postcase( PROJROOT, LIST_CASES=None, mc=1 ) :
def postcase( inppath=None, case=None, mc=0 ) :
  '''
def postcase( inppath=None, case='simcase', mc=0 ) : ## rev <24-03-23<
null = postcase( inppath=None, case=None, mc=0 ) :

* PROJROOT <str>         :
    path where inputfiles exist
* case <str> = 'simcase' : 
    name of simcase, such as Design_1, or [TRQ0200](.sim)
    will be the basename for the Slide Deck
    needed if mc=1 and thus specifies the casedir for the load case under PROJROOT
* mc=0 <int> :
    option to specify a subdirector of loadcase


Purpose: generates Slide file (pptx) with compilation of figures ...
  generated from STARCCM post-processing such as from post_batch.java

 Vers: dac/2024-02-16-1714Z~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

  import lib_wiskdac as wisk ;
  os.chdir( inppath );
  ls = os.listdir( inppath );
  if inppath==None: inppath = os.getcwd(); 
  if case==None: case = wisk.getsimcase( inppath) ;
 #   if LIST_CASES==None:
 #       LIST_CASES = simcase(inppath ); mc=0;
    #case = getsimcase(inppath ); mc=0;
    #if getsimcase(inppath )==None: case='simcase';
  if 1: 
    # for case in LIST_CASES:
        dir_proj = inppath + FSS ;
        if mc>0: dir_proj = inppath + FSS + case + FSS ;
        # ls_proj  =  listdir( dir_proj  ) ;
        # print( ls_proj) ;
        dir_post = inppath + FSS + mc*(case +FSS) + "post" +FSS ;
        os.chdir( dir_post) ; 
        print( dir_post) ;
        ls_post =  listdir( dir_post  )
        ''' 
    SLIDENAMES = MakeSlides( ppt_gallery, inppath, inpfile, EXE, PSH, EXE, PSH, .... )
         '''

        if 1:
          #for patt in ( "hist","sce" ,"plot", ):
            #lst_plot  = wisk.getfilesbe( dir_post, begkw="plot", endkw='.png', PSH=[0,1] )
            #print (  ls_plot )     
            ls_patt = \
                wisk.getfilesbe( dir_post, begkw='', endkw='.png', PSH=[0,1])

            print(" making slides for {}".format( ls_patt) );
            wisk.MakeSlides( 
              ### make Slides for postcases ###
                ls_patt, PSH, 
                inppath=dir_post, 
                ncol=1,
                nrow=1,
                figr=9,
                basename=case,
                xtagname='',
                PPTXPATH=r"G:\\My Drive\\mylab\\lib\\",
                PPTXFILE=r"WISK.pptx",
                googledrive = r"G:\\My Drive\\Review\\" ,
                #pptsavename = None,
                pptsavename = f"{case}_postmac",
            );
            
        

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
##  MAIN EXECUTE
# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
if __name__ == '__main__': 
  if 1:
      EXE = getArgs( EXE );
      wisk.showkeys( EXE );
  if EXE['v']: print( __doc__, __version__, __usage__ , end='\n\n' );
 
  if 1:#<< input path  >>========================================   
    if inppath==None : inppath = os.getcwd();
    if EXE['inp']: 
      inppath =EXE['inp'];
      if type( EXE['inp'])==list: inppath=EXE['inp'][0] 
  #    inppath = EXE['inp'];  
      if PSH[0]: print ( os.listdir() )
      #if PSH[0]:
      print(' current path is {} '.format(inppath));
      print(' Inppath: {} '.format(inppath));

#<< Execution >>========================================= 
  if EXE['ppc']:
      if 1: ##{{ MASKING CODE }}
        ''' LIST_CASES = readcsv( dictionary of cases) '''
        if     ( EXE['sim']): 
          setcase =EXE['sim']; 
          if type( EXE['sim'])==list: setcase=EXE['sim'][0] ;
        else : setcase='';
        if PSH[0]: pass;
        print ( 'setting setcase as {}'.format( setcase ) )
        if     ( EXE['inp']): 
          inppath =EXE['inp'];
          if type( EXE['inp'])==list: inppath=EXE['inp'][0] ;
        else: inppath = os.getcwd() ;
        if PSH[0]: pass;
        print ( 'setting inppath as {}'.format( inppath ) )
        postcase( inppath=inppath, case=setcase , mc = 0)  ;
        exit() ; 

#<< Execution >>========================================= 
 
  if ( EXE['sum'] or EXE['fig'] or EXE['ppt'] ):
    if type( EXE['KWL'])==str : kw=str(EXE['KWL'] ) ;
    if type( EXE['KWL'])==list: kw=str(EXE['KWL'][0]) ;
    
    inpfile = getFiles( str(inppath), KW_LOG=str(kw) );
    inpfile = str( inpfile[-1] ) ; ### only last-one
    #if PSH[2]:

    print(' input file = {}'.format(inpfile));
    print('Now reading file {}'.format(inpfile));
    HEADER, DSET = getdatarows(inpfile);
    
    DF = pd.DataFrame( data=DSET , columns=HEADER  );
    F  = DF.to_numpy();
    Fnames = HEADER ;
    print( 'Fnames: \n\t' ); print( Fnames );
    if PSH[6]:
         print('Fnames = \n {}'.format(Fnames));
   
#<< Execution >>=========================================
  if 1: ## if 0: ## ignore code....
    if EXE['sum']:
        if len(Fnames) <1: print(" Fnames no length! "); exit(); 
        writeoutfile = inpfile + '.stat.txt'
        outfile = open ( writeoutfile , 'w'); outfile.write('') ;
        outfile = open ( writeoutfile , 'a');
        wrsum( F, Fnames, inpfile, outfile, EXE, )
        outfile.close() 
        
    if EXE['flu']:
        if len(Fnames) <1: print(" Fnames no length! "); exit(); 
        writestream( F, Fnames, EXE ) ;

    if EXE['ave']:
        if len(Fnames) <1: print(" Fnames no length! "); exit(); 
        writewide( F, Fnames, EXE ) ;

    if EXE['lez']:  
        if len(Fnames) <1: print(" Fnames no length! "); exit();     
        prlast( F, Fnames, EXE );
       
    if ( EXE['plt'] or EXE['fig'] or EXE['ppt'] ):
        # if EXE['fig']: 'do plot';
        if len(Fnames) <1: print(" Fnames no length! "); exit();         
        ppt_framenames = makeplots( DF, Fnames, EXE ) ;        
        if PSH[2]: 
          print( ' last few lines of ppt_framenames ')
          for i, p in enumerate(ppt_framenames):
            print( p );   
        
    if EXE['ppt']:
        #if 0: ##{{ MASKING CODE }}
        #if     ( EXE['sim']): 
        setcase = str( EXE['sim'] ); 
        if type( EXE['sim'])==list: setcase=str(EXE['sim'][0] ) ;
        #else : setcase='';

        if PSH[0]: print ( 'setting setcase as {}'.format( setcase ) );

        if     ( EXE['inp']): 
          inppath = str( EXE['inp'] );
          if type( EXE['inp'])==list: inppath=str( EXE['inp'][0] );
        else: inppath = os.getcwd() ;
        if PSH[0]: print ( 'setting inppath as {}'.format( inppath ) );
        if     ( EXE['sim']): 
          setcase =EXE['sim']; 
          if type( EXE['sim'])==list: setcase=EXE['sim'][0] ;
        else : setcase='';
        if PSH[0]: pass;
        print ( 'setting setcase as {}'.format( setcase ) ) ;
        pptsave=None;
        if len(setcase)>0: pptsave = f"{setcase}_moni" ; 
        #else: pptsave=None;
        SLIDENAMES = \
            wisk.MakeSlides( 
              ### make Slides for MoniSumPlots ###
                ppt_framenames ,
                #inpfile, 
                PSH, 
                inppath=inppath, 
                ncol=3,
                nrow=1,
                basename= str( setcase ) ,
                xtagname='moni',
                #figr=1.444,
                figr=1.325,
                figb=6.000,
                ph_set=5.00,
                pw_set=3.00,
                pwhmax=True,
                PPTXPATH=r"G:\My Drive\mylab\lib\\",
                PPTXFILE=r"WISK.pptx",
                googledrive = r"G:\My Drive\Review\\",
                pptsavename = pptsave,
        );
 #<< Execution >>========================================= 

#####################################################################

####<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<######
##  END OF SCRIPT
####<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<######

__doc_sample__=\
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
« crow = cleanrow( frow) : »
  « frow < str> : un-filtered raw row streated as one string
  » crow : cleaned up string
§ cleans row by removing open spaces and null etnries, ...
     as per the formatting in STARCCM's run output.
@ 2024-02-16-1636Z/DAC/Daniel.Collins@wisk.aero •
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

__version__={
  240131.1938:'''+ initial ''',
  240201.1515:'''       ''',
  240205.1833:'''~ inppath; ~plot, fig, plt.log   ''',
  240205.1920:'''~ inppath; ~plot, fig, plt.log   ''',
  240207.2117:'''+ postcases... ''',
  240209.2116:'''+ lots of revamp and fixing throughout ''',
  240316.1309:''' fixing setcae and case, adding makeSlides( pptsavename=(setcase...)''',
 }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~