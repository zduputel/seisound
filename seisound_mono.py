#!/usr/bin/env python
# A simple script to listen seismograms in mono
# i.e., create a mono wav Audio file from SAC data
# Z. Duputel -- November 2015

from datetime import datetime, timedelta
import os, sys, wave, time, struct
import scipy as sp

def rsac(FILE):
    '''
    Reads sac file
    Args:
        - FILE: input file
    ''' 
    try:
        fid     = open(FILE,'rb')
        delta   = float(sp.fromfile(fid,'float32',   1)[0])
        fid.seek(20,0)
        b       = float(sp.fromfile(fid,'float32',   1)[0])
        fid.seek(280,0);
        nzyear  = int(sp.fromfile(fid,  'int32',   1)[0])
        nzjday  = int(sp.fromfile(fid,  'int32',   1)[0])
        nzhour  = int(sp.fromfile(fid,  'int32',   1)[0])
        nzmin   = int(sp.fromfile(fid,  'int32',   1)[0])
        nzsec   = int(sp.fromfile(fid,  'int32',   1)[0])
        nzmsec  = int(sp.fromfile(fid,  'int32',   1)[0])
        fid.seek(316,0)
        npts    = int(sp.fromfile(fid,  'int32',   1)[0])
        fid.seek(632,0);
        depvar  = sp.array(sp.fromfile(fid,'float32',npts),dtype='f')
        fid.close();
        return [depvar,delta,npts,b, nzyear,nzjday,nzhour,nzmin,nzsec,nzmsec]
    except IOError:
        sys.stderr.write('error reading file '+FILE+'!!!\n')
        sys.exit(1)
        
        
def seisound_mono(sacfile,wavfile='o_seismosound.wav',acc = 3125,format='i'):
    '''
    Reads a SAC file, speed it up and write it in a wav file
    Args:
        - sacfile: the input SAC file
        - wavfile: the output wav file
        - acc: speedup factor
        - format: data format in wav file
    '''
    if os.path.exists(wavfile):
        os.remove(wavfile)
    
    # Read sac file
    depvar,delta,npts,b,nzyear,nzjday,nzhour,nzmin,nzsec,nzmsec = rsac(sacfile);

    # Sampling rate
    fsamp  = int(acc/delta) ;
        
    # Format conversion 
    Nbytes =  struct.calcsize(format)
    depvar = sp.cast[format](depvar/sp.absolute(depvar).max() * (2**(Nbytes*8-1)-1))
    
    # Write wav file
    w = wave.open(wavfile,'w')
    w.setparams((1,Nbytes,fsamp,0,'NONE','not compressed'))
    for i in xrange(npts):
        v_1 = struct.pack(format,depvar[i])
        w.writeframes(v_1)
    w.close()
    
    
if __name__=="__main__":


    # Explosion in Tianjin harbor in 2015
    #sacfile = 'explosion_Tianjin2015/2015.224.15.30.00.0195.IC.BJT.00.BHZ.M.SAC'
    #wavfile = 'explosion_Tianjin2015/o_givemesound.wav'
    #acc =   300. ;

    # 2013 Nuclear explosion in North Korea
    #sacfile = 'meteor_russia2013/2013.046.03.10.00.0195.II.ARU.00.BHZ.M.SAC.filt.sac.cut.sac'
    #wavfile = 'meteor_russia2013/o_givemesound.wav'
    #acc =   300. ;        

    # Piton de la fournaise Eruption
    #sacfile = 'eruption_PitonDeLaFournaise/PF.BOR.00.EHZ.Q.SAC'
    #wavfile = 'eruption_PitonDeLaFournaise/o_givemesound.wav'
    #acc = 300. ;        

    # 2008 Sichuan earthquake (Mw=7.9)
    #sacfile1 = 'seisme_sichuan_2008/2008.133.06.33.30.9999.G.ECH.10.LHZ.R.SAC' ;
    #sacfile2 = 'seisme_sichuan_2008/2008.133.06.33.30.9999.G.ECH.10.LHZ.R.SAC' ;
    #wavfile  = 'seisme_sichuan_2018/o_seismosound.wav
    #acc = 3000. ;

    # 2004 Sumatra-Andaman earthquake (Mw=9.1)
    #sacfile = 'seisme_sumatra_2004/2004.361.00.41.29.0095.II.BFO.00.BHZ.M.SAC'
    #wavfile = 'seisme_sumatra_2004/o_givemesound.wav'
    #acc = 1500. ;    

    # Get input parameters
    if len(sys.argv)!=4:
        sys.stderr.write('Syntax: %s sacfile wavfile speedup_factor\n'%sys.argv[0])
    else:
        sacfile = sys.argv[1]
        wavfile = sys.argv[2]
        speedup = float(sys.argv[3])

        # run the code
        seisound_mono(sacfile,wavfile,speedup,'i')
    

