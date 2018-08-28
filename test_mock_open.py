#!/usr/bin/env python
from mock import mock_open, patch


def wrap_open(fname, *args):
    return open(fname, *args)


def fs_read(fname):
    with wrap_open(fname, 'r') as fo:
        return fo.read()


def fs_write(fname, txt):
    with open(fname, 'w') as fo:
        for l in txt.split('\n'):
            fo.write(l + '\n')


def test_read():
    ''' Test fs.read() works. '''
    filename = 'somefile'
    data = 'somedata'

    with patch('__builtin__.open', mock_open(read_data=data)) as mock_file:
        assert fs_read(filename) == data
        mock_file.assert_called_with(filename, 'r')


def test_write():
    ''' Test fs.write() works. '''
    filename = 'somefile'
    data = 'somedata\nfefe'
    m = mock_open()

    with patch('__builtin__.open', m) as mock_file:
        fs_write(filename, data)
        mock_file.assert_called_with(filename, 'w')
        m().write.assert_called_with('fefe\n')
