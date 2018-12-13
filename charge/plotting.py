import matplotlib; matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from .utils import load, group, colorscale, category, chnames
from .echem import current_differential, coulomb_conversions
from .echem import charge as ch
from .statistics import Statistics
import numpy as np
from itertools import chain


class Plot(object):

    def __init__(self, data, groups=None, active_channels=None, title=None, categories=None, span=0.2):

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

        if groups is not None:
            self.statistics = Statistics(self.data, self.groups, self.active_channels)

    def replicates(self, data):

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

    def replicates_std(self, data):
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

    def mean_std(self, data):
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
            line, = plt.plot(self.time, mean[i])
            plt.fill_between(self.time, (mean[i] - sd[i]), (mean[i] + sd[i]), color=line.get_color(), alpha=0.5, linewidth=0.0)

        if self.categories is not None:
            mean_cats = [x[0] for x in self.categories]
            plt.legend(mean_cats)
        plt.show()

    def g_replicates(self, data):
        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        plt.ylabel(u'Current (μA)', fontsize=14)
        plt.xlabel('Time (Seconds)', fontsize=14)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

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
                #print(data[o])
                #print(data[o].shape)
                #print(data[o][0].shape)
                #print(data[o][0].size)
                #exit()
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

        # flat_colors = np.array([x if x is type(list) else list(x) for x in colors]).flatten()
        # print(flat_colors)
        # print(len(data))

        # print(colors)
        # print(groups)
        # exit()

        for i in range(len(data)):

            # print(data[i].ndim)
            # print(colors)
            # print(flat_colors)
            # print(data[i].shape[0])
            # print(data[i].shape)
            # print(data[i].size)
            # exit()

            if data[i].ndim > 1:
                if data[i].shape[0] > 1:
                    for j in range(len(data[i])):
                        plt.plot(self.time, data[i][j], color=colors[i][j])
                        # print(data[i][j])
                        # print(colors[i][j])
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
        plt.show()

    def replicates_mean(self, data):
        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        plt.ylabel(u'Current (μA)', fontsize=14)
        # plt.ylabel('Charge (mC)', fontsize=14)
        plt.xlabel('Time (Seconds)', fontsize=14)

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        mprops = dict(color='#3F5D7D')

        # for i in range(len(data)):
        #     plt.plot(self.time, [x/1000 for x in data[i]])

        for i in range(len(data)):
            plt.plot(self.time, data[i])

        if self.categories is not None:
            mean_cats = [x[0] for x in self.categories]
            plt.legend(mean_cats)

        plt.show()

    def current_differential(self):

        dif = current_differential(self.g_data[1], self.g_data[2])

        charge = ch(self.g_data[1], self.g_data[2])

        # print(charge)
        # exit()

        mC, e = coulomb_conversions(charge)

        # print(mC)
        # print(e)
        # exit()

        #
        e = float('{:0.2e}'.format(e))
        mC = round(mC, 2)

        ax1 = plt.subplot(111)

        ax1.yaxis.grid(color='#F1F1F1')
        ax1.xaxis.grid(color='#F1F1F1')

        ax1.text(0.05, 0.8, 'AUC, Charge: ' + str(mC) + ' mC', transform=ax1.transAxes, fontsize=12)
        ax1.text(0.05, 0.7, 'AUC, Number of Electrons: ' + str(e) + ' e', transform=ax1.transAxes, fontsize=12)

        plt.ylabel(u'Current (μA)', fontsize=14)
        plt.xlabel('Time (Seconds)', fontsize=14)

        # plt.title('Current Differential after Addition of Substrate \n')

        if self.title is not None:
            plt.title(str(self.title) + ' \n')

        line, = plt.plot(self.time, dif)
        plt.fill_between(self.time, dif, np.zeros(len(dif)), where=dif > 0,
                         color=line.get_color(), alpha=0.5, linewidth=0.0)

        plt.legend(['[Rhodo, Add. Substrate] - [Rhodo, No Substrate]'])

        plt.show()

    def t_test(self, p_vals):

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


def boxplot(data):

    ax1 = plt.subplot(111)

    ax1.yaxis.grid(color='#F1F1F1')
    ax1.xaxis.grid(color='#F1F1F1')

    plt.ylabel('Charge (mC)', fontsize=14)
    plt.xlabel('Time', fontsize=14)
    plt.title("Impact of Addition of Substrate on Charge Produced \n", fontsize=18)

    mprops = dict(color='#3F5D7D')

    plt.boxplot(data, medianprops=mprops)
    plt.xticks([1, 2, 3, 4], [str('Day 0'), str('Day 1'), str('Day 2'), str('Day 3')])

    plt.show()
