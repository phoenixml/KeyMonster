#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import subprocess


__author__ = "Touhid M.Shaikh"
__description__ = """Dump KeyStroke From Pcap file"""

def keys():
    keys = {}
    keys.update({
        i + 0x4: chr(i + ord('a'))
        for i in range(26)
    })
    keys.update({
        i + 0x1e: chr(i + ord('1'))
        for i in range(9)
    })
    keys[0x27] = '0'
    keys.update({
        0x28: '\n',
        0x2c: ' ',
        0x2d: '-',
        0x2e: '=',
        0x2f: '[',
        0x30: ']',
        0x37: '.',
        0x34: '\''
    })
    return keys

def skeys():
    keys = {}
    keys.update({
            i + 0x4: chr(i + ord('A'))
            for i in range(26)
            })

    shiftwithnum = ['!','@','#','$','%','^','&','*','(',')']

    keys.update({
            i + 0x1e: chr(ord(shiftwithnum[i]))
            for i in range(9)
            })
    keys[0x27] = '0'
    keys.update({
        0x28: '\n',
        0x2c: ' ',
        0x2d: '_',
        0x2e: '+',
        0x2f: '{',
        0x30: '}',
        0x37: '>',
        0x34: '\"'
    })
    return keys

def arrow():
    keys = {}
    keys.update({
        0x4f: 'RIGHT',
        0x50: 'LEFT'

    })
    return keys

keys = keys()
skeys = skeys()
arrow = arrow()

file = sys.argv[1]
cmd = "tshark -r "+file+" -T fields -e usb.capdata -Y usb.capdata 2>/dev/null | tail -n +6 "
out = subprocess.check_output(cmd,shell=True)

lis = out.splitlines()

nums = []
shift = []
for key in lis:
    s = key[3:5]
    a = key[6:8]
    nums.append(int(a,16))
    shift.append(int(s,16))

output = []
pos = 0

for n in range(0,len(nums)):

    if nums[n] == 80:
        pos = pos -1


    if nums[n] == 79:
        pos = pos +1


    if shift[n] == 0:
        c = nums[n]
        if c in keys:
            output.insert(pos,str(keys[c]))
            pos = pos +1


    if shift[n] == 32:
        c = nums[n]
        if c in skeys:
            output.insert(pos, str(skeys[c]))
            pos = pos + 1

print "Total msg lenth : ",len(output)
final = ""
for i in output:
    final += i

print final
