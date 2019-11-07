#!/bin/bash
snr=0.001
tracenum=1000
bootnum=2000
fixvalue=5
#python yuan_sim_signal.py $tracenum $snr $fixvalue 
#python yuan_sim_signal_fix.py $tracenum $snr $fixvalue
python yuan_sim_signal_fix2.py $tracenum $snr $fixvalue
#python boot.py $bootnum $snr $fixvalue $tracenum
#python boot2.py $bootnum $snr $fixvalue $tracenum
#python boot3.py $bootnum $snr $fixvalue $tracenum
python boot2_gtest.py $bootnum $snr $fixvalue $tracenum