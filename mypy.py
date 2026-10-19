#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings;warnings.simplefilter(action='ignore', category=FutureWarning);# Suppress FutureWarning
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import myfavs as my;
import danpy as dan;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# basics
import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;
import matplotlib as mpl;
import seaborn as sns;
from scipy import stats;
# %matplotlib inline # uncomment only in jupyter
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# sci-kit modeling
from sklearn.metrics import mean_squared_error, r2_score;
from sklearn.model_selection import train_test_split,cross_val_score,cross_val_predict,GridSearchCV;
from sklearn.preprocessing import PolynomialFeatures, StandardScaler;
from sklearn.pipeline import Pipeline;
from sklearn.linear_model import LinearRegression, Ridge;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import requests; ## for json webscrapping requests
import folium;   ## maps
import json;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# dashboards
import plotly.express as px ;
import dash ;
from dash import html ;
from dash import dcc ;
from dash.dependencies import Input, Output ;
#import dash_html_components as html ; ## deprecated
#import dash_core_components as dcc ;  ## deprecated
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import warnings ; ## Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning) ;## loadimports.py
'''
import loadimports; ### load imports...
for r in loadimports.impload(): exec(r);
'''


class loadimports:
    notvalid='''import ;
    for r in loadimports.impload(): exec(r);
     partially initialized module 'myimports' has no attribute 'impload' (most likely due to a circular import)
     '''
    ##############################################################################
    # In[0]: 
    def impload( show=False ):
        impfile = '/Users/dac/pylab/lib/imports.py';
        myimp = list();
        ignore="#"; 
        with open( impfile ,'r',newline='\n') as inp:
            for row in inp:  #.readline():
                #row = inp.read();
                row = row.strip('\n');
                if len(ignore)>0:
                    ##print(f"testing {ignore}")
                    if show: print (row);
                    if row.startswith( ignore ):
                        pass;
                    else: myimp.append(row);
                else:     myimp.append(row);
        inp.close();
        return myimp; ## list of imports
    def imprecall( myimp ):
        if len(myimp)<1:
            myimp = impload();
        f=" {} \t {} "
        for i,r in enumerate( myimp):
            print( (f).format( str(i+1), str(r) ));
        return myimp;
    
    def impshow( ):
        myimp = impload();
        f="{1}"
        for i,r in enumerate( myimp):
            print( (f).format( str(i+1), str(r) ));
        return myimp;
        
    def impexec( myimp=[], ii=0, ):
        if len(myimp)<1:
            myimp = impload();
        if ii==0: ## importing all
            print("doing all! ");
            for each in myimp:
                print(f"doing .. {each}");
                exec( each );
        else:
            each = myimp[ii-1];
            print(f"doing .. {each}");
            exec( each );
    
    def hint():
        hint='''
        # load imports:
        for r in loadimports.impload(): exec(r);
        '''
        print( hint );
        return hint;
    def loadall():
        """
        for r in loadimports.impload(): exec(r);"""
        for r in loadimports.impload(): exec(r);
    # hint() ;
    ##############################################################################
    # if 0: 
    #     for r in loadimports.impload(): exec(r);
    #     h = loadimports.hint(); print( h );
    # if __name__=='__main__':
    #     hint() ;
    #     #myimp = impload( show=False);
    #     #print( myimp );
    #     #imprecall( myimp) ;
    #     #importsrecall( myimp );
    #     impexec( [], ii=0);
##############################################################################

##!/usr/bin/env python3
## -*- coding: utf-8 -*-
"""
myfavs.py

Created on Tue Oct  8 09:47:01 2024

@author: dac
"""

##############################################################################
# In[0]: Load packages
#------------------------------------------------------------------------------
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

#import requests
#import bs4 
#import seaborn as sn;
#-----------------------------------------------------------------------------#
###############################################################################
def goloadimports():
    """
    for r in loadimports.impload(): exec(r);
    loaded = pd.DataFrame( loadimports.impload(), columns=['load'] ); print(loaded);
    """
    import loadimports;
    for r in loadimports.impload(): exec(r);
    loaded = pd.DataFrame( loadimports.impload(), columns=['load'] ); print(loaded);
    hint="""
    for r in loadimports.impload(): exec(r);
    loaded = pd.DataFrame( loadimports.impload(), columns=['load'] ); print(loaded);
    """
    print(hint);
    return loaded;

###############################################################################
EXE = {
       'inp':   None, # (os.getcwd() ),
       'v':     False,
      };
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#import myfavs as my;
###############################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hr = 60*'==';
br = 60*'--';
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

def brsep(pr=False, c='*', n=80, a=0, e=0):
    br = ( a*'\n' + n*f'{c}' +  1*e*'\n');
    #br = ( a*'\n' +   '{}'  +  1*e*'\n').format( c * n);
    if pr: print(br,  end='' ); #+ e*'\n');
    return br;

def alphabet():
    alphabet = [chr(i) for i in range(65, 65+26) ]
    return alphabet;

def smybols():
    alphabet = [chr(i) for i in range(32, 64) ]
    return alphabet;

def pcenter( s, spad="#",sp = " ",n=60, pr=True):
    e = (int(n/2) - int((len(s)+len(sp))/2) )//len(spad);
    R = str( (e)*spad + (sp)+(s)+(sp) +(e)*spad) ;
    if pr: print(f"{R}");
    return R

def pleft( s, spad="#",sp = " ",n=60, rpad="-", pr=True):
    jle =  4;
    jre =  max(0,n - (jle*len(spad) + len(s) + 5*len(sp)));
    #if jre <1: jre=0;
    R = str( (jle)*spad + (1*sp)+(s)+(4*sp) +(jre)*rpad);
    if pr: print(f"{R}");
    return R

######################################################################
  
def whoami( x ):
    print( type( x) )
    #if type(x) == 
    print( )
    return None;



######################################################################

###############################################################################
# Months to Months
#------------------------------------------------------------------------------
month2mon={
        'Jan' :  1 ,
        'Feb' :  2 ,
        'Mar' :  3 ,
        'Apr' :  4 ,
        'May' :  5 ,
        'Jun' :  6 , 
        'Jul' :  7 ,
        'Aug' :  8 ,
        'Sep' :  9 ,
        'Oct' :  10 ,
        'Nov' :  11 ,
        'Dec' :  12 ,
}
mon2month={
        1: 'Jan', 
        2: 'Feb', 
        3: 'Mar', 
        4: 'Apr', 
        5: 'May', 
        6: 'Jun', 
        7: 'Jul', 
        8: 'Aug', 
        9: 'Sep', 
        10: 'Oct', 
        11: 'Nov', 
        12: 'Dec',
    }
def get_mon2month():
    return mon2month;

def get_month2mon():
    return month2mon;

def get_months( out='s' ):
    '''
    set out to s for making Jan..Dec
    set out to i for making 01.. 12
    '''
    if out=='i':
        return month2mon;
    if out=='s':
        return month2mon;

def monthsordered( rettype='list' ):    
    pass;

def monthstr_2_monint(dfa, colmonth='Month'):
    MON=list();
    #colmonth='Month'
    for d in dfa[colmonth]:
        m = 0 +\
        1*(d=='Jan') +\
        2*(d=='Feb') +\
        3*(d=='Mar') +\
        4*(d=='Apr') +\
        5*(d=='May') +\
        6*(d=='Jun') +\
        7*(d=='Jul') +\
        8*(d=='Aug') +\
        9*(d=='Sep') +\
       10*(d=='Oct') +\
       11*(d=='Nov') +\
       12*(d=='Dec') ;
        m = int(m);
        #print( d, m);
        MON.append(m);
    dfa['Mon'] = pd.DataFrame( MON );
    return dfa;
###############################################################################


######################################################################
# WRANGLE AND CLEAN
######################################################################

def reportaction( action, do=True ):
    print( pcenter( action,n=80,sp="  ") );
    if do:
     eval( 'print( {} ) '.format( action ));
    print( pcenter( "#",n=80,sp="") );
#=====================================================================
def dfcorr( df ):
    " look for not floats and drop or convert with dummies"
    
    pass;
#=====================================================================
# made special for reporting df characterisitics:dfcharacter(df) ----
def dfcharacter( df ):
    do=True;
    LACTIONS=[
        'df.shape',
        'df.columns',
        'df.head()',
        'df.info()',
        'df.describe()',
        #'df.corr()',
        #'my.report_missing(df)'
        'report_missing(df)'
    ]
    for action in ( LACTIONS ):
        #reportaction( h, do =False );
        print( pcenter( action,n=80,sp="  ") );
        #if do:
        eval( 'print( {} ) '.format( action ));
        print( pcenter( "#",n=80,sp="") );
#=====================================================================
##  test for missing
def missing(df):
    missing_data = df.isnull();
    print( missing_data.head(5) );
    for column in missing_data.columns.values.tolist():
        print(column);
        print (missing_data[column].value_counts());
        print("") ;
#=====================================================================
def report_missing( df , showreport=False ):
    missing_data = df.isnull() ;
    #missing_data.head(5) 
    report=list();
    for column in missing_data.columns.values.tolist():
        ct = missing_data[column].value_counts()[0] ;
        gr = missing_data[column].shape[0] ;
        null = gr - ct;
        report.append( [ column, ct, null, gr ] );
        #print (missing_data[column].value_counts())
        #print("")  
    rp = pd.DataFrame( data=report, index=None, columns=['col','nonull','Nulls', 'Size']);
    if showreport:
        pcenter( f" Showing report for df ");
        print(rp);
        pbr();
    return rp;
#=====================================================================
# Cleaning
## replace duds 
def cleanval( df ):
    s = '?'
    df.replace( s, np.nan, inplace=True);
    return df;
#=====================================================================
## repalce with mean
def replacemean(df, xlab ):
    pass   
    mu = df[ xlab ].astype("float").mean(axis=0);
    #mu
    df[ xlab ].replace( np.nan, mu, inplace=True) ;
    return df;

## replace with top frequent
def replacefreq( df, xlab, show=True, replace=True) :
    x1  = df[ xlab ].value_counts();
    top = vct = df[ xlab ].value_counts().idxmax(); 
    #print( "counts ", x1, "idmax: ", x2 )
    #top = vct
    if show: print ("top count: ", top)
    if replace: df[ xlab ].replace( np.nan, top, inplace=True);
    return df ;


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

def cwd():
    """ returns the current directory
    """
    cwd = os.getcwd();
    return cwd; 


###############################################################################
def initsetfile ( SETFILE, ofile=None, setkey=None ):
    """
    initialize ofile based on SETFILE
    return ofile[key]
    """
    if ofile==None: ofile = {} ;    
    thisfile = SETFILE 
    if 1:        
      if type(setkey) == str or int: k=setkey
      else: k=0;
      #if PSH[0]:
      #print('setkey', end='..', sep='.. ')
      #print( setkey )
    if 1:        
      ofile[k] =(open( thisfile, 'w',encoding='utf-8',newline=None, )).write('' );
      ofile[k] =(open( thisfile, 'a',encoding='utf-8',newline='\n', ));
    return ofile ;

def showheader( listparm, wf=None, ):
    for k, p in enumerate( listparm  ) : 
        if k < len( listparm  ) -1: 
              print(('{}'+1*','+0*' ').format( str( (p)) ), sep='', end=''  ,file=wf )
        else: print(('{}'+0*','+0*' ').format( str( (p)) ), sep='', end='\n',file=wf )
def showkeys( DICT, wf=None, ):
    for i, k in enumerate( DICT) : 
        p = DICT.get(k)
        print(('{:<3s} : {:<5s} : {}').format( str(i),str(k),str( p) ),
              sep='',end='\n',file=wf );
###############################################################################

def getdf(Selectfiles, PSH):
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
###############################################################################

def getArgs( EXE= {} ):
    '''
    return EXE = getArgs() ;
    EXE = {
          };
    '''
  ##-----------------------------------------------------------    
    ##INARGS={};
    __doc__=''' '''
    __version__=''' '''
    __usage__=''' '''
    parser = argparse.ArgumentParser();
    parser.add_argument("-inp",
            nargs=1, type=str, default='' ,
            help="__<str:>: path of inputh file ",
            action='store',);
    args   = parser.parse_args();
    if (args.inp)!=None: EXE['inp'] = args.inp; print("will do inp: {}".format(args.inp));

    if EXE['v']: print( __doc__, __version__, __usage__ , end='\n\n' );
    return EXE ;

###############################################################################


def normalize( y, opt=2 ):
    """ y: dataframe-series 
    opt==1: y/ymax
    opt==2: y-ymin / ymax-ymin >def<
    """
    if opt==1:
        ynorm = (y )/ (y.max());
    if opt==2:
        ynorm = (y - y.min())/(y.max() - y.min());
    return ynorm;


##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##


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
##!/usr/bin/env python3
## -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 09:47:01 2024

@author: dac
"""


##############################################################################
# In[0]: Load packages
#------------------------------------------------------------------------------
####  Import Packages
#import lib_tcpro as tcpro ;
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

#import requests
#import bs4 
#import seaborn as sn;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#import myfavs as my;

#-----------------------------------------------------------------------------#
import myimports;
def loadall_hint():
    hint='''
    # load imports:
    for r in loadimports.impload(): exec(r);
    '''
    print( hint );

def loadimports():
    """
    for r in loadimports.impload(): exec(r);
    loaded = pd.DataFrame( loadimports.impload(), columns=['load'] ); print(loaded);
    """
    for r in loadimports.impload(): exec(r);
    loaded = pd.DataFrame( loadimports.impload(), columns=['load'] ); print(loaded);
    hint="""
    for r in loadimports.impload(): exec(r);
    loaded = pd.DataFrame( loadimports.impload(), columns=['load'] ); print(loaded);
    """
    print(hint);
    return loaded;

###############################################################################
EXE = {
       'inp':   None, # (os.getcwd() ),
       'v':     False,
      };

PATH_LIB = r'/Users/dac/pylab/lib/';
###############################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
hr = 60*'==';
br = 60*'--';
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def PRDIV( s="=", n=80, ):  
    p = '{}'.format( (n)*(s) );
    return str(p) ;

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

def alphabet():
    alphabet = [chr(i) for i in range(65, 65+26) ]
    return alphabet;

def smybols():
    alphabet = [chr(i) for i in range(32, 64) ]
    return alphabet;
    
def whoami( x ):
    print( type( x) )
    #if type(x) == 
    print( )
    return None;

######################################################################
def pcenter( s, spad="#",sp = " ",n=60, pr=True):
    e = (int(n/2) - int((len(s)+len(sp))/2) )//len(spad);
    R = str( (e)*spad + (sp)+(s)+(sp) +(e)*spad) ;
    if pr: print(f"{R}");
    return R

def pleft( s, spad="#",sp = " ",n=60, rpad="-", pr=True):
    jle =  4;
    jre =  max(0,n - (jle*len(spad) + len(s) + 5*len(sp)));
    #if jre <1: jre=0;
    R = str( (jle)*spad + (1*sp)+(s)+(4*sp) +(jre)*rpad);
    if pr: print(f"{R}");
    return R

def reportaction( action, do=True ):
    print( pcenter( action,n=80,sp="  ") );
    if do:
     eval( 'print( {} ) '.format( action ));
    print( pcenter( "#",n=80,sp="") );

def dfcorr( df ):
    " look for not floats and drop or convert with dummies"
    
    pass;
######################################################################
# made special for reporting df characterisitics:dfcharacter(df) ----
def dfcharacter( df ):
    do=True;
    LACTIONS=[
        'df.shape',
        'df.columns',
        'df.head()',
        'df.info()',
        'df.describe()',
        #'df.corr()',
        'my.report_missing(df)'
    ]
    for action in ( LACTIONS ):
        #reportaction( h, do =False );
        print( pcenter( action,n=80,sp="  ") );
        #if do:
        eval( 'print( {} ) '.format( action ));
        print( pcenter( "#",n=80,sp="") );

######################################################################

######################################################################

######################################################################
# WRANGLE AND CLEAN
######################################################################
##  test for missing
def missing(df):
    missing_data = df.isnull();
    print( missing_data.head(5) );
    for column in missing_data.columns.values.tolist():
        print(column);
        print (missing_data[column].value_counts());
        print("") ;
def report_missing( df , showreport=False ):
    missing_data = df.isnull() ;
    #missing_data.head(5) 
    report=list();
    for column in missing_data.columns.values.tolist():
        ct = missing_data[column].value_counts()[0] ;
        gr = missing_data[column].shape[0] ;
        null = gr - ct;
        report.append( [ column, ct, null, gr ] );
        #print (missing_data[column].value_counts())
        #print("")  
    rp = pd.DataFrame( data=report, index=None, columns=['col','nonull','Nulls', 'Size']);
    if showreport:
        pcenter( f" Showing report for df ");
        print(rp);
        pbr();
    return rp;

# Cleaning
## replace duds 
def cleanval( df ):
    s = '?'
    df.replace( s, np.nan, inplace=True);
    return df;

## repalce with mean
def replacemean(df, xlab ):
    pass   
    mu = df[ xlab ].astype("float").mean(axis=0);
    #mu
    df[ xlab ].replace( np.nan, mu, inplace=True) ;
    return df;

## replace with top frequent
def replacefreq( df, xlab, show=True, replace=True) :
    x1  = df[ xlab ].value_counts();
    top = vct = df[ xlab ].value_counts().idxmax(); 
    #print( "counts ", x1, "idmax: ", x2 )
    #top = vct
    if show: print ("top count: ", top)
    if replace: df[ xlab ].replace( np.nan, top, inplace=True);
    return df ;


###############################################################################
month2mon={
        'Jan' :  1 ,
        'Feb' :  2 ,
        'Mar' :  3 ,
        'Apr' :  4 ,
        'May' :  5 ,
        'Jun' :  6 , 
        'Jul' :  7 ,
        'Aug' :  8 ,
        'Sep' :  9 ,
        'Oct' :  10 ,
        'Nov' :  11 ,
        'Dec' :  12 ,
}
longmonth2mon={
        'January' :  1 ,
        'February' :  2 ,
        'March' :  3 ,
        'April' :  4 ,
        'May' :  5 ,
        'June' :  6 , 
        'July' :  7 ,
        'August' :  8 ,
        'September' :  9 ,
        'October' :  10 ,
        'November' :  11 ,
        'December' :  12 ,
}
mon2longmonth={
        1: 'January', 
        2: 'February', 
        3: 'March', 
        4: 'April', 
        5: 'May', 
        6: 'June', 
        7: 'July', 
        8: 'August', 
        9: 'September', 
        10: 'October', 
        11: 'November', 
        12: 'December',
    }
mon2month={
        1: 'Jan', 
        2: 'Feb', 
        3: 'Mar', 
        4: 'Apr', 
        5: 'May', 
        6: 'Jun', 
        7: 'Jul', 
        8: 'Aug', 
        9: 'Sep', 
        10: 'Oct', 
        11: 'Nov', 
        12: 'Dec',
    }

def get_mon2month():
    return mon2month;

def get_month2mon():
    return month2mon;

def get_months( out='s' ):
    '''
    set out to s for making Jan..Dec
    set out to i for making 01.. 12
    '''
    if out=='i':
        return month2mon;
    if out=='s':
        return month2mon;

def monthconv( out='s' ):
    '''
    set out to s for making Jan..Dec
    set out to i for making  01.. 12
    '''
    if out=='i':
        return month2mon;
    if out=='s':
        return month2mon;

def monthsordered( rettype='list' ):
    
    pass;


def monthstr_2_monint(dfa, colmonth='Month'):
    MON=list();
    #colmonth='Month'
    for d in dfa[colmonth]:
        m = 0 +\
        1*(d=='Jan') +\
        2*(d=='Feb') +\
        3*(d=='Mar') +\
        4*(d=='Apr') +\
        5*(d=='May') +\
        6*(d=='Jun') +\
        7*(d=='Jul') +\
        8*(d=='Aug') +\
        9*(d=='Sep') +\
       10*(d=='Oct') +\
       11*(d=='Nov') +\
       12*(d=='Dec') ;
        m = int(m);
        #print( d, m);
        MON.append(m);
    dfa['Mon'] = pd.DataFrame( MON );
    return dfa;
###############################################################################
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

def alphabet():
    alphabet = [chr(i) for i in range(65, 65+26) ]
    return alphabet;

def smybols():
    alphabet = [chr(i) for i in range(32, 64) ]
    return alphabet;


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

def cwd():
    """ returns the current directory
    """
    cwd = os.getcwd();
    return cwd; 

def brsep1(pr=False, c='*', n=80 ):
    b = ('\n{}\n').format( c * n);
    if pr: print(b);
    return b;

def brsep(pr=False, c='*', n=80, a=0, e=0):
    br = ( a*'\n' + n*f'{c}' +  1*e*'\n');
    #br = ( a*'\n' +   '{}'  +  1*e*'\n').format( c * n);
    if pr: print(br,  end='' ); #+ e*'\n');
    return br;

def pbr(i=1,n=60,):
    symbols= '''#=-~''';
    br = n*symbols[i] ;
    print (br);


###############################################################################
def initsetfile ( SETFILE, ofile=None, setkey=None ):
    """
    initialize ofile based on SETFILE
    return ofile[key]
    """
    if ofile==None: ofile = {} ;    
    thisfile = SETFILE 
    if 1:        
      if type(setkey) == str or int: k=setkey
      else: k=0;
      #if PSH[0]:
      #print('setkey', end='..', sep='.. ')
      #print( setkey )
    if 1:        
      ofile[k] =(open( thisfile, 'w',encoding='utf-8',newline=None, )).write('' );
      ofile[k] =(open( thisfile, 'a',encoding='utf-8',newline='\n', ));
    return ofile ;

def showheader( listparm, wf=None, ):
    for k, p in enumerate( listparm  ) : 
        if k < len( listparm  ) -1: 
              print(('{}'+1*','+0*' ').format( str( (p)) ), sep='', end=''  ,file=wf )
        else: print(('{}'+0*','+0*' ').format( str( (p)) ), sep='', end='\n',file=wf )
def showkeys( DICT, wf=None, ):
    for i, k in enumerate( DICT) : 
        p = DICT.get(k)
        print(('{:<3s} : {:<5s} : {}').format( str(i),str(k),str( p) ),
              sep='',end='\n',file=wf );
###############################################################################

def getdf(Selectfiles, PSH):
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
###############################################################################
def examples():
    def matchcase(term, pattern=[0,1,2,3], action={0:0,1:0,2:0,3:0,'def':0}):
        pass;
        '''
        match term:     
            case pattern[1]:
                 pass; #action action[1]
            case pattern[2]:
                 action
            case pattern[3]:
                 action
            case _:
                action[0] ## default action
        '''
def getArgs( EXE= {} ):
    '''
    return EXE = getArgs() ;
    EXE = {
          };
    '''
  ##-----------------------------------------------------------    
    ##INARGS={};
    __doc__=''' '''
    __version__=''' '''
    __usage__=''' '''
    parser = argparse.ArgumentParser();
    parser.add_argument("-inp",
            nargs=1, type=str, default='' ,
            help="__<str:>: path of inputh file ",
            action='store',);
    args   = parser.parse_args();
    if (args.inp)!=None: EXE['inp'] = args.inp; print("will do inp: {}".format(args.inp));

    if EXE['v']: print( __doc__, __version__, __usage__ , end='\n\n' );
    return EXE ;

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##
##===========================================================================##
def loadcfg( cfgfile='qstar_CFG.txt', SKIP='##~', SHOW=False ):
    """
    cfgfile : <str> filename of cfg file
        * default 'qstar_CFG.txt'.
    SHOW : <Bool> show print out
        * default False.
    SKIP : <str> skip over processing the line if starting with SKIP
        * default '##~'
    -------Returns: -------
    CFG: Dict: of parameters loaded from cfg file
      key: parameter
    """
    #SKIP='##~';
    #SHOW=False;
    #cfgfile='qstar_CFG.txt';
    CFG = dict();
    with open( cfgfile , 'r', newline='\n' ) as f:
        for line in f:
            line = line.rstrip('\n')
            if SHOW: print( line );
            if line.startswith( SKIP ):
                pass; ## skip line don't process
            elif line.startswith('#' ):
                key = line.lstrip('#');
                print(key)
                WW=list(); 
            else:
                for e in line.split(','):
                    WW.append(e);  
                CFG[key] = WW;
    f.close();
    return CFG;
##===========================================================================##
def savecfg( CFG, cfgfile='cfg.txt', SHOW=False ):
    #SHOW=False;
    #cfgfile='cfg.txt';
    #CFG = dict();
    with open( cfgfile , 'w', newline='\n' ) as f:
        for k in CFG.keys():

            print( '{}{}'.format('#', k ), end='\n',file=f);
            v = CFG.get(k);
            if type(v)==list:
                for w in v:
                    print( '{}'.format( w ), end=',',file=f);
            print( '\n'.format( ), end='',file=f);
        
    f.close();
    return CFG;
#-----------------------------------------------------------------------------#
def getfilesbe ( inppath, begkw=None, endkw='.csv', PSH=[0, 0 ] ):
    '''
    Return FILESETPATHS <list of strings>
    Parameters
    ----------
    inppath [str]
        DESCRIPTION.
    begkw [str]
        keyword for files to be sought in path, def = None
    endkw [str]
        keyword for end of file name, def='csv'
    PSH [list]
        toggles for PrintOut
        *default is [0, 0 ].

    '''
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

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##
def getsimfile( inp ):
    simfile = os.path.split(inp)[1];
    simfile = simfile.rstrip( 'run.log' );
    simfile = simfile.rstrip( '.' );
    simfile = simfile.rstrip( '-' );
    simfile = simfile.rstrip( '~' );
    return simfile ;

'''
def getsimcase_v310( inp, method='log' ): ## requires python v > 3.10
    match str(method):
        case 'rfile':
            simfile = os.path.split(inp)[1];
            simfile = simfile.rstrip( 'run.log' );
        case 'sim':
            simfile = getfilesbe( inp, endkw='sim' );
        case 'log': 
            simfile = getfilesbe( inp, endkw='run.log' );
            simfile = simfile.rstrip( 'run.log' ) ;

    simfile = simfile.rstrip( 'run.log' );
    simfile = simfile.rstrip( '.' );
    simfile = simfile.rstrip( '-' );
    simfile = simfile.rstrip( '~' );
    simfile = simfile.rstrip( '.sim' );
    return simfile ;
'''
def getsimcase( inp, method='log' ): ## requires python v > 3.10
    if method=='rfile':
            simfile = os.path.split(inp)[1];
            simfile = simfile.rstrip( 'run.log' );
    if method=='sim':
            simfile = getfilesbe( inp, endkw='sim' );
    if method=='log': 
            simfile = getfilesbe( inp, endkw='run.log' );
            simfile = simfile.rstrip( 'run.log' ) ;

    simfile = simfile.rstrip( 'run.log' );
    simfile = simfile.rstrip( '.' );
    simfile = simfile.rstrip( '-' );
    simfile = simfile.rstrip( '~' );
    simfile = simfile.rstrip( '.sim' );
    return simfile ;

# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
PATH_SLIDEMASTER = r'/Users/dac/pylab/lib/';

#####################################################################
# In[1]: ##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def find_time_label( Fnames, SHOW=False ):
    ctlist=list();
    for f in Fnames: 
        y = re.search(r'(?i).(time)', f, re.IGNORECASE);
        if y != None: # if len(y)>0:
            ctlist.append( y.group() )
    if SHOW: print(ctlist)        
    return ctlist;

#####################################################################

def set_psh( e, verb='V' ):
    '''
    PSH = set_psh( e ) 
    >> finds instances of verb(='V') where e = EXE['v'] 
    '''
    PSH =[0 for i in range(0,100)] ; ## initializing PSH 
    import re;    
    w = re.findall( verb , e ); #print(w)
    r = [( verb in k )*int(1) for k in w ]; #print (r);
    PSH = r + PSH ; #print (r)    
    return PSH ;
    
#####################################################################

def get_html( url ): ## DAC:soupstock
    r = requests.get( url );
    html_data = ( r ).text ;
    return html_data;
def get_soup( html_data ): ## DAC:soupstock
    soup = BeautifulSoup( html_data, 'html.parser') ; 
    return soup ; 
#####################################################################
