# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 12:27:06 2023

@author: daniel.collins
"""

def TempsAtTmax( DSTAT ):
    '''
return:
    RETCO = {
        'kxm' : kmx,
        'kend': kend,
        'tmax': Tat['max'],
        'TminAtTmax':Tat['min'],
        'TdelAtTmax':Tat['del'],        
        }
    
    '''
    #DSTAT = tcpro.Drawers( RGDF, JGRPBEG, 
    #  KEYCHANNELS.loc[JGRPBEG:JGRPEND,'Alias'], DEB=False ) ;
    kmx  = DSTAT['kmx'] ;
    kend = len(DSTAT['LMAX']) ;
    Tat = {
      'max' : DSTAT['LMAX'][DSTAT['kmx']],
      'min' : DSTAT['LMIN'][DSTAT['kmx']]
    }
    Tat['del'] = Tat['max'] - Tat['min']  ;
    if 0: print( '''
   smp# Tmax: {:d}
   smp  Last: {:d}
       Tmax:  {:3.1f}
       Tmin:  {:3.1f}
         dT:  {:3.1f} '''.format( kmx, kend, Tat['max'],Tat['min'],Tat['del']
          ));

    RETCO = {
        'kxm' : kmx,
        'kend': kend,
        'tmax': Tat['max'],
        'TminAtTmax':Tat['min'],
        'TdelAtTmax':Tat['del'],        
        }
    
    return RETCO ;
    
