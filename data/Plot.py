#!/usr/bin/env python

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType, AInFlag,
                   TempScale, AiChanType, ULException, ULError, AiInputMode)
from time import *
from matplotlib.animation import FuncAnimation
from collections import deque
from os import (path, getcwd)
from matplotlib import pyplot as plt


# Function to initialise the USB-TC device

def init_dev(nchan,tc_types):
    interface = InterfaceType.USB
    tscale = TempScale.CELSIUS
    daq_list = get_daq_device_inventory (interface)
    ndev = len(daq_list)
    input_mode = AiInputMode.SINGLE_ENDED
    tc_dev = None
    ps_dev = None

    # Listing devices and finding USB-TC
    
    if ndev == 0:
        print ('** No devices connected : terminating **')
        exit()
    else:
        str = '\nThe following USB devices are conected :-\n\n'
        for daq in daq_list:
            str += '%s' % (daq.product_name)
            str += '\t (%s)\n' % (daq.unique_id)
            if daq.product_name == 'USB-TC':
                tc_dev = DaqDevice (daq)
            elif daq.product_name == 'USB-201':
                ps_dev = DaqDevice (daq)
        print (str)
        if tc_dev == None:
            print ('\n**USB-TC failed to connect**\n')
            exit(0)
        if ps_dev == None:
            print ('\n**USB-201 failed to connect**\n')
            exit(0)
            
        # Connect TC device and get current info / configuration

        at_dev = tc_dev.get_ai_device()
        at_inf = at_dev.get_info()
        tc_dev.connect()
        at_cnf = at_dev.get_config()
        for c in range (nchan) :
            at_cnf.set_chan_tc_type (c,tc_types[c])
            tc_typ = at_cnf.get_chan_tc_type(c)
            print ('Channel %d is of TC type : %s' % (c,tc_typ.name))

        # Connect pressure sensor DAQ

        ap_dev = ps_dev.get_ai_device()
        ap_inf = ap_dev.get_info()
        ps_dev.connect()
        ap_cnf = ap_dev.get_config()
        ap_rng = ap_inf.get_ranges(input_mode)[0]
            
        ans = raw_input ('\nPress RETURN to continue and Ctrl-C to stop\n')
    return tc_dev, at_dev, ps_dev, ap_dev, ap_rng

def dev_scan(at_dev,ntcs,tscale,ap_dev,ap_rng,npss):
    data = []
    input_mode = AiInputMode.SINGLE_ENDED
    for c in range (ntcs):
        try:
            temp = at_dev.t_in(c,tscale)
        except ULException as ul_error:
            if ul_error.error_code == ULError.OPEN_CONNECTION:
                temp = 20.0
            else:
                raise ul_error
        data.append (temp)
    for c in range (npss):
        try:
            pres = ap_dev.a_in(c, input_mode, ap_rng, AInFlag.DEFAULT)
            pres = (pres - poffs[c]) * pfacs[c] + padds[c]
        except ULException as ul_error:
            raise ul_error
        data.append (pres)
    return data

def time_step (target,tzero,tint):
    delt = target - time() + tzero
    if delt < 0:
        print ("\n** Time is greater than target time **\n")
        exit(0)
    target += tint
    return delt, target


#########################################

# DP calibration for box 4

patmo = input('Enter atmospheric pressure (bar): ')
if (patmo < 0.85) or (patmo > 1.15):
    print ('Unlikely mate!')
    exit(0)

poffs = [2.0000, 1.880, 1.880]
pfacs = [0.0500, 3.989, 3.989]
padds = [0.0000, patmo, patmo]

p_off = 2.0150
p_gan = 0.1024

# Select file name for logging and write time

runno = 1
fstem = strftime("HP_%b%d_",localtime())
fname = fstem + "%02d" % runno
wkdir = getcwd()
while path.isfile(fname):
    runno += 1
    fname = fstem + "%02d" % runno
ofile = open(fname,'w')
tstmp = '# Run number %02d on %s\n' % (runno,ctime())
ofile.write (tstmp)

# Initialise the USB-TC device and set the thermocouple types

ntcs = 8
npss = 3
ndat = npss + ntcs
tscale = TempScale.CELSIUS
tc_types = [2, 2, 2, 2, 2, 2, 2, 2] # All K Type
tc_dev, at_dev, ps_dev, ap_dev, ap_rng = init_dev(ntcs,tc_types)

# Set the zero time and initialise time, temperature and
# pressure lists for plotting

maxfr = 600
tint = 30.0
YDAT = [] # List of thermcouple temperatures and pressure for plottig
tim  = deque(maxlen=maxfr)
for n in range (ndat):
    YDAT.append(deque(maxlen=maxfr))

# Initialise the plotting figure and axes

fig, axs = plt.subplots(2,2,figsize=(12,10))

axTA = axs[0,0]
axT1 = axs[0,1]
axDP = axs[1,0]
axP1 = axs[1,1]
                 
tcs = ( { 'ax': axTA, 'col': 'y', 'lab': 'TA', 'fmt': '%5.1f' },
        { 'ax': axTA, 'col': 'r', 'lab': 'TB', 'fmt': '%5.1f' },
        { 'ax': axTA, 'col': 'g', 'lab': 'TC', 'fmt': '%5.1f' },
        { 'ax': axTA, 'col': 'b', 'lab': 'TD', 'fmt': '%5.1f' },
        { 'ax': axT1, 'col': 'g', 'lab': 'T1', 'fmt': '%5.1f' },
        { 'ax': axT1, 'col': 'r', 'lab': 'T2', 'fmt': '%5.1f' },
        { 'ax': axT1, 'col': 'y', 'lab': 'T3', 'fmt': '%5.1f' },
        { 'ax': axT1, 'col': 'b', 'lab': 'T4', 'fmt': '%5.1f' },
        { 'ax': axDP, 'col': 'y', 'lab': 'DP', 'fmt': '%6.3f' },
        { 'ax': axP1, 'col': 'r', 'lab': 'P2', 'fmt': '%6.3f' },
        { 'ax': axP1, 'col': 'b', 'lab': 'P1', 'fmt': '%6.3f' },        
        )

plots = map(lambda tc: tc['ax'].plot ([], [], tc['col'], lw=2, label = tc['lab']), tcs)
lines = map(lambda x: x[0], plots)

# Write header to log file

fhead = '# time'
for tc in tcs:
    fhead += '\t'+tc['lab']
fhead += '\n'
ofile.write (fhead)

def plt_init():
    
    axi = ( {'ax':axTA, 'y1':10, 'y2':60, 'tit':'External Temperatures', 'ylab':'Temperature (C)'},
            {'ax':axT1, 'y1':10, 'y2':60, 'tit':'R134a Temperatures', 'ylab':'Temperature (C)'},
            {'ax':axDP, 'y1':-0.05, 'y2':0.25, 'tit':'Flow pressure diff.', 'ylab':'Pressure (bar)'},
            {'ax':axP1, 'y1':-0.1, 'y2':20., 'tit':'R134a Pressures', 'ylab':'Pressure (bar)'} )
    
    for a in axi:
        a['ax'].set_xlim(0,300.0)
        a['ax'].set_ylim(a['y1'],a['y2'])
        a['ax'].set_xlabel('Time (s)')
        a['ax'].set_ylabel(a['ylab'])
        a['ax'].set_title(a['tit'])
        a['ax'].legend(loc='lower left')
        a['ax'].grid()                        
    return

def update (frame):

    # Axis information

    axi = ( {'ax': axTA, 'n1': 0, 'n2': 4, 'yint': 5.0},
            {'ax': axT1, 'n1': 4, 'n2': 8, 'yint': 5.0},
            {'ax': axDP, 'n1': 8, 'n2': 9, 'yint': 0.1},
            {'ax': axP1, 'n1': 9, 'n2': 11, 'yint': 1.0})

    # Scan the temperatures and store in temps[]
    
    try:
        tim.append(time() - tim0)
        data = dev_scan (at_dev,ntcs,tscale,ap_dev,ap_rng,npss)

    except Exception as e:
        print (e)
        exit(0)

    # Display temperatures on the screen and output to logging file

    flout = '%7.1f' % tim[-1]
    scout = 't=%.1f : ' % (tim[-1])
    for n in range (len(tcs)):
        scout += tcs[n]['lab'] + '=' + tcs[n]['fmt'] % data[n]
        flout += '\t' + tcs[n]['fmt'] % data[n]
    print (scout)
    flout += '\n'
    ofile.write (flout)

    # Append the temperatures to the 'deque' lists TCS and update the plots

    for n in range (len(tcs)):
        YDAT[n].append(data[n])
        lines[n].set_data(tim,YDAT[n])
    
    # Update the time axis range if necessary

    for a in axi:
        tmin, tmax = a['ax'].get_xlim()
        if tim[-1] > tmax:
            if frame > maxfr:
                a['ax'].set_xlim(tmin+tint,tmax+tint)
            else:
                a['ax'].set_xlim(tmin,tmax+tint)                    
        ymin, ymax = a['ax'].get_ylim()
        dmin = min (data[a['n1']:a['n2']])
        dmax = max (data[a['n1']:a['n2']])
        if dmin < ymin:
            ymin -= a['yint']
        if dmax > ymax:
            ymax += a['yint']
        a['ax'].set_ylim (ymin, ymax)
    
    return

plt_init()
tim0 = time()
ani  = FuncAnimation(fig, update, interval=50)
try:
    plt.show()
except:
    pass

if tc_dev.is_connected():
    descrip = tc_dev.get_descriptor()
    print ("\nDiconnecting %s\n" % (descrip.dev_string))
    tc_dev.disconnect()
if ps_dev.is_connected():
    descrip = ps_dev.get_descriptor()
    print ("\nDiconnecting %s\n" % (descrip.dev_string))
    ps_dev.disconnect()
print ('Data has been logged in : %s\n' %(fname))
ofile.close()
print ("HP terminated normally\n")

