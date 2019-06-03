import numpy as np
import scipy as sp
import pandas as pd
import re
from tqdm import tqdm
from .utils import load, group
import multiprocessing
from multiprocessing import Pool
from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess


class Statistics(object):

    def __init__(self, data, groups, active_channels=None, span=0.2,):

        if type(data) == str and data.lower().endswith('.xlsx'):
            self.data, self.active_channels = load(data)
            self.groups = groups
            self.g_data, self.groups = group(self.data, groups, self.active_channels)

        else:
            if active_channels is None:
                print('Please pass active channels')
                exit(1)
            else:
                self.active_channels = active_channels
                self.data = data
                self.groups = groups
                self.g_data, self.groups = group(self.data, groups, self.active_channels)

        self.span = span
        self.time = np.array(range(0, self.data.shape[1]))

    def groups(self):
        return self.g_data

    def mean(self):
        return np.array([np.mean(x, axis=0) for x in self.g_data])

    def std(self):
        return np.array([np.std(x, axis=0) for x in self.g_data])

    def smooth(self):

        sm_data = self.imap_unordered_bar(self.lowess_ind, range(len(self.data)))

        # for i in tqdm(range(len(self.data))):
        #     sm_data[i] = lowess(self.data[i], self.time,
        #                         frac=float(self.span),
        #                         it=1,
        #                         delta=0.0,
        #                         is_sorted=True,
        #                         return_sorted=False)

        return sm_data

    def noise(self):
        noise_data = np.zeros(self.data.shape)
        sm_data = self.smooth()

        for i in range(len(self.data)):
            noise_data[i] = abs(np.subtract(self.data[i], sm_data[i]))

        return noise_data

    def t_test(self, g1_idx, g2_idx):

        group1 = self.g_data[g1_idx]
        group2 = self.g_data[g2_idx]

        t_stat, p_value = sp.stats.ttest_ind(group1, group2, equal_var=False, axis=0)

        return t_stat, p_value

    def imap_unordered_bar(self, func, args, n_processes=multiprocessing.cpu_count()):
        p = Pool(n_processes)

        sm_data = np.zeros(self.data.shape)

        with tqdm(total=len(args)) as pbar:
            for i, res in tqdm(p.imap_unordered(func, args)):
                pbar.update()
                sm_data[i] = res
        pbar.close()
        p.close()
        p.join()
        return sm_data

    def lowess_ind(self, i):

        smooth = lowess(self.data[i], self.time, frac=float(self.span), it=1, delta=0.0,
                        is_sorted=True, return_sorted=False)

        return i, smooth

