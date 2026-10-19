## -*- coding: utf-8-*g
__doc__='''
#==============================================================================
# lib_wiskdac.py
@ last: 2024-03-16-2011z
@ author: Daniel.Collins <Daniel.Collins@wisk.aero >
# library of python tools shared for Wisk applications
#Python ; #wisk; #Daniel.COllins; #makeSlides
#------------------------------------------------------------------------------'''
###############################################################################
PSH =[0 for i in range(0,100)] ; ## PSH[1]  = 0 ;

##############################################################################
# In[0]: Load packages
#------------------------------------------------------------------------------
####  Import Packages
#import lib_tcpro as tcpro ;
#import lib_wiskdac as wisk ;
#import lib_getfiles as getfiles ;
#import tcpro_tempstat as tempstat;
#import showmaxia as showmaxia  ;
####  Import Packages
import re ;
from   os import listdir;
import os;
import string ;
import math ;
import linecache ;
import argparse ;
import statistics ;
import pandas as pd ;
import numpy as np ;
import matplotlib as mpl ;
import matplotlib.pyplot as plt ;
import matplotlib.font_manager as fontmgr ;
from   scipy import signal;
from   datetime import datetime ;
#-----------------------------------------------------------------------------#

###############################################################################

def osfss( ):   
    '''
    arg:  None
    ret: FSS <str> file-separator based on the operating system

    '''
    import platform; p = platform.uname();
    #import unicode; 
    import platform; p = platform.uname();
    if p.system == 'Windows': FS  =  str('\u005c') ;  ## == "\" #if system is Windows:
    else: FS  =  str('\u002f') ;  ## == "/"  # if NOT windows
    FSS =  str( 1*FS ) ;
    return FSS;

FSS = osfss();
###############################################################################
def initsetfile_v1 ( SETFILE,ofile = {}  ):
    #ofile = {} ;    
    for digit, thisfile in enumerate( SETFILE ):
              (open( SETFILE[digit] , 'w')).write('');
              ofile[digit] = (open (SETFILE[digit] , 'a')) ;
    return ofile ;

def initsetfile_v3 ( SETFILE, ofile=None, setkey=None ):
    if ofile==None: ofile = {} ;    
    for k, thisfile in enumerate( SETFILE ):
      if type(setkey) == str or int: k=setkey
      print( setkey )
      ofile[k] =(open( thisfile, 'w',encoding='utf-8',newline=None, )).write('' );
      ofile[k] =(open( thisfile, 'a',encoding='utf-8',newline='\n', ));
    return ofile ;

def initsetfile ( SETFILE, ofile=None, setkey=None ):
    if ofile==None: ofile = {} ;    
    thisfile = SETFILE 
    if 1:        
      if type(setkey) == str or int: k=setkey
      #if PSH[0]:
      #print('setkey', end='..', sep='.. ')
      #print( setkey )
    if 1:        
      ofile[k] =(open( thisfile, 'w',encoding='utf-8',newline=None, )).write('' );
      ofile[k] =(open( thisfile, 'a',encoding='utf-8',newline='\n', ));
    return ofile ;

def initsetfile2  ( SETFILE, ofile=None, setkey=None ):
    if type(ofile) == dict:
        okeys = ofile.keys();
    for k, thisfile in enumerate( SETFILE ):
      if type(setkey) == str or int: k=setkey
      if k in okeys: k = str(k) + '_0'
      ofile[k] =(open( thisfile, 'w',encoding='utf-8',newline=None, )).write('' );
      ofile[k] =(open( thisfile, 'a',encoding='utf-8',newline='\n', ));
    return ofile ;

def initsetfile3 ( SETFILE, ofile={}, setkey=None ):
    if type(ofile) == dict:
        okeys = ofile.keys();
    for k, thisfile in enumerate( SETFILE ):
      if type(setkey) == str or int: k=setkey
      if k in okeys: k = str(k) + '_0'
      ofile[k] =(open( thisfile, 'w',encoding='utf-8',newline=None, )).write('' );
      ofile[k] =(open( thisfile, 'a',encoding='utf-8',newline='\n', ));
    return ofile ;
###############################################################################
#import re ;   
def showheader( listparm, wf=None, ):
    for k, p in enumerate( listparm  ) : 
        if k < len( listparm  ) -1: 
              print(('{}'+1*','+0*' ').format( str( (p)) ), sep='', end=''  ,file=wf )
        else: print(('{}'+0*','+0*' ').format( str( (p)) ), sep='', end='\n',file=wf )
###############################################################################
def showkeys( DICT, wf=None, ):
    for i, k in enumerate( DICT) : 
        p = DICT.get(k)
        print(('{:<3s} : {:<5s} : {}').format( str(i),str(k),str( p) ),
              sep='',end='\n',file=wf );
###############################################################################        
def showeval(   listparm, listform, vdict, csep=True, wf=None, wend=True ):
    '''
    listparm: list of parameters
    listform: list of formatting
    vdict   : dictionary of values for the parameters
    '''        
    for k, p in enumerate( listparm ) : 
        showform = listform[k]  ;
        #print(showform) ;
        #v = vdict[p] ;
        #print( v );
        if k < len( listparm  ) -1: 
            print( 
                (showform +csep*',') .format(     ( vdict[p] ) ) , 
#                (showform +csep*',') .format( eval( vdict[p] ) ) , 
                #sep=',' ,
                end='',
                file=wf 
            ) ;
        else: 
            print( 
                (showform  ) .format( ( vdict[p] ) ) , 
                #sep='' ,
                end=(wend*'\n'),
                file=wf 
            ) ;

###############################################################################
def setcolors( FARBSCALE = True ):
    '''
    arg:  FARBSCALE = True (scales the values of FARBEN to fit range of 0/255 to 255/255)
    ret:  WISKCLR < dictionary of color palettes >,
          FARBEN  < dictionary of color palettes >
    ''' 
    #####-----------------------------------------------------------------------
    # color=[ 220*(1/255),  15*(1/255),   5*(1/255) ],
    WISKCLR={  ## WISK COLOR PALETTE
            0:[ 255/255, 209/255,   0/255  ] , ## Yellow
            1:[   0/255, 169/255, 206/255  ] , ## Blue
            2:[  85/255,  86/255,  90/255  ] , ## Grey
    };
    FARBEN={
           0: [  255, 209,   0  ] , ## Yellow
           1: [    0, 169, 206  ] , ## Blue
           2: [   85,  86,  90  ] , ## Grey
           3: [  210,  10,   5  ] , ## mag-red-01
           4: [  255,  20,  20  ] , ## Red
           4: [  160,  90, 140  ] , ## Purple
    };
    
    if FARBSCALE:
      for i, farb in enumerate(FARBEN):
        FARBEN[i] = [ 
            FARBEN[i][0] * (1/255), 
            FARBEN[i][1] * (1/255), 
            FARBEN[i][2] * (1/255) 
        ];
    return WISKCLR, FARBEN ;            
    ####-----------------------------------------------------------------------

###############################################################################
def makecolor( r, g, b, ckey = 0 , SCALE = True, ):
    '''
  arg:  
        r: <float> between 0 to 255 for Red  -Axis
        g: <float> between 0 to 255 for Green-Axis
        b: <float> between 0 to 255 for Blue -Axis
        ckey = 0 ( key for returning dictionary )
        SCALE = True (scales the values of FARBEN to fit range of 0/255 to 255/255)
  ret:
        COLOR < 3x0 list > 
    ''' 
    #####-----------------------------------------------------------------------
    COLOR = {} ;
    COLOR[ckey] = [ r, g, b ];
    
    if SCALE:
      for i, farb in enumerate(COLOR):
        COLOR[i] = [ 
            COLOR[i][0] * (1/255), 
            COLOR[i][1] * (1/255), 
            COLOR[i][2] * (1/255) 
        ];
    return COLOR ;            
    ####-----------------------------------------------------------------------

###############################################################################

###############################################################################

###############################################################################
if 1: ## FORMATS FOR PRINTING
    numpat = '%8de%2d';
    DIVI = [ '-'*10, '-'*20, '-'*30,'-'*40, ];

    def prbr(nn, *PR):
        r = ('{0}'.format(str('='*nn)));
        if PR: print( r );
        return r;

    def prbr1(nn, *PR):
        r = ('{0}'.format(str('-'*nn)));
        if PR: print( r );
        return r;
    def prbrs(s, nn, *PR):
        r = ('{0}\n'.format(str(s*nn)));
        if PR: print( r );
        return r;

    def prcr(nn, *PR):
        r = ('{0}'.format(str('='*nn)));
        if PR: print( r );
        return r;

    def prcr1(nn, *PR):
        r = ('{0}'.format(str('-'*nn)));
        if PR: print( r );
        return r;

    def prcrs(s, nn, *PR):
        r = ('{0}'.format(str(s*nn)));
        if PR: print( r );
        return r;

###############################################################################
#-----------------------------------------------------------------------------#
def getfilesbe ( inppath, begkw=None, endkw='.csv', PSH=[0, 0 ] ):
    '''
    Return FILESETPATHS <list of strings>
    Parameters
    ----------
    inppath [str]
        DESCRIPTION.
    begins [str]
        keyword for files to be sought in path
    PSH [list]
        toggles for PrintOut
        *default is [0, 0 ].

    '''
    ### from: eslib_getfiles.py as getfiles.wisk.getfilebegins
    FILESETPATHS = [];
    if PSH[1] : print(f' inppath = {inppath}');
    for f in listdir(inppath):
      if f.endswith( endkw ) and f.startswith( begkw ) :
         # for ii in range(10,1,-1):
         #   ol = ''
         #   for jj in range(ii):
         #     ol += (r'\\')
         #   f = f.replace( ol , '');
           # eval( f' f = f.replace( (r'\\')*ii, '') ')
         FILESETPATHS.append( str( inppath + f ) );
    if PSH[1] : print( FILESETPATHS );
    return FILESETPATHS;

#-----------------------------------------------------------------------------#
def getfilesbegins( inppath, begins, PSH=[0, 0 ] ):
    '''
    Return FILESETPATHS <list of strings>
    Parameters
    ----------
    inppath [str]
        DESCRIPTION.
    begins [str]
        keyword for files to be sought in path
    PSH [list]
        toggles for PrintOut
        *default is [0, 0 ].

    '''
    ### from: eslib_getfiles.py as getfiles.wisk.getfilebegins
    FILESETPATHS = [];
    if PSH[1] : print(f' inppath = {inppath}');
    for f in listdir(inppath):
      if f.endswith('.csv') and f.startswith(begins) :
         for ii in range(10,1,-1):
           ol = ''
           for jj in range(ii):
             ol += (r'\\')
           f = f.replace( ol , '');
           # eval( f' f = f.replace( (r'\\')*ii, '') ')
         FILESETPATHS.append( str( inppath + f ) );
    if PSH[1] : print( FILESETPATHS );
    return FILESETPATHS;

#-----------------------------------------------------------------------------#

def getdf(Selectfiles):
    if PSH[2] : print (f'nr of files as input: {len(Selectfiles)}');
    if len(Selectfiles) == 1:
      if PSH[2] : print(f' Executing...  pd.read_csv(Selectfiles) ... ');
      if PSH[2] : print(f' Selectfiles = {Selectfiles}');
      df = pd.read_csv( str(Selectfiles[0]) );
    if len(Selectfiles) > 1:
      if PSH[2] : print(f' Executing...  pd.concat(map(pd.read_csv, Selectfiles)) ...');
      if PSH[2] : print(f' Selectfiles = {Selectfiles}');
      df = pd.concat(map(pd.read_csv, Selectfiles));
    return df;

#=============================================================================#

def get_date ( timestamp):
    gs  = datetime.fromisoformat(timestamp);
    ss  = '' ;
    su  = '_' ;
    Y=str(gs.year - 2000)
    A=(gs.month <10)*'0'+str(gs.month )
    D=(gs.day   <10)*'0'+str(gs.day   )
    H=(gs.hour  <10)*'0'+str(gs.hour  )
    I=(gs.minute<10)*'0'+str(gs.minute)
    fig_date = Y + ss + A + ss + D + su + H + ss + I ;
    return fig_date ;
#-----------------------------------------------------------------------------#

def dstrip( dt ):
    ww = []
    for u in dt:
      ww.append( u.rstrip() );
    return np.asarray(ww);

#-----------------------------------------------------------------------------#

def smooth( smpl ):
  b, a = signal.butter( 1 , ( 1/18 ), fs=10);
  fsmooth = signal.filtfilt( b, a, smpl );
  return fsmooth;

#==============================================================================
#==============================================================================
## In[2]:# Unpack 
class Unpack:
    def __init__( self, mat ):
        if len( mat )> 0:
            self.mat = mat[0];
        else:
            self.mat = mat ;
            
def   unpack(mat):
        unpack = mat;     
        if len( mat )> 0:
             unpack = mat[0];
        return unpack ;

#==============================================================================
#==============================================================================

def RemlinesF1(csvfile, remlines = [0,1,2,3] ):
        import csv ;
        import shutil;
        import os; 
        shutil.copyfile( csvfile, csvfile +'.bak' )
        finp  = open( csvfile      , 'r');
        fout  = open( 'tempout'    , 'w', newline='\n');
        writer = csv.writer( fout, dialect='unix' ) ;
        irow = 0 ;
        for row in ( csv.reader( finp) ) :
            irow +=1 ;
            if irow in remlines :
                pass; ## skip;
            else:
                writer.writerow( row );
        finp.close();
        fout.close();
        shutil.copyfile( 'tempout', csvfile );

def RemlinesF(csvfile, remlines = [0,1,2,3] ):
        import csv ;
        import shutil;
        import os; 
        shutil.copyfile( csvfile, csvfile +'.bak' )
        finp  = open( csvfile      , 'rb');
        fout  = open( 'tempout'    , 'wb', newline='\n');
        writer = csv.writer( fout, dialect='unix' ) ;
        irow = 0 ;
        for row in ( csv.reader( finp) ) :
            irow +=1 ;
            if 1: 
                writer.writerow(row);
            if 0: 
              if irow in remlines :
                pass; ## skip;
              else:
                writer.writerow(row);
        finp.close();
        fout.close();
        shutil.copyfile( 'tempout', csvfile );
    


# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def getsimfile( inpfile ):
    simfile = os.path.split( inpfile)[1].rstrip( 'run.log') 
    return simfile ;

def getsimcase( inpfile ):
    #getfilesbe ( inppath, begkw=None, endkw='.csv', PSH=[0, 0 ] )
    simfile = getfilesbe( inpfile, begkw=None, endkw='sim', PSH=[0, 0 ] )
    #simfile = getFilesbe( inppath, ndef=1, KW_LOG='sim' ); 
    simcase = simfile.rstrip( '.sim') ;
    return simcase ;



#==============================================================================
##{ FOOTER }##################################################################{
# In[000.001]: VERSIONING
__VERSIONING__={
    231114.1625:''' ''',
    231114.1633:''' ''',
    231114.1800:''' added platform.uname().system''',
    240120.1515:''' VV wisk.initsetfile, wisk.showheader(...), wisk.showeval(...),
                    imporved the functionality of wisk.showeval etc
                ''',
    240214.0035:''' makeslides( +PPTXFILE=, +PPTXPATH=  )
                ''',
    240223.2206:''' 
      ++ TabulateGroup( ...) ; thermocouple signals output
      @2024-02-22-1606J - verified batch 
      ''',
    240301.2140:''' added options MakeSlides( pw_set, ph_set, and pwhmax ) ::=)     ''' ,
    240316.1309:''' fixing setcae and case, adding makeSlides( pptsavename=(setcase...)''',   
};

##############################################################################}

