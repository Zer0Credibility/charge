import numpy as np
import pandas as pd
import re
from tqdm import tqdm
from itertools import chain


def load(file):

    df = pd.read_excel(file, encoding='utf8', skiprows=range(1, 2))

    headers = list(df.columns.values)

    times = headers[0::2]
    bad_times = headers[2::2]
    # data = headers[1::2]

    ch_names = [s.encode('ascii') for s in times]
    ch_names = [x.strip(' '.encode()) for x in ch_names]
    ch_names = [int(re.sub('[^0-9]', '', i.decode())) for i in ch_names]

    df = df.drop(bad_times, axis=1)
    df.columns = ['Time'] + ch_names
    df = df.astype(np.float64)
    df = df.round(decimals=4)
    df = df.drop(['Time'], axis=1)

    matrix = df.values.T

    return matrix, ch_names


def group(data, groups, chs):

    groups = np.asarray(groups)
    chs_idx = [x-1 for x in chs]

    # print(groups)
    # print(chs_idx)
    # print(chs)

    if len(chs_idx) != chs_idx[-1]+1:
        # print(True)
        # print(chs_idx)
        # print(groups)
        chs_idx = list(chain.from_iterable(groups))

    # print(chs_idx)
    # exit()

    if len(chs_idx) != len(list(chain.from_iterable(groups))):
        print('One or more channels specified are not available and will be removed from output.')
        diffs = list(set(list(chain.from_iterable(groups))) - set(chs_idx))
        groups = np.asarray([[x for x in j if x not in diffs] for j in groups])

    # if len(chs_idx) != chs_idx[-1]:
    #     full_chs_idx = list(range(chs_idx[-1]+1))
    #     print(full_chs_idx)
    #
    #
    #
    #     exit()
    #
    #
    # print(chs_idx)
    # # print(groups)
    # print(data)
    #
    # print('\n')
    #
    g_data = []

    for i in range(len(groups)):
        single_group = []
        for j in range(len(groups[i])):
            # print(groups[i])
            # print(len(groups[i]))
            if groups[i][j] in chs_idx:
                # print(groups[i][j])
                # print(j)
                # print(ns_idx)
                # single_group.append(data[groups[sum(ns_idx)-1]])
                single_group.append(data[groups[i][j]])
                # print(data[groups[i][j]])
            else:
                continue
        # ns_idx.append(len(groups[i]))
        g_data.append(np.asarray(single_group))
    g_data = np.asarray(g_data)

    return g_data, groups


def category(categories, chs):
    cats = []

    for i in range(len(chs)):
        single_category = []
        for j in range(len(chs[i])):
            single_category.append(categories[i])
        cats.append(single_category)

    return cats


def chnames(groups):
    return ['Ch' + str(x+1) for x in chain.from_iterable(groups)]


def clamp(val, minimum=0, maximum=255):
    if val < minimum:
        return minimum
    if val > maximum:
        return maximum
    return val


def colorscale(hexstr, scalefactor):
    """
    Scales a hex string by ``scalefactor``. Returns scaled hex string.

    To darken the color, use a float value between 0 and 1.
    To brighten the color, use a float value greater than 1.

    """

    hexstr = hexstr.strip('#')

    if scalefactor < 0 or len(hexstr) != 6:
        return hexstr

    r, g, b = int(hexstr[:2], 16), int(hexstr[2:4], 16), int(hexstr[4:], 16)

    # print(r, g, b)
    # print(scalefactor)
    # exit()

    if scalefactor == 1.0:
        r = clamp(r)
        g = clamp(g)
        b = clamp(b)
    else:
        r = clamp(r * scalefactor)
        g = clamp(g * scalefactor)
        b = clamp(b * scalefactor)

    return f'#{int(round(r)):02x}{int(round(g)):02x}{int(round(b)):02x}'
