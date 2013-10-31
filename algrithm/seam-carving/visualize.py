#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2010 Mathieu Blondel
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
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import sys

import gtk
from gtk import gdk

from seamcarving import *

if len(sys.argv) == 1:
    print """Show the seams that seam-carving would delete/add.

%s imgfile [n_vseams] [n_hseams]

n_vseams: number of vertical seams to show (default: 1)
n_hseams: number of horizontal seams to show (default: 1)
""" % sys.argv[0]

    exit(1)

try:
    n_vseams = int(sys.argv[2])
except:
    n_vseams = 1

try:
    n_hseams = int(sys.argv[3])
except:
    n_hseams = 1

buf = gdk.pixbuf_new_from_file(sys.argv[1])

width = buf.get_width()
height = buf.get_height()
rowstride = buf.get_rowstride()
bits_per_sample = buf.get_bits_per_sample()
has_alpha = buf.get_has_alpha()
colorspace = buf.get_colorspace()

arr = buf.get_pixels_array()

energ = energy(arr)
arr = grayscale_to_rgb(normalize(energ))

vM = vmatrix(energ)
for path in backtrack_nbest_vpaths(vM, n_vseams):
    mark_vpath(arr, path)

hM = hmatrix(energ)
for path in backtrack_nbest_hpaths(hM, n_hseams):
    mark_hpath(arr, path)

buf = to_pixbuf(arr)

win = gtk.Window()

img = gtk.image_new_from_pixbuf(buf)

win.add(img)

win.connect("delete-event", lambda w,e: gtk.main_quit())
win.show_all()

gtk.main()
