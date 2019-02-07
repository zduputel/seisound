#!/usr/bin/env python
# A simple script to listen seismograms in stereo
# i.e., create a stereo wav Audio file from SAC data
# Z. Duputel - 2009

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

def seisound_stereo(sacfile1,sacfile2,wavfile='o_seismosound.wav',acc = 3125,format='i'):
    '''
    Reads two SAC files, speed them up and write them in a wav file
    Args:
        - sacfile1: SAC file name for speaker 1
        - sacfile2: SAC file name for speaker 2
        - wavfile: output wave file name (default: o_givemesound.wav)
        - acc: speedup factor (default:3125)
        - format: data format in wav file
    '''
    if os.path.exists(wavfile):
        os.remove(wavfile)
    
    # Read sac files
    depvar1,delta1,npts1,b1,nzyear1,nzjday1,nzhour1,nzmin1,nzsec1,nzmsec1 = rsac(sacfile1);
    depvar2,delta2,npts2,b2,nzyear2,nzjday2,nzhour2,nzmin2,nzsec2,nzmsec2 = rsac(sacfile2);

    # Check if they are synchronized in time
    D1   = datetime(nzyear1,1,1,nzhour1,nzmin1,nzsec1,0)+timedelta(days = nzjday1 - 1)
    D2   = datetime(nzyear2,1,1,nzhour2,nzmin2,nzsec2,0)+timedelta(days = nzjday2 - 1)
    B1 = time.mktime(D1.timetuple()) + float(nzmsec1)/1000. + b1
    B2 = time.mktime(D2.timetuple()) + float(nzmsec2)/1000. + b2
    assert delta1 == delta2, 'Sac files must have the same sampling step'
    assert npts1 == npts2, 'Sac files must have the same number of samples'
    assert abs(B1-B2) < 0.5*delta1, 'Sac files must be synchronized (shift=%f sec)'%(B1-B2)

    # Sampling rate
    fsamp  = int(acc/delta1) ;
        
    # Format conversion 
    Nbytes =  struct.calcsize(format)
    depvar1 = sp.cast[format](depvar1/sp.absolute(depvar1).max() * (2**(Nbytes*8-1)-1))
    depvar2 = sp.cast[format](depvar2/sp.absolute(depvar2).max() * (2**(Nbytes*8-1)-1))
    
    # Write wav file
    w = wave.open(wavfile,'w')
    w.setparams((2,Nbytes,fsamp,0,'NONE','not compressed'))
    for i in range(npts1):
        v_1 = struct.pack(format,depvar1[i])
        v_2 = struct.pack(format,depvar2[i])
        w.writeframes(v_1)
        w.writeframes(v_2)
    w.close()

    # All done
    return
    
    
if __name__=="__main__":
    
    ## Piton de la Fournaise eruption in June 2014
    #sacfile1 = 'examples/PitonDeLaFournaise_eruption_June2014/PF.DSO.90.EHZ.SAC'
    #sacfile2 = 'examples/PitonDeLaFournaise_eruption_June2014/PF.FOR.00.HHZ.SAC'
    #wavfile  = 'examples/PitonDeLaFournaise_eruption_June2014/o_seismosound.wav'
    #acc = 300. ;    

    ## 2004 Sumatra-Andaman earthquake (Mw=9.1)
    #sacfile1 = 'examples/sumatra_earthquake_2004/IU.CHTO.00.LHZ.M.2004.361.005352.SAC'
    #sacfile2 = 'examples/sumatra_earthquake_2004/II.BFO.00.LHZ.M.2004.361.005352.SAC'
    #wavfile  = 'examples/sumatra_earthquake_2004/o_seismosound.wav'
    #acc = 3000. ;    
    
    # Get input parameters
    if len(sys.argv)!=5:
        sys.stderr.write('Syntax: %s sacfile1 sacfile2 wavfile speedup_factor\n'%sys.argv[0])
    else:
        sacfile1 = sys.argv[1]
        sacfile2 = sys.argv[2]
        wavfile  = sys.argv[3]
        speedup  = float(sys.argv[4])
        
        # run the code
        seisound_stereo(sacfile1,sacfile2,wavfile,speedup,'i')
    

