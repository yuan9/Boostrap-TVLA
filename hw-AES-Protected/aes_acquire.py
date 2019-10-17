
import os

import Dpaws
import DpawsUtils

try:
#    scope = Dpaws.Scope('ivi:WR610Zi')
    scope = Dpaws.Scope('lan:10.84.160.226')
    ser = Dpaws.DPASLDevice('COM6', 57600)

    scope.SetMode('stream', 'ch3', False)
#    scope.SetMode('run')
except:
    print("scope/serial port setup failed")
else:
    no_acqs = 100000

    tv_gen =  DpawsUtils.Generators.SelectGenerator('fvr', DpawsUtils.AES_TV( 128 ))
    seedgen = DpawsUtils.Generators.RandomDataGenerator(8);

    rw = Dpaws.DatasetWriter( 'log.dwdb' , './data/000/t000.dwfm', '.' );

    ser.Transact('ai')
    ser.Transact('akfedcba98765432100123456789abcdef')

    i=0
    while (i < no_acqs):
        tv = tv_gen.generate(1)
        print i,':',tv[ 'Data' ].encode( 'hex' ),tv[ 'Sel' ]

        seed = seedgen.generate(1); # "{0:08x}".format(int(seed['Data'].encode('hex'),8))

        ser.Transact("s1"+seed[ 'Data' ].encode('hex'))
        ser.Transact("am"+tv[ 'Data' ].encode('hex'))

        try:
            r = rw.NewRecord()
            ser.Transact("ae")
            scope.WaitTillAcquired()
            scope.StoreTrace(r, 'ch3' )
        except:
            print('Acquisition failed\n')
        else:
            r.SetMeta('{}', tv[ 'Sel' ])
            rw.SubmitRecord(r)

            i+=1

    ser.Transact("ad");
    
    rw.Close()
    ser.Close();
    scope.Close()
