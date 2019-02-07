#!/usr/bin/env python

import obspy

# Get data from eida.ipgp.fr
BOR = obspy.read('http://eida.ipgp.fr/fdsnws/dataselect/1/query?start=2014-06-20T20:10:00&end=2014-06-21T20:10:00&net=PF&sta=BOR&loc=00&cha=EHZ')
FOR = obspy.read('http://eida.ipgp.fr/fdsnws/dataselect/1/query?start=2014-06-20T20:10:00&end=2014-06-21T20:10:00&net=PF&sta=FOR&loc=00&cha=HHZ')

# Build a stream
stream = obspy.Stream(traces=[BOR[0],FOR[0]])

# Trim data
start = obspy.UTCDateTime(2014,06,20,20,11,00)
end   = obspy.UTCDateTime(2014,06,21,17,00,00)
stream.trim(start,end)

# Write in sac format
for t in stream:
    fname = t.get_id()+'.SAC'
    t.write(fname,format='SAC')
