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

if len(sys.argv) < 4:
    print """Decrease/Increase size of image

%s imgfile perc_width perc_height [output]

perc_width and perc_height: 0 < x < 1 for decrease, x > 1 for increase 
""" % sys.argv[0]

    exit(1)

perc_width = float(sys.argv[2])
perc_height = float(sys.argv[3])

buf = gdk.pixbuf_new_from_file(sys.argv[1])
arr = buf.get_pixels_array()

arr = resize(arr, perc_width, perc_height)
buf = to_pixbuf(arr)

if len(sys.argv) == 5:
    save_pixbuf(buf, sys.argv[4])
else:
    win = gtk.Window()

    img = gtk.image_new_from_pixbuf(buf)

    win.add(img)

    win.connect("delete-event", lambda w,e: gtk.main_quit())
    win.show_all()

    gtk.main()
