#!/bin/bash 

# Data should be downloaded using get_OVPF_data.py before using this script

# Input parameters
sacfile1='./IU.CHTO.00.LHZ.M.2004.361.005352.SAC'
sacfile2='./II.BFO.00.LHZ.M.2004.361.005352.SAC'
wavfile='sumatra_earthquake_2004_stereo.wav'
speedup=3000.

# Speedup factor
python ../../seisound_stereo.py $sacfile1 $sacfile2 $wavfile $speedup
