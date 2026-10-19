# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 16:39:47 2023

@author: daniel.collins
"""

#==============================================================================
# In[000.002]: Load packages
##>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>##

#  Import configurations
import platform;
import os;
from   os import listdir;

import string ;
import math ;
import re ;
import linecache ;
import argparse ;

import pandas as pd ;
import numpy as np ;

import scipy.io ;

##<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<##


#==============================================================================
# In[0000.0000]:# File Separator based on OS
if 1:
    FSS = os.sep ;
if 0:    #---[ File Separator ]-------------------------------------------#
    import platform; # p = platform.uname();
    if 1:
      FS  =  str('\u002f') ;  ## == "/"  # if NOT windows
    if platform.uname().system == 'Windows': # if system is Windows:
      FS  =  str('\u005c') ;  ## == "\"
    FSS =  str(2*FS) ;
    if (0):
      print (' FS  {}'.format(FS ));print (' FSS {}'.format(FSS));print ( type(FSS ));
