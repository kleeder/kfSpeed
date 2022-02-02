#!/usr/bin/env python

"""
kfSpeed, version 0.1
----------------------

This is a very simple tool to convert raw pcm data into klangfreude.
It works by DC-offsetting silence.
Adjusting and setting up your .KFTM is needed for this to work.
Since klangfreude behaves differently depending on where you wanna start the PCM,
brute-forcing the correct values is needed. I cannot help you with this.

Make sure you have the following files in your directory:
- music.wav (all kHz work, but keep the file size limit in mind)
- kfSpeedRaw.KFTM (included with the tool; only works if you want PCM directly at the start)


There are ideas for 2-channel-PCM, which is WIP and uncommented for now.
Other improvements to be made:
- generating the whole .KFTM aka not requiring a raw-file,
  unless you specify it.
- specify wether you want 1-channel or 2-channel-PCM

Version history
---------------

* 0.1: alpha-version. Partially working tool, yay!

"""

import binascii
import wave
import struct


# necessary funtion to convert the double values into hex format
def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])


# read the pcm
with wave.open('music.wav', 'rb') as wr:
    frames = wr.readframes(wr.getnframes())

# this part is only needed if you wanna write a 2nd part into your file on a different channel.
# more setup is required for this
# work in progress(?)
# uncomment this if you know what you're doing
# with wave.open('music2.wav', 'rb') as wr:
#     frames2 = wr.readframes(wr.getnframes())

# setting the beginning and end of the rows, as hex (all 00)
rowStart = "0" * 20 #20
rowEnd = "0" * 240

# alternative version for two channels
# rowStart = "0" * 20 #20
# rowEnd = "0" * 48 #240
# rowEnd2 = "0" * 176 #240

# The raw KFTM
kfraw = open("kfSpeedRaw.KFTM", "ab")

# for debugging reasons, this is tracked.
# You need to change the division later on according to the peaks here.
lowest = 2000
highest = 0

# main loop to write all info into the .KFTM file
for offset in range(0, len(frames), 2):
    # change the offset depending on how many frames you wanna skip in the song
    # this changes the quality (and saves file size)
    if offset%32 == 0:
        data_new = (struct.unpack_from('<h', frames, offset)[0])

        # depending on where you start your PCM, these values need to be changed.
        # currently uncommented line is for the example raw KFTM.
        x = int((data_new + 31540)/415) #415

        # this one got used by me for my ac21 entry. can be ignored.
        #x = int(((data_new + 31540)/21)) #415
        doubleHex = (double_to_hex(x)).ljust(18, "0")
        hexArray = [doubleHex[i:i + 2] for i in range(0, len(doubleHex), 2)]
        rowMiddle = hexArray[8]+hexArray[7]+hexArray[6]+hexArray[5]+hexArray[4]+hexArray[3]+hexArray[2]+hexArray[1]

        # this stuff is only needed for 2-channel PCM
        # try:
        #     data_new2 = (struct.unpack_from('<h', frames2, offset)[0])
        #     x2 = int((data_new2 + 31540) / 415)  # 415
        #     doubleHex2 = (double_to_hex(x2)).ljust(18, "0")
        #     hexArray2 = [doubleHex2[i:i + 2] for i in range(0, len(doubleHex2), 2)]
        #     rowMiddle2 = hexArray2[8] + hexArray2[7] + hexArray2[6] + hexArray2[5] + hexArray2[4] + hexArray2[3] + hexArray2[2] + hexArray2[1]
        # except:
        #     rowMiddle2 = "0" * 16
        # row = rowStart + rowMiddle + rowEnd + rowMiddle2 + rowEnd2

        row = rowStart + rowMiddle + rowEnd
        kfraw.write(binascii.unhexlify(row))
        lowest = min(lowest, x)
        highest = max(highest, x)

kfraw.close()
print(lowest)
print(highest)
