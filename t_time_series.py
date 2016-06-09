#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import numpy as np


def test():
    df = pd.DataFrame({'a': [1, 3, 5, 7, 4, 5, 6, 4, 7, 8, 9],
                       'b': [3, 5, 6, 2, 4, 6, 7, 8, 7, 8, 9]})
    df['a'].values.tolist()
    df.head()
    df.tail()
    df.append(df.iloc[3], ignore_index=True)


def t_random():
    df = pd.DataFrame(np.random.randn(8, 2), columns=['A', 'B'])
    return df


def convert_matrix(df):
    ma = df.as_matrix()
    df.from_records(ma)


def with_csv(df):
    row_list = df.to_csv(None, header=False, index=False).split('\n')
    return row_list
