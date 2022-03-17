# giffy: Create vanilla-compatible animated displays from an animated GIF.
# Copyright (C) 2022 JadingTsunami
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
from PIL import Image
from PIL import GifImagePlugin
import math
import sys
from tkinter import messagebox

def make_sure(condition, msg):
    if not condition:
        messagebox.showerror(sys.argv[0], msg)
        sys.exit(1)

def warn(condition, msg):
    if not condition:
        messagebox.showwarning(sys.argv[0], msg)

imgfile = ""
if len(sys.argv) > 1:
    imgfile = sys.argv[1]
else:
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    Tk().withdraw()
    imgfile = askopenfilename(filetypes=[("Animated GIF","*.gif")],multiple=False)

make_sure(imgfile, "Must choose an animated GIF.")

imageObject = Image.open(imgfile)

make_sure(imageObject.is_animated, "GIF isn't animated.")
make_sure(imageObject.n_frames, "GIF doesn't have any animation frames.")


width, height = imageObject.size
nframes = (imageObject.n_frames)

make_sure(width <= 128, "Only video widths up to 128 are supported. If you need more let me know and I might add it.")

if 128 // width > 1:
    nimg = int(math.ceil(width/(128/width)))
else:
    nimg = width

outimg = []
outpix = []

imglimit = max(8,2**(nframes-1).bit_length())

make_sure(imglimit <= 1024, "Only up to 1024 frames is supported. If you need more let me know, I might add it.")
warn(imglimit % 8 != 0, "Warning: The number of frames in your GIF is not a power of 2. That means your animation won't loop smoothly, or will have blank space at the end. If you don't care, you can ignore this.")

for img in range(nimg):
    outimg.append(Image.new('RGBA', (imglimit,128)))
    outpix.append(outimg[-1].load())

# split each frame into a single row of pixels
for r in range(width):
    for frame in range(0,imglimit):
        imageObject.seek(frame % nframes)
        pf = imageObject.convert('RGBA').load()
        for y in range(height):
            outpix[r*width//128][frame,y + (r*width%128)] = pf[r,y]

for i,img in enumerate(outimg):
    img.save("anim%d.png" % i, "PNG")

instructions = """Success!
Created the following files:
"""
instructions += "anim%d .. %d.png\n" % (0, nimg-1)
instructions += "\n"
instructions += "Each has dimensions %dx%d\n" % (imglimit, 128)
instructions += "Each contains %d 1px slices of decomposed video.\n" % (math.floor(128/width))
instructions += "\n"
instructions += "To create your display, create %d 1px lines and give them special 48 (scrolling wall).\n" % (width)
instructions += "Start the lines with the 0th texture that was generated.\n"
if 128 // width > 1:
    instructions += "Increase the y-offset on each line by %d until the offset is >= 128, then use the next texture and reset the y-offset to 0." % (width)
else:
    instructions += "Use the next texture in the sequence for each subsequent line."

messagebox.showinfo("Success!", instructions)
