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

"""
Implementation of the technique described in

"Seam Carving for Content-Aware Image Resizing"
by Shai Avidan and Ariel Shamir
"""

import sys
from gtk import gdk
import numpy as np

INF = float("infinity")

def argmin(arr):
    return list(arr).index(min(arr))

def grayscale_to_rgb(img):
    """
    Return a NxMx3 matrix in RGB from a NxM matrix in grayscale.
    """
    rows, cols = img.shape
    return np.repeat(img, 3).reshape((rows, cols, 3)).astype(np.uint8)

def rgb_to_grayscale(img):
    """
    Return a NxM matrix in grayscale from a NxMx3 matrix in RGB.
    """
    return (img[:,:,0].astype(np.uint32) * 30 + \
            img[:,:,1].astype(np.uint32) * 59 + \
            img[:,:,2].astype(np.uint32) * 11) / 100

def energy(img):
    """
    Return a NxM matrix of the gradients from a NxMx3 matrix.
    """
    #gradx, grady = np.gradient(img.mean(axis=2))
    gradx, grady = np.gradient(rgb_to_grayscale(img).astype(np.float32))
    return np.abs(gradx) + np.abs(grady)

def normalize(img):
    """
    Ensure values are between 0 and 255.
    """
    return np.floor(img * 255.0 / (img.max() - img.min()))

def mark_vpath(img, path, color=(255, 0, 0)):
    """
    Mark a vertical path on a NxMx3 matrix.
    """
    #img[:,path] = np.array(color)
    for i,j in enumerate(path):
        img[i,j] = np.array(color)

def mark_hpath(img, path, color=(255, 0, 0)):
    """
    Mark a horizontal path on a NxMx3 matrix.
    """
    for j,i in enumerate(path):
        img[i,j] = np.array(color)

def vtriple(M, i, j):
    """
    Return the 3 candidate neighbor pixels for pixel (i,j) in a vertical path.

    This forms the local constraints of the DP-algorithm, for vertical paths.
    """
    if j == 0: # left edge
        return (INF, M[i-1,j], M[i-1,j+1])
    elif j == M.shape[1]-1: # right edge
        return (M[i-1,j-1], M[i-1,j], INF)
    else:
        return (M[i-1,j-1], M[i-1,j], M[i-1,j+1])

def htriple(M, i, j):
    """
    Return the 3 candidate neighbor pixels for pixel (i,j) in a horizontal path.

    This forms the local constraints of the DP-algorithm, for horizontal paths.
    """
    if i == 0: # top edge
        return (INF, M[i,j-1], M[i+1,j-1])
    elif i == M.shape[0]-1: # bottom edge
        return (M[i-1,j-1], M[i,j-1], INF)
    else:
        return (M[i-1,j-1], M[i,j-1], M[i+1,j-1])

def vmatrix(energ):
    """
    Return the cumulated distance matrix for vertical paths.
    """
    rows, cols = energ.shape
    M = np.zeros(energ.shape, dtype=np.float32)
    M[0,:] = energ[0,:]

    for i in range(1, rows):
        for j in range(0, cols):
            M[i,j] = energ[i,j] + min(vtriple(M, i, j))

    return M

def hmatrix(energ):
    """
    Return the cumulated distance matrix for horizontal paths.
    """
    rows, cols = energ.shape
    M = np.zeros(energ.shape, dtype=np.float32)
    M[:,0] = energ[:,1]

    for j in range(1, cols):
        for i in range(0, rows):
            M[i,j] = energ[i,j] + min(htriple(M, i, j))

    return M

def backtrack_vpath(M, from_col):
    """
    Backtrack the best vertical path starting from a given column.
    """
    rows, cols = M.shape
    path = np.zeros((rows,), dtype=np.uint32)
    j = path[rows-1] = from_col

    for i in range(rows-2, -1, -1):
        # argmin(vtriple(M, i, j)) returns one of 0, 1, 2
        # so j becomes either j-1, j or j+1
        j = path[i] = j + argmin(vtriple(M, i, j)) - 1

    return path

def backtrack_hpath(M, from_row):
    """
    Backtrack the best horizontal path starting from a given row.
    """
    rows, cols = M.shape
    path = np.zeros((cols,), dtype=np.uint32)
    i = path[cols-1] = from_row

    for j in range(cols-2, -1, -1):
        i = path[j] = i + argmin(htriple(M, i, j)) - 1

    return path

def backtrack_nbest_vpaths(M, n):
    """
    Backtrack the n best vertical paths in cumulated distance matrix.
    """
    from_cols = M[-1,:].argsort()[:n]
    return [backtrack_vpath(M, from_col) for from_col in from_cols]

def backtrack_nbest_hpaths(M, n):
    """
    Backtrack the n best horizontal paths in cumulated distance matrix.
    """
    from_rows = M[:,-1].argsort()[:n]
    return [backtrack_hpath(M, from_row) for from_row in from_rows]

def remove_vpath(arr, path):
    """
    Remove vertical path from matrix.
    """
    rows, cols = arr.shape[:2]
    return np.array([arr[i,:][np.arange(cols) != path[i]] for i in range(rows)])

def remove_hpath(arr, path):
    """
    Remove horizontal path from matrix.
    """
    rows, cols = arr.shape[:2]
    arr =  np.array([arr[:,i][np.arange(rows) != path[i]] for i in range(cols)])
    return arr.transpose()

def from_2d_to_3d(a):
    """
    Convert NxM matrix to NxMx3 matrix.
    """
    return np.dstack(((a >> 16) & 0xFF, (a >> 8) & 0xFF, a & 0xFF)). \
              astype(np.uint8)

def from_3d_to_2d(a):
    """
    Convert NxMx3 matrix to NxM matrix.
    """
    return (a[:,:, 0].astype(np.uint32) << 16) | \
           (a[:,:,1].astype(np.uint32) << 8) | \
            a[:,:,2]

def decrease_size(img, perc_w, perc_h):
    rows, cols = img.shape[:2]
    drows = rows - int(rows * perc_h)
    dcols = cols - int(cols * perc_w)

    energ = energy(img)

    img = from_3d_to_2d(img)

    # For simplicity, we remove all vertical seams first, 
    # then all horizontal seams. Ideally, the removals should be done
    # in the optimal order, as described in the paper.

    print "processing vertical seams"
    vM = vmatrix(energ)
    for i in range(dcols):
        if i % 10 == 0 or i == dcols-1: print "%d/%d" % (i+1, dcols)
        path = backtrack_nbest_vpaths(vM, 1)[0]
        img = remove_vpath(img, path)
        vM = remove_vpath(vM, path)
        energ = remove_vpath(energ, path)

    print "processing horizontal seams"
    hM = hmatrix(energ)
    for i in range(drows):
        if i % 10 == 0 or i == drows-1: print "%d/%d" % (i+1, drows)
        path = backtrack_nbest_hpaths(hM, 1)[0]
        img = remove_hpath(img, path)
        hM = remove_hpath(hM, path)

    return from_2d_to_3d(img)

def resize(img, perc_w, perc_h):
    if perc_w <= 1.0 and perc_h <= 1.0:
        return decrease_size(img, perc_w, perc_h)
    else:
        raise NotImplementedError # TODO

def to_pixbuf(img, colorspace=gdk.COLORSPACE_RGB, bits_per_sample=8):
    """
    Convert NxMx3 matrix to GDK pixbuf.
    """
    return gdk.pixbuf_new_from_array(np.asarray(img, dtype=np.uint8), 
                                     colorspace, bits_per_sample)

def save_pixbuf(pixbuf, filename):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        pixbuf.save(filename, "jpeg")
    else:
        pixbuf.save(filename, "png")
