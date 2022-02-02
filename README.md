# kfSpeed

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

## Version history

* 0.1: alpha-version. Partially working tool, yay!
