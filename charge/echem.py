import numpy as np
from num2words import num2words


def charge_accumulation(data):
    return np.array([np.cumsum(x) for x in data])


def current_differential(group1, group2):

    try:
        return np.mean(group2, axis=0) - np.mean(group1, axis=0)
    except IndexError:
        return group2 - group1


def charge(group1, group2):

    """
    Integrate Current with Respect to Time in order to generate number of Coulombs
    :param group1:
    :param group2:
    :return:
    """

    # group1 = np.array(group1[np.logical_not(np.isnan(np.array(group1)))])
    # group2 = np.array(group2[np.logical_not(np.isnan(np.array(group2)))])

    # print(group1)
    # print(group2)

    x = np.mean(group2, axis=0, dtype=np.float) - np.mean(group1, axis=0, dtype=np.float)

    # print(x)
    # exit()

    return np.trapz(x[np.logical_not(np.isnan(x))])


def adjust(data, group_idxs, adjustment_factor):
    for i in range(len(group_idxs)):
        data[group_idxs[i]] = [x-adjustment_factor for x in data[group_idxs[i]]]
    return data


def coulomb_conversions(u_coulombs):

    uC = float(u_coulombs)
    mC = float(u_coulombs) / float(1e3)
    C = float(u_coulombs) / float(1e6)
    e = float(C) * float(6.24150975e18)

    print(r'µC: ' + str(uC))
    print('mC: ' + str(mC))
    print('C: ' + str(C))
    try:
        print('e: ' + str(e) + ' | [' + str(num2words(e)) + ']')
    except ValueError:
        print(e)

    return mC, e


