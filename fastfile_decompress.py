#!/bin/python
import zlib
import sys
print("you've got the power to be his friend!")
if(len(sys.argv) != 3):
    print("fastfile_decompress.py:\nUsage ./fastfile_decompress.py [mc.art] [outputdir]")
    quit()

outdir = sys.argv[2] + "/"
f = open(sys.argv[1], 'rb')
items = []
nbytes = (int.from_bytes(f.read(4), byteorder='little'))
i  = 0
while i < nbytes:
    addr = (int.from_bytes(f.read(4), byteorder='little'))
    name = f.read(16).decode('ascii').rstrip('\x00')
    items.append({
        "addr": addr,
        "name": name
        })
    i  += 1
i = 0
for file in items:
    if(items.index(file) == len(items)-1):
        break
    try:
        length = items[i+1]["addr"]-file["addr"]
        f.seek(file["addr"])
        out = open(outdir+file["name"], 'wb')
        out.write(zlib.decompress(f.read(length)))
        out.close() # no memory leak here
        print("Decompressed file: "+ file["name"])
    except:
        print("Failed parsing file: " + file["name"])
    i += 1
f.close()
