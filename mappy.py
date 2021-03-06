# mappy: Create an animated display in a test map.
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
    assert height <= 1024
else:
    Tk().withdraw()
    using_tk = True
    width = askinteger(title="Width", prompt="What is the WIDTH of your display?")
    height = askinteger(title="Height", prompt="What is the HEIGHT of your display?") 
    prefix = askstring(title="Prefix", prompt="What is the PREFIX of your display textures?\nEx: ANIM0, ANIM1, ... -- you enter: ANIM\nEx: TEX_0, TEX_1, ... -- you enter: TEX_")

make_sure(width and width >= 8, "Minimum width is 8.")
make_sure(height and height <= 1024, "Maximum height is 1024.")

m = MapEditor()

MIDTEX = "STONE2"
EXTEX = "SHAWN2"
LUTEX = "SUPPORT2"

s = Sidedef()
s.tx_mid = MIDTEX

# draw a big open sector
m.draw_sector(vertexes=[(1536,1536), (-1536,1536), (-1536,-1536), (1536,-1536)], sidedef=s)

m.sectors[-1].z_ceil = 1056

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

m.sectors[-1].z_floor = 32
m.sectors[-1].z_ceil = 32 + height
m.sectors[-1].light = 255
m.sectors[-1].tx_floor = "FLAT23"
m.sectors[-1].tx_ceil = "FLAT23"


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
        elif tidx == math.ceil(width / max(1,math.floor(128 / height))):
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

tidx = 0
offset = 0
tnext = not offset_needed
# now draw a 2S transparent version
for x in range(width+1):
    v = Vertex()
    v.x = x
    v.y = -256
    m.vertexes.append(v)
    if x > 0:
        # draw a line between this and the previous vertex
        l = Linedef()
        l.two_sided = True
        l.lower_unpeg = True
        l.action = 48
        l.vx_a = len(m.vertexes)-2
        l.vx_b = len(m.vertexes)-1
        s1 = Sidedef()
        s2 = Sidedef()
        s1.sector = 0
        s2.sector = 0

        s1.tx_mid = prefix
        if tidx == math.ceil(width / max(1,math.floor(128 / height))):
            s1.tx_mid = EXTEX
        else:
            s1.tx_mid += str(tidx)
            s1.off_y = offset
            if offset_needed:
                offset += height
                if offset + height > 128:
                    offset = 0
                    tnext = True
                else:
                    tnext = False
            if tnext:
                tidx += 1
        m.sidedefs.append(s1)
        l.front = len(m.sidedefs)-1
        m.sidedefs.append(s2)
        l.back = len(m.sidedefs)-1
        m.linedefs.append(l)

def make_circle(origin, width, max_angle):
    # circle version
    global m
    global offset_needed
    radius = width / (max_angle)

    v = []
    o_x, o_y = origin
    tidx = 0
    offset = 0
    tnext = not offset_needed
    # positives first
    step = 1/radius
    angle = 0
    first_vert = len(m.vertexes)
    while angle <= max_angle + step:
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        angle += step
        vert_x = round(o_x + x)
        vert_y = round(o_y + y)
        vv = Vertex()
        vv.x = vert_x
        vv.y = vert_y
        m.vertexes.append(vv)
        if angle > step:
            # draw a line between this and the previous vertex
            l = Linedef()
            l.two_sided = True
            l.lower_unpeg = True
            l.action = 48
            l.vx_a = len(m.vertexes)-2
            if (2*math.pi + step) - angle < 0.00001:
                l.vx_b = first_vert
            else:
                l.vx_b = len(m.vertexes)-1
            s1 = Sidedef()
            s2 = Sidedef()
            s1.sector = 0
            s2.sector = 0

            s1.tx_mid = prefix
            if tidx == math.ceil(width / max(1,math.floor(128 / height))):
                s1.tx_mid = EXTEX
            else:
                s1.tx_mid += str(tidx)
                s1.off_y = offset
                if offset_needed:
                    offset += height
                    if offset + height > 128:
                        offset = 0
                        tnext = True
                    else:
                        tnext = False
                if tnext:
                    tidx += 1
            m.sidedefs.append(s1)
            l.front = len(m.sidedefs)-1
            m.sidedefs.append(s2)
            l.back = len(m.sidedefs)-1
            m.linedefs.append(l)

make_circle((width/2,-512), width, 2*math.pi)
make_circle((width/2,-1024), width, math.pi)

w = WAD()
w.maps["MAP01"] = m.to_lumps()
w.to_file("template.wad")
if using_tk:
    messagebox.showinfo(title="Done!",message="Generated template.wad with your display.\nIt does NOT have nodes built!")
else:
    print("Generated template.wad with your display.\nIt does NOT have nodes built!")
