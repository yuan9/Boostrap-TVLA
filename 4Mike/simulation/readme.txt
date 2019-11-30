1. tp_smallT_DataGenerator.py is used for generating two Fix vs Random data. It will generate two set of data and write them into .txt
with the information of t-statitics, SNR

Note that I have already generate two sets of data for our Boostrapping experiment. 
9--5.22999896061RandNoise_1000traces_1SNR_f5.txt  and  9--5.22999896061FixNoise_1000traces_1SNR_f5.txt are the files for the experiment

2.  TVLA-evolution.py is used to generating the p-value evolution for t-test

3.  Bootstrap-1sample.py is used for the Boostrapping method two those two set of data. The result is in the folder fn_evolution_test/
4.  plot2.py in the folder fn_evolution_test/ is used to plotting the Boostrap evolution result