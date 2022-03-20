import sys
import math
from omg import *
from omg.mapedit import *
from tkinter import messagebox
from tkinter import Tk
from tkinter.simpledialog import askinteger
from tkinter.simpledialog import askstring


def make_sure(condition, msg):
    if not condition:
        messagebox.showerror(sys.argv[0], msg)
        sys.exit(1)

using_tk = False

if len(sys.argv) == 4:
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    prefix = sys.argv[3]
    assert width >= 8
    assert height <= 128
else:
    Tk().withdraw()
    using_tk = True
    width = askinteger(title="Width", prompt="What is the WIDTH of your display?")
    height = askinteger(title="Height", prompt="What is the HEIGHT of your display?") 
    prefix = askstring(title="Prefix", prompt="What is the PREFIX of your display textures?\nEx: ANIM0, ANIM1, ... -- you enter: ANIM\nEx: TEX_0, TEX_1, ... -- you enter: TEX_")

make_sure(width and width >= 8, "Minimum width is 8.")
make_sure(height and height <= 128, "Maximum height is 1024.")

m = MapEditor()

MIDTEX = "STONE2"
EXTEX = "SHAWN2"
LUTEX = "SUPPORT2"

s = Sidedef()
s.tx_mid = MIDTEX

# draw a big open sector
m.draw_sector(vertexes=[(1024,1024), (-1024,1024), (-1024,-1024), (1024,-1024)], sidedef=s)

# Add a player 1 start so the map can be tested if desired
p1 = Thing()
p1.type = 1
p1.x = -64
p1.y = -64

m.things.append(p1)

s = Sidedef()
s.tx_low = LUTEX
s.tx_up = LUTEX

m.draw_sector(vertexes=[(width+8,40), (-8,40), (-8,-8), (width+8,-8)], sidedef=s)

m.sectors[-1].z_ceil = int(128 - (128 - height)/2)
m.sectors[-1].z_floor = int((128 - height)/2)


v = [(width//2,32)]
# draw a sector in the middle with the display dimensions
for px in range(width,-1,-1):
    v.append((px,0))

s = Sidedef()
s.tx_mid = prefix

m.draw_sector(vertexes=v, sidedef=s)

tidx = 0
offset = 0
offset_needed = bool((128 // height) > 1)

first = True
tnext = not offset_needed
for sd in reversed(m.sidedefs):
    sd.sector = len(m.sectors)-1
    if sd.tx_mid == prefix:
        if first:
            first = False
            sd.tx_mid = EXTEX
        # FIXME: ideally should handle fractional offsets here,
        # so some textures will be wrong. known bug here.
        elif tidx == math.ceil(width / math.floor(128 / height)):
            sd.tx_mid = EXTEX
        else:
            sd.tx_mid += str(tidx)
            sd.off_y = offset
            if offset_needed:
                offset += height
                if offset + height > 128:
                    offset = 0
                    tnext = True
                else:
                    tnext = False
            if tnext:
                tidx += 1

for lc in m.linedefs:
    sf = m.sidedefs[lc.front]
    if sf.tx_mid.startswith(prefix):
        lc.action = 48
        sf.sector = 1
    elif sf.tx_mid == EXTEX:
        sf.sector = 1
    elif sf.tx_up == LUTEX:
        nsd = Sidedef()
        nsd.sector = 0
        sf.sector = 1
        nsd.tx_up = LUTEX
        nsd.tx_low = LUTEX
        m.sidedefs.append(nsd)
        lc.back = len(m.sidedefs)-1
        lc.two_sided = True
    elif sf.tx_mid == MIDTEX:
        sf.sector = 0

w = WAD()
w.maps["MAP01"] = m.to_lumps()
w.to_file("template.wad")
if using_tk:
    messagebox.showinfo(title="Done!",message="Generated template.wad with your display.\nIt does NOT have nodes built!")
else:
    print("Generated template.wad with your display.\nIt does NOT have nodes built!")
