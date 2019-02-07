# seisound
Simple python scripts to listen to seismograms in mono or stereo.

Output files are in the [WAV format](https://en.wikipedia.org/wiki/WAV). 
To read these files, I recommend [Sonic Visualiser](https://www.sonicvisualiser.org), 
an open source application for viewing and analysing audio files.

## Dependencies
- python2 or python3
- python modules: scipy, wave, datetime, struct

## How to run
There are two scripts:
- seisound_mono.py: Reads a single SAC file, speed it up and write it in a mono WAV file. This script should be used as follows:
```
python seisound_mono.py sacfile wavfile speedup
```
where `sacfile` is the input SAC file name, `wavfile` is the output WAV audio file and `speedup` is the speedup factor.
- seisound_stereo.py: Reads two synchronized SAC files, speed them up and write it a stereo WAV file. To run this script:
```
python seisound_stereo.py sacfile1 sacfile2 wavfile speedup
```
where `sacfile1` and `sacfile2` are the input SAC files, `wavfile` is the output WAV audio file and `speedup` is the speedup factor.

## Examples
Two examples are provided:
- `examples/sumatra_earthquake_2004`: the 2004 Sumatra-Andaman earthquake recorded at two stations (`CHTO` in thailand and `BFO` in germany). 
  You can just run `get_audio_stero.sh` to generate an audio file with a speedup factor of 3000.
- `examples/PitonDeLaFournaise_eruption_June2014`: The June 2014 eruption at the Piton de la Fournaise volcano (La Réunion island) recorded at two seismological stations maintained by the volcano observatory (OVPF). Data can be downloaded using the `obspy` script `get_OVPF_data.py`. 
  Once data is downloaded, you can generate an audio file using `get_audio_stero.sh` (speedup factor = 300).

