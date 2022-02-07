# kfSpeed

This is a very simple tool to convert raw pcm data into [klangfreude](https://kleeder.de/files/botb/klangfreude/klangfreude_20210508.zip).
It works by DC-offsetting silence.
Adjusting and setting up your .KFTM is needed for this to work, unless you wanna generate one from scratch.
Since klangfreude behaves differently depending on where you wanna start the PCM,
brute-forcing the correct values is needed. I cannot help you with this.
-------
## Setup

Make sure you have the following files in your directory:
- mandatory
  - music.wav (all kHz work, but keep the file size limit in mind)
- optional
  - kfSpeedRaw.KFTM 

Now just run the script by using
  ```bash
   python main.py music.wav
  ```
If you don't specify a .kftm, it will just generate a new output.KFTM.
If you specify a .kftm by running the following:
  ```bash
   python main.py music.wav file.kftm
  ```
it will append to an already existing .kftm file.

Possible improvements to be made:
- specify wether you want 1-channel or 2-channel-PCM
-------
## Version history

* 0.2: more settings and auto-generating the whole kftm if nothing else is specified
* 0.1: alpha-version. Partially working tool, yay!
-------