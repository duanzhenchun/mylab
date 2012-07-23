[1;31mType:       [0mbuiltin_function_or_method
[1;31mBase Class: [0m<type 'builtin_function_or_method'>
[1;31mString Form:[0m<built-in method getfield of numpy.ndarray object at 0x3365da0>
[1;31mNamespace:  [0mInteractive
[1;31mDocstring:[0m
a.getfield(dtype, offset)

Returns a field of the given array as a certain type.

A field is a view of the array data with each itemsize determined
by the given type and the offset into the current array, i.e. from
``offset * dtype.itemsize`` to ``(offset+1) * dtype.itemsize``.

Parameters
----------
dtype : str
    String denoting the data type of the field.
offset : int
    Number of `dtype.itemsize`'s to skip before beginning the element view.

Examples
--------
>>> x = np.diag([1.+1.j]*2)
>>> x
array([[ 1.+1.j,  0.+0.j],
       [ 0.+0.j,  1.+1.j]])
>>> x.dtype
dtype('complex128')

>>> x.getfield('complex64', 0) # Note how this != x
array([[ 0.+1.875j,  0.+0.j   ],
       [ 0.+0.j   ,  0.+1.875j]], dtype=complex64)

>>> x.getfield('complex64',1) # Note how different this is than x
array([[ 0. +5.87173204e-39j,  0. +0.00000000e+00j],
       [ 0. +0.00000000e+00j,  0. +5.87173204e-39j]], dtype=complex64)

>>> x.getfield('complex128', 0) # == x
array([[ 1.+1.j,  0.+0.j],
       [ 0.+0.j,  1.+1.j]])

If the argument dtype is the same as x.dtype, then offset != 0 raises
a ValueError:

>>> x.getfield('complex128', 1)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: Need 0 <= offset <= 0 for requested type but received offset = 1

>>> x.getfield('float64', 0)
array([[ 1.,  0.],
       [ 0.,  1.]])

>>> x.getfield('float64', 1)
array([[  1.77658241e-307,   0.00000000e+000],
       [  0.00000000e+000,   1.77658241e-307]])