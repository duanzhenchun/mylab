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

import unittest
import numpy as np

from seamcarving import *

class SeamCarvingTest(unittest.TestCase):

    def testVerticalPathRemoval(self):
        path = np.array([1, 2, 0, 1])

        a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
        b = np.array([[1,3],[4,5],[8,9],[10,12]])
        self.assertTrue(np.array_equal(remove_vpath(a, path), b))

    def testHorizontalPathRemoval(self):
        path = np.array([2, 1, 0])

        a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
        b = np.array([[1,2,6],[4,8,9],[10, 11,12]])       
        self.assertTrue(np.array_equal(remove_hpath(a, path), b))

    def test2dTo3d(self):
        a = np.asarray(np.floor(np.random.random((5, 4, 3)) * 255), 
                      dtype=np.uint8)
        self.assertTrue(np.array_equal(from_2d_to_3d(from_3d_to_2d(a)), a))

if __name__ == "__main__":
    unittest.main()
