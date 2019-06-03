import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib import rc
from .utils import load, group, colorscale, category, chnames
from .echem import current_differential, coulomb_conversions
from .echem import charge as ch
from .statistics import Statistics
import numpy as np
from itertools import chain


class Plot(object):

    def __init__(self, data, groups=None, active_channels=None, std=True,
                 title=None, categories=None, span=0.2, latex=False, fontsize=12,
                 ratio='golden', ylim_bottom=None, ylim_top=None):
        """

        :param data:
        :param groups:
        :param active_channels:
        :param std: Bool - Standard Deviation Error Bars Plotting On/Off
        :param title:
        :param categories:
        :param span:
        :param latex:
        :param fontsize:
        :param ratio: 'golden', or 'square', '4:3', or default
        :param ylim_bottom:
        :param ylim_top:
        """

        if type(data) == str and data.lower().endswith('.xlsx'):
            self.data, self.active_channels = load(data)
            if groups is not None:
                self.groups = groups
                self.g_names = chnames(groups)
                self.g_data, self.groups = group(data, groups, self.active_channels)
            else:
                self.g_names = None
        else:
            if active_channels is None:
                print('Please pass active channels')
                exit(1)
            else:
                self.active_channels = active_channels
                self.data = data
                if groups is not None:
                    self.groups = groups
                    self.g_names = chnames(groups)
                    self.g_data, self.groups = group(data, groups, self.active_channels)
                else:
                    self.g_names = None

        self.span = span
        if categories is not None:
            self.categories = category(categories, groups)
        else:
            self.categories = None
        self.time = np.array(range(0, self.data.shape[1]))

        self.title = title
        self.ratio = ratio

        self.fontsize = fontsize

        fig = matplotlib.pyplot.gcf()
        if self.title is None:
            fig.subplots_adjust(top=0.925)
        if ratio is 'golden':
            x = 6
            y = x / 0.618
            fig.set_size_inches(y, x, forward=True)
        elif ratio is 'square':
            x, y = 6, 6
            fig.set_size_inches(y, x, forward=True)
        elif ratio is 'fourbythree':
            print('Ratio set to 4:3')
            x, y = 9, 9/(4/3)
            fig.set_size_inches(x, y, forward=True)
            self.fontsize = x * (25/9)
        else:
            pass

        if groups is not None:
            self.statistics = Statistics(self.data, self.groups, self.active_channels)

        self.latex = latex
        if self.latex:


            # setup matplotlib to use latex for output
            self.params = {
                "pgf.texsystem": "pdflatex",
                "text.usetex": True,
                "font.family": "serif",
                "font.serif": ["Palatino"],
                "pgf.preamble": [
                    r"\usepackage[T1]{fontenc}",  # plots will be generated
                    r"\usepackage[detect-all,locale=DE]{siunitx}",
                ]
            }

            # matplotlib.rc('text', usetex=True)
            # matplotlib.rc('font', **{'family': "sans-serif"})
            #
            # params = {'text.latex.preamble': [r'\usepackage{siunitx}',
            #                                   r'\usepackage{sfmath}', r'\sisetup{detect-family = true}',
            #                                   r'\usepackage{amsmath}']}

            matplotlib.rcParams.update(self.params)
        else:
            pass

        self.std = std

        if ylim_bottom is not None:
            self.ylim_bottom = ylim_bottom
        else:
            self.ylim_bottom = None
        if ylim_top is not None:
            self.ylim_top = ylim_top
        else:
            self.ylim_top = None

    def replicates(self, data):
        """

        :param data:
        :return:
        """

        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        plt.ylabel(u'Current (μA)', fontsize=14)
        plt.xlabel('Time (Seconds)', fontsize=14)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        for i in range(len(data)):
            plt.plot(self.time, data[i])

        if self.g_names is not None:
            if self.categories is None:
                plt.legend(self.g_names)
            elif self.categories is not None:
                lab = [str(x[0]) + ' | ' + str(x[1]) for x in zip(self.g_names,
                                                                  list(chain.from_iterable(self.categories)))]
                plt.legend(lab)

        plt.show()
        return plt

    def replicates_std(self, data):
        """

        :param data:
        :return:
        """
        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        plt.ylabel(u'Current (μA)', fontsize=14)
        plt.xlabel('Time (Seconds)', fontsize=14)

        mean = self.statistics.mean()
        sd = self.statistics.std()

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        for i in range(len(data)):
            line, = plt.plot(self.time, data[i])
            plt.fill_between(self.time, (mean[i] - sd[i]), (mean[i] + sd[i]), color=line.get_color(), alpha=0.5, linewidth=0.0)

        if self.categories is not None:
            mean_cats = [x[0] for x in self.categories]
            plt.legend(mean_cats)
        plt.show()
        return plt

    def mean_std(self, data):
        """
        Individual Replicates Data Plotting
        :param data:
        :return:
        """
        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        # plt.ylabel(u'Current (μA)', fontsize=14)
        # plt.xlabel('Time (Seconds)', fontsize=14)

        if self.ylim_bottom is not None and self.ylim_top is not None:
            plt.ylim(self.ylim_bottom, self.ylim_top)

        if self.latex:
            plt.ylabel(r'Current (\textmu A)', fontsize=self.fontsize)
        else:
            plt.ylabel(u'Current (μA)', fontsize=self.fontsize)
        plt.xlabel('Time (Seconds)', fontsize=self.fontsize)

        plt.xticks(fontsize=self.fontsize/1.4)
        plt.yticks(fontsize=self.fontsize / 1.4)

        mean = self.statistics.mean()
        sd = self.statistics.std()

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        for i in range(len(data)):
            line, = plt.plot(self.time, mean[i])
            plt.fill_between(self.time, (mean[i] - sd[i]), (mean[i] + sd[i]), color=line.get_color(), alpha=0.5, linewidth=0.0)

        if self.categories is not None:
            mean_cats = [x[0] for x in self.categories]
            plt.legend(mean_cats, fontsize=self.fontsize/1.55)
        plt.show()
        return plt

    def g_mean(self, data):
        """
        Group Means & Standard Deviation Plotting
        :param data: Group data
        :return: Plot
        """

        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        if self.ylim_bottom is not None and self.ylim_top is not None:
            plt.ylim(self.ylim_bottom, self.ylim_top)

        if self.latex:
            plt.ylabel(r'Current (\textmu A)', fontsize=self.fontsize)
        else:
            plt.ylabel(u'Current (μA)', fontsize=self.fontsize)

        plt.xlabel('Time (Seconds)', fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize/1.4)
        plt.yticks(fontsize=self.fontsize / 1.4)

        mean = self.statistics.mean()
        sd = self.statistics.std()

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        for i in range(len(data)):
            line, = plt.plot(self.time, mean[i])

            if self.std is True:
                plt.fill_between(self.time,
                                 (mean[i] - sd[i]),
                                 (mean[i] + sd[i]),
                                 color=line.get_color(),
                                 alpha=0.5,
                                 linewidth=0.0)
            else:
                pass

        if self.categories is not None:
            mean_cats = [x[0] for x in self.categories]
            plt.legend(mean_cats, fontsize=self.fontsize/1.55)

        return plt

    def g_replicates(self, data):
        """

        :param data:
        :return:
        """
        ax1 = plt.subplot(111)

        # ax1.set_ylabel(u'Current (μA)', fontsize=14)
        # ax1.set_xlabel('Time (Seconds)', fontsize=14)

        # plt.ylabel(u'Current (μA)', fontsize=14)
        # plt.xlabel('Time (Seconds)', fontsize=14)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        plt.suptitle(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        groups = np.array(self.groups)

        colors = []

        for o in range(len(groups)):
            sgroup_color = []

            if len(groups[o]) is 0:
                continue
            elif len(groups[o]) is 1:
                line, = plt.plot(self.time, data[o].flatten())
                s_color = line.get_color()
                colors.append(s_color)
            else:
                if data[o][0].size is not 1:
                    line, = plt.plot(self.time, data[o][0])
                    for i in range(len(groups[o])):
                        # s_color = colorscale(line.get_color(), 1-(i/(len(groups[o])+1)))  # Darken
                        s_color = colorscale(line.get_color(), 1+(i/(len(groups[o])+2)))  # Lighten
                        sgroup_color.append(s_color)
                    colors.append(sgroup_color)
                else:
                    line, = plt.plot(self.time, data[o])
                    for i in range(len(groups[o])):
                        # s_color = colorscale(line.get_color(), 1-(i/(len(groups[o])+1)))  # Darken
                        s_color = colorscale(line.get_color(), 1 + (i / (len(groups[o]) + 2)))  # Lighten
                        sgroup_color.append(s_color)
                    colors.append(sgroup_color)

        plt.cla()

        for i in range(len(data)):
            if data[i].ndim > 1:
                if data[i].shape[0] > 1:
                    for j in range(len(data[i])):
                        plt.plot(self.time, data[i][j], color=colors[i][j])
                elif data[i].shape[0] is 1:
                    plt.plot(self.time, np.array(data[i]).flatten(), color=colors[i])
                else:
                    continue
            elif data[i].ndim is 1:
                # print(data[i])
                plt.plot(self.time, np.array(data[i]), color=colors[i])

        if self.g_names is not None:
            if self.categories is None:
                plt.legend(self.g_names)
            elif self.categories is not None:
                lab = [str(x[0]) + ' | ' + str(x[1]) for x in zip(self.g_names,
                                                                  list(chain.from_iterable(self.categories)))]
                plt.legend(lab)

        ax1.set_ylabel(u'Current (μA)')
        ax1.set_xlabel('Time (Seconds)')

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        return plt

    def replicates_mean(self, data):
        """

        :param data:
        :return:
        """
        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        if self.ylim_bottom is not None and self.ylim_top is not None:
            plt.ylim(self.ylim_bottom, self.ylim_top)

        if self.latex:
            plt.rcParams.update(self.params)
            # plt.ylabel(r'Current (\textmu A)', fontsize=self.fontsize)
            plt.ylabel(r'Charge (mC)', fontsize=self.fontsize)
        else:
            plt.ylabel(u'Current (μA)', fontsize=self.fontsize)

        plt.xlabel('Time (Seconds)', fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize/1.4)
        plt.yticks(fontsize=self.fontsize / 1.4)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        for i in range(len(data)):
            plt.plot(self.time, data[i])

        if self.categories is not None:
            mean_cats = [x[0] for x in self.categories]
            plt.legend(mean_cats, fontsize=self.fontsize/1.55)

        return plt

    def current_differential(self):
        """
        Plot Area Under Curve of fed rhodo vs Negative Control
        :return:
        """

        dif = current_differential(self.g_data[1], self.g_data[2])
        charge = ch(self.g_data[1], self.g_data[2])

        mC, e = coulomb_conversions(charge)

        e = float('{:0.2e}'.format(e))
        mC = round(mC, 2)

        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        print('AUC, Charge: ' + str(mC) + ' mC')
        print('AUC, Number of Electrons: ' + str(e) + ' e')

        # ax1.text(0.05, 0.8, 'AUC, Charge: ' + str(mC) + ' mC', transform=ax1.transAxes, fontsize=self.fontsize-2)
        # ax1.text(0.05, 0.7, 'AUC, Number of Electrons: ' + str(e) + ' e', transform=ax1.transAxes, fontsize=self.fontsize-2)

        if self.latex:
            plt.ylabel(r'Current (\textmu A)', fontsize=self.fontsize)
            plt.legend([r'[\textit{R. palustris}, Add. Substrate] - [\textit{R. palustris}, No Substrate]'],
                       fontsize=self.fontsize/1.55)
        else:
            plt.ylabel(u'Current (μA)', fontsize=self.fontsize)
            plt.legend(['[R. palustris, Add. Substrate] - [R. palustris, No Substrate]'],
                       fontsize=self.fontsize/1.55)

        plt.xlabel('Time (Seconds)', fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize/1.4)
        plt.yticks(fontsize=self.fontsize / 1.4)

        if self.ylim_bottom is not None and self.ylim_top is not None:
            plt.ylim(self.ylim_bottom, self.ylim_top)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        line, = plt.plot(self.time, dif)
        plt.fill_between(self.time, dif, np.zeros(len(dif)), where=dif > 0,
                         color=line.get_color(), alpha=0.5, linewidth=0.0)

        return plt

    def t_test(self, p_vals):
        """

        :param p_vals:
        :return:
        """

        ax1 = plt.subplot(111)

        time = np.array(range(0, len(p_vals)))

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        plt.ylabel(u'Current (μA)', fontsize=14)
        plt.xlabel('Time (Seconds)', fontsize=14)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        plt.plot(time, p_vals)

        plt.legend()
        plt.show()
        return plt


class BoxPlot(object):

    def __init__(self, file_list=None, title=None, groups=None, categories=None,
                 pc_idx=1, nc_idx=0, latex=True, ratio='golden', fontsize=12):
        """

        :param file_list:
        :param title:
        :param groups:
        :param categories:
        :param pc_idx:
        :param nc_idx:
        :param latex:
        """
        self.title = title
        self.file_list = file_list
        self.groups = groups
        self.categories = categories
        self.negative_control_idx = nc_idx
        self.positive_control_idx = pc_idx

        self.fontsize = fontsize
        self.ratio = ratio

        fig = matplotlib.pyplot.gcf()
        if self.title is None:
            fig.subplots_adjust(top=0.925)
        if ratio is 'golden':
            x = 6
            y = x / 0.618
            fig.set_size_inches(y, x, forward=True)
        elif ratio is 'square':
            x, y = 6, 6
            fig.set_size_inches(y, x, forward=True)
        elif ratio is 'fourbythree':
            print('Ratio set to 4:3')
            x, y = 9, 9/(4/3)
            fig.set_size_inches(x, y, forward=True)
            self.fontsize = x * (25/9)
        else:
            pass

        if latex:
            rc('font', **{'family': 'serif', 'serif': ['Palatino']})
            rc('text', usetex=True)
            self.latex = True
        else:
            pass

    def multi_acus_load(self):
        """

        :return:
        """
        files = self.file_list

        aucs = []
        for i in range(len(files)):
            aucs.append(self.auc_load(files[i]))

        return aucs

    def auc_load(self, filename):
        """

        :param filename:
        :return:
        """

        if self.groups is not None:
            pass
        else:
            print('Requires Groups')
            exit(500)

        data, active_channels = load(filename)
        g_data, groups = group(data, self.groups, active_channels)

        mean_dif = []
        aucs = []
        for i in range(len(g_data[self.positive_control_idx])):
            x = g_data[self.positive_control_idx][i] - np.mean(g_data[self.negative_control_idx], axis=0)
            y = x[np.logical_not(np.isnan(x))]
            mean_dif.append(y)
            auc = np.trapz(y)
            aucs.append(auc)
        aucs = [x / 1000 for x in aucs]  # Convert uC to mC

        return aucs

    def auc_boxplot(self, aucs=None):
        """

        :param aucs:
        :return:
        """

        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        if self.latex:
            plt.ylabel(r'Charge (mC)', fontsize=self.fontsize)
            plt.xlabel(r'Time', fontsize=self.fontsize)
        else:
            plt.ylabel('Charge (mC)', fontsize=self.fontsize)
            plt.xlabel('Time', fontsize=self.fontsize)

        plt.xticks(fontsize=self.fontsize/1.4)
        plt.yticks(fontsize=self.fontsize / 1.4)

        if self.title is not None:
            plt.title(self.title, fontsize=self.fontsize)

        mprops = dict(color='#3F5D7D')

        if aucs is not None:
            pass
        else:
            aucs = self.multi_acus_load()

        days = [r'Day ' + str(i) for i in range(len(aucs))]

        plt.boxplot(aucs, medianprops=mprops)
        plt.xticks(range(1, len(aucs)+1), days)

        plt.show()

        return plt


