#!/bin/bash 

# Data should be downloaded using get_OVPF_data.py before using this script

# Input parameters
sacfile1='./PF.FOR.00.HHZ.SAC'
sacfile2='./PF.BOR.00.EHZ.SAC'
wavfile='PDLFJune2014_stereo.wav'
speedup=300.

# Speedup factor
python ../../seisound_stereo.py $sacfile1 $sacfile2 $wavfile $speedup
