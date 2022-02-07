#!/usr/bin/env python

# kfSpeed Version 0.2

import binascii
import wave
import struct
from sys import argv, stderr
import os.path


def die(msg):
    if isinstance(msg, BaseException):
        msg = str(msg)
    stderr.write(str(msg) + '\n')
    exit(1)

def open_wav(wav):
    # read the pcm
    try:
        with wave.open(wav, 'rb') as wr:
            return wr.readframes(wr.getnframes()), wr.getframerate()
    except:
        die(".wav file not found.")

def open_kftm(kftm):
    # read the pcm
    try:
        return open(kftm, "ab")
    except:
        die(".kftm file not found.")


def get_usage(self_py):
    return 'Usage: {} music.wav\n\nOptional parameters:\nexisting.KFTM (to add data to an existing .KFTM)\ntwochannel (to add a second channel of PCM data (not implemented))\n\nmain.py music.wav existing.KFTM twochannel'.format(self_py)


# necessary funtion to convert the double values into hex format
def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])


def reverse_hex_array(hex_value):
    hexArray = [hex_value[i:i + 2] for i in range(0, len(hex_value), 2)]
    return hexArray[8] + hexArray[7] + hexArray[6] + hexArray[5] + hexArray[4] + hexArray[3] + hexArray[2] + hexArray[1]


def generate_KFTM():
    output_file = open("output.KFTM", "wb")
    output_string = "6B66746D0100"  # KFTM header
    output_string += "0"*128  # Title
    output_string += "0"*128  # Composer
    output_string += "0"*128  # Description
    output_string += "FFFF"  # Total amount of rows
    # Content of the first 4 rows (this is stupidly long and could be shortend, but I am lazy rn)
    output_string += "01000000000000408F40000000000000F0BF000000000000F03F000000000000F0BF0000000000E07540000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000F0BF000000000000F03F000000000000F0BF000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"

    output_file.write(binascii.unhexlify(output_string))
    output_file.close()




MUSIC = None
KFRAW = None
TWOCHANNEL = False

if len(argv) == 1:
    die(get_usage(argv[0]))

for arg in argv:
    if arg.endswith('.wav'):
        if MUSIC is None:
            MUSIC = arg
        else:
            die(get_usage(argv[0]))
    if arg.lower().endswith('.kftm'):
        if KFRAW is None:
            KFRAW = arg
        else:
            die(get_usage(argv[0]))
    if arg == 'twochannel':
        die("Twochannel mode is not implemented yet.")


if MUSIC is None:
    die(get_usage(argv[0]))


MUSIC, framerate = open_wav(MUSIC)
print(".wav file opened. Frequency: {}Hz - Speed used for kf-emulation: s{}".format(str(framerate), str(framerate/8)))

if KFRAW is None:
    generate_KFTM()
    KFRAW = open_kftm("output.KFTM")
    print("generated a new kftm file \"output.kftm\"")
else:
    if os.path.isfile(KFRAW):
        print("appending to {}".format(KFRAW))
        KFRAW = open_kftm(KFRAW)
    else:
        die("{} is not an existing file.".format(KFRAW))




# this part is only needed if you wanna write a 2nd part into your file on a different channel.
# more setup is required for this
# work in progress(?)
# uncomment this if you know what you're doing
# with wave.open('music2.wav', 'rb') as wr:
#     frames2 = wr.readframes(wr.getnframes())

# setting the beginning of the first row (the speed is wav-hz/8) and the end of the row (bunch of empty columns)
rowStart = "0100" + reverse_hex_array((double_to_hex((framerate/8))).ljust(18, "0"))
rowEnd = "0" * 240

# alternative version for two channels
# rowStart = "0" * 20 #20
# rowEnd = "0" * 48 #240
# rowEnd2 = "0" * 176 #240


# for debugging reasons, this is tracked.
# You need to change the division later on according to the peaks here.
lowest = 2000
highest = 0


print("writing pcm into .kftm")

# main loop to write all info into the .KFTM file
for offset in range(0, len(MUSIC), 2):
    # change the offset depending on how many frames you wanna skip in the song
    # this changes the quality (and saves file size)
    if offset%32 == 0:
        data_new = (struct.unpack_from('<h', MUSIC, offset)[0])

        # depending on where you start your PCM, these values need to be changed.
        # currently uncommented line is for the example raw KFTM.
        x = int((data_new + 31540)/415) #415

        # this one got used by me for my ac21 entry. can be ignored.
        #x = int(((data_new + 31540)/21)) #415
        doubleHex = (double_to_hex(x)).ljust(18, "0")
        rowMiddle = reverse_hex_array(doubleHex)

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
        KFRAW.write(binascii.unhexlify(row))
        lowest = min(lowest, x)
        highest = max(highest, x)
        # important to set this to 0 now, so the speed command is not written into every new row
        # (even tho it wldnt hurt to do this, it looks cleaner if we skip it)
        rowStart = "0" * 20  # 20

KFRAW.close()
print("sucessfully written pcm into .kftm")
print("Lowest Value: " + str(lowest))
print("Highest Value: " + str(highest))
