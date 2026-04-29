#!/bin/python
import zlib
import sys
from os import listdir
from os.path import isfile, join, getsize
print("you've got the power to be his friend!")
if(len(sys.argv) != 3):
    print("fastfile_compress.py:\nUsage ./fastfile_decompress.py [inputdir] [outfile]")
    quit()

outdir = sys.argv[1] + "/"
importfiles = [f for f in listdir(outdir) if isfile(join(outdir, f))]
compressedfiles = []
print(importfiles)
out = open(sys.argv[2], 'wb')
entries = (len(importfiles)+1)
entrylength = 20 # this is 20 bytes long, since 4 bytes for the addr, then 16 bytes for the name
offset = 4 # 4 byte offset for tha headah
print("writing "+str(entries)+" files to archive...")
out.write(entries.to_bytes(4,'little'))
table_length = (entries*entrylength+offset) #length of the naming entries table
current_offset = 0
for file in importfiles:
    f = open(outdir+file, 'rb')
    uncompressed = f.read()
    f.close()
    compressed = zlib.compress(uncompressed)
    compressedfiles.append(compressed)
    length = len(compressed)
    out.write((table_length+current_offset).to_bytes(4,'little'))
    out.write(file.ljust(16,'\x00').encode('ascii'))
    current_offset += length

#we've also got to write a dummy entry, so lets do it now before things get too heated...'
out.write((table_length+current_offset).to_bytes(4,'little'))
out.write("".ljust(16,'\x00').encode('ascii'))
for comp in compressedfiles:
    out.write(comp) # that was really easy?
out.close()
# items = []
# nbytes = (int.from_bytes(f.read(4), byteorder='little'))
# i  = 0
# while i < nbytes:
#     addr = (int.from_bytes(f.read(4), byteorder='little'))
#     name = f.read(16).decode('ascii').rstrip('\x00')
#     items.append({
#         "addr": addr,
#         "name": name
#         })
#     i  += 1
# i = 0
# for file in items:
#     try:
#         length = items[i+1]["addr"]-file["addr"]
#         f.seek(file["addr"])
#         out = open(outdir+file["name"], 'wb')
#         out.write(zlib.decompress(f.read(length)))
#         print(file)
#     except:
#         print("failed parsing file: " + file["name"])
#     i += 1
# f.close()
