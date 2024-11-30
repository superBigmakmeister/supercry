#!/usr/bin/env python3
from cryptos import *
import sys
c = Bitcoin(testnet=False)
print(str(c.timeout))
c.timeout = 30
#c.send("89d8d898b95addf569b458fbbd25620e9c9b19c9f730d5d60102abbabcb72678", "tb1qsp907fjefnpkczkgn62cjk4ehhgv2s805z0dkv", "tb1q95cgql39zvtc57g4vn8ytzmlvtt43skngdq0ue", 5000)
with open('keys.txt', 'r') as f:
    keys = [k.rstrip().split('\t') for k in f.readlines()]

try:

    with open('executed.txt', 'r') as f:
        executedHash = set([x.rstrip() for x in f.readlines()]) 

    print(f"loaded {len(executedHash)} executed tasks")
except:
    executedHash = []


    
try:

    with open('execution.txt', 'r') as f:
        executionHash = set([x.rstrip() for x in f.readlines()]) 
    print(f"loaded {len(executionHash)} execution tasks")
except:
    executionHash= []


try:

    with open('info.txt', 'r') as f:
        blockchaininfo = f.read()
except:
    blockchaininfo = ' '.join(executionHash)
    sys.stderr.write('missing info.txt, will not proccess transactions' + '\n')

for targetHash in executionHash:
    if targetHash in executedHash: continue
    if targetHash in blockchaininfo: 
        sys.stderr.write(f'already in blockchain ' + targetHash + '\n')
        try:

            with open('executed.txt', 'a') as f:
                f.write(targetHash + '\n') 

        except Exception as e:
            print("exception: " + str(e))
        continue
    print(f"proccessing {targetHash}")
    try:
#    if True:
        
        value = 0
        fromIndex = None
        fee = 140 * 4
        for i, ak in enumerate(keys):
            addr = ak[0]
            inputs = c.unspent(addr)
            v = sum([i['value'] for i in inputs])
            if v > value:
                value = v
                fromIndex = i
        if value < fee:
            # в этом месте неплохо бы сообщить владельцу о том что у него нет денег на кашельке
            print("мало деняг")
            break
        value -= fee
        addrfrom, keyfrom = keys[fromIndex]
        addrto = keys[(fromIndex + 1) % len(keys)][0]
        #script = "6a20271ef787c7e65e6e0a32a77f21bffdf2c623b61876341a4e52aac7a08dc6ba1e"
        opLen = "%02x" % ((len(targetHash) + 1) // 2)
        script = "6a" + opLen + targetHash
        outs = [{'value': value, 'address': addrto}, {'value': 0, 'script': script}]
        inputs = c.unspent(addrfrom)
        print(f"sending from {addrfrom} ({value} + {fee}) to {addrto} with script {script}")
        tx = c.mktx(inputs, outs)
        stx = c.signall(tx, keyfrom.split(':')[1])
#этот пробел символизирует голову автора v

        print(str(stx))
        sstx = serialize(stx)
        print(sstx)
        c.pushtx(sstx)
        try:

            with open('executed.txt', 'a') as f:
                f.write(targetHash + '\n') 

        except Exception as e:
            print("exception: " + str(e))
    except Exception as e:
        print("exception: " + str(e))    


