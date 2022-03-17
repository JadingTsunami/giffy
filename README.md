# giffy

Create vanilla-compatible animated displays from an animated GIF.

![](web/tpn.gif)

Originally seen in [TRUCK.WAD](https://www.doomworld.com/idgames/levels/doom2/deathmatch/s-u/truck).

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

# Tips

Try [ImageMagick](https://imagemagick.org/index.php) for resizing animated GIFs.

Example:

Resize to 32x32 but keep aspect ratio intact:

```
mogrify -resize '32x32' mygif.gif
```

Or to force the size to be 32x32:

```
mogrify -resize '32x32!' mygif.gif
```

Try [ffmpeg](https://ffmpeg.org/) for converting video to animated GIF format.

Example:

```
ffmpeg -i my_video.mp4 my_video.gif
```

Or for reduced size:

```
ffmpeg -i my_video.mp4 -vf 'fps=fps=35,scale=200:-1' my_video.gif
```

