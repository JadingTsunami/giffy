# giffy

Create vanilla-compatible animated displays from an animated GIF.



# Warnings

**Creating vanilla-compatible animated displays is effort intensive.**

Make sure you actually want to do this as it will require some investment of time on your part.

The **WIDTH** of your display will be the most troublesome part. Narrow displays (&le;32px) will be the easiest to work with, but you can create any size within the limits.

# Pre-requisites

* Python3
* Tkinter
* Pillow

# Instructions

1. Choose an animated GIF.
    * No more than 1024 frames.
    * No more than 128px height and width per frame.
    * Only animations with power-of-2 frames will loop smoothly.
2. Run the program, select your animated GIF.
3. Import each generated PNG as a Texture in your WAD and follow the instructions you were given at the output prompt.

