from charge import utils
from charge.statistics import Statistics
from charge.plotting import Plot, boxplot
from charge import echem
import numpy as np


# nc_nc = [0, 1, 2, 3]
# pc_nc = [4, 5, 6, 7]
# pc_pc = [8, 9, 10, 11]


def test_plot_greplicates():
    file = './test_data/2018-10-07_from_Paolo_1.xlsx'

    nc_nc = [1, 2]
    pc_nc = [5, 6]
    pc_pc = [9]

    # nc_nc = [12, 13, 14, 15]
    # pc_nc = [16, 17, 18, 19]
    # pc_pc = [20, 21, 22, 23]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    p_title = 'Impact of Substrate Addition on Charge, Day 1'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)
    plot = plots.g_replicates(g_data)

def test_plot_greplicates_alt_data():

    file = './test_data/acetate+ur+glucose_vs_glucose.xlsx'

    pc_nc = [0, 1, 2, 3, 4, 5]
    pc_pc = [6, 7, 8, 9, 10]

    groups = [pc_nc, pc_pc]
    categories = ['PC PC [Rhodo, +Glucose, +Acetate & Urea]', 'PC NC [Rhodo, +Acetate & Urea]']
    p_title = 'Impact of Glucose & Acetate+Urea on Production of Charge'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    # stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)
    plots.g_replicates(g_data)


def test_plot_means():
    file = './test_data/2018-10-07_from_Paolo_1.xlsx'

    # nc_nc = [0, 1, 2, 3]
    # pc_nc = [4, 5, 6, 7]
    # pc_pc = [9]

    nc_nc = [1, 2]
    pc_nc = [5, 6]
    pc_pc = [9]

    # nc_nc = [12, 13, 14, 15]
    # pc_nc = [16, 17, 18, 19]
    # pc_pc = [20, 21, 22, 23]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    p_title = 'Impact of Substrate Addition on Charge, Day 1'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    mean = stats.mean()

    # print(mean)
    # exit()

    plot = plots.replicates_mean(mean)
    print(plot)


def test_plot_means_alt():
    file = '/Users/Clayton/Documents/Electrochemistry/Datasets/Dropbox/Clayton/2018-11-20/acetate+ur+glucose_vs_glucose.xlsx'

    # nc_nc = []
    pc_nc = [0, 1, 2, 3, 4, 5]
    pc_pc = [6, 7, 8, 9, 10]

    groups = [pc_nc, pc_pc]
    categories = ['PC PC [Rhodo, +Glucose, +Acetate & Urea]', 'PC NC [Rhodo, +Acetate & Urea]']
    p_title = 'Impact of Glucose & Acetate+Urea on Production of Charge'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    # print(groups)
    # print(active_channels)
    # exit()
    # exit()

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    mean = stats.mean()

    # print(mean)
    # exit()

    # print(g_data[0])
    # print(g_data[1])
    # print(g_data[0].shape)
    # print(g_data[1].shape)
    # exit()

    plot = plots.replicates_mean(mean)
    # plot = plots.mean_std(g_data)
    print(plot)


def test_plot_replicates():
    file = './test_data/2018-10-07_from_Paolo_1.xlsx'
    p_title = 'Impact of Substrate Addition on Accumulated Charge, Day 1'
    data, active_channels = utils.load(file)
    plots = Plot(data, groups=None, active_channels=active_channels, categories=None, title=p_title)
    plot = plots.replicates(data)
    print(plot)

def test_echem_charge():

    file = './test_data/2018-10-07_from_Paolo_2.xlsx'

    nc_nc = [0, 1, 2, 3]
    pc_nc = [4, 5, 6, 7]
    pc_pc = [9]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    p_title = 'Impact of Substrate Addition on Accumulated Charge, Day 2'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    charge = echem.charge(g_data[1], g_data[2])

    return charge


def test_echem_current_differential():
    file = './test_data/2018-10-07_from_Paolo_1.xlsx'

    nc_nc = [1, 2]
    pc_nc = [5, 6]
    pc_pc = [9]

    # nc_nc = [0, 1, 2, 3]
    # pc_nc = [4, 5, 6, 7]
    # pc_pc = [9]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    p_title = 'Current Differential after Addition of Substrate, Day 1'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    plots.current_differential()


def test_plot_accumulated_charge():
    file = './test_data/2018-10-07_from_Paolo_2.xlsx'

    nc_nc = [0, 1, 2, 3]
    pc_nc = [4, 5, 6, 7]
    pc_pc = [9]

    # nc_nc = [1, 2]
    # pc_nc = [5, 6]
    # pc_pc = [9]

    # nc_nc = [12, 13, 14, 15]
    # pc_nc = [16, 17, 18, 19]
    # pc_pc = [20, 21, 22, 23]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    p_title = 'Impact of Substrate Addition on Accumulated Charge, Day 2'
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    mean = stats.mean()
    mean = echem.charge_accumulation(mean)

    plot = plots.replicates_mean(mean)
    print(plot)


def test_means_series(day):
    file = './test_data/Day' + str(day) + '.xlsx'

    if day == 0:
        nc_nc = [0, 1]
        pc_nc = [4, 5]
        pc_pc = [8, 9, 10, 11]
    else:
        nc_nc = [1]
        pc_nc = [2, 3]
        pc_pc = [4, 5, 6, 7]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    # p_title = 'Impact of Substrate Addition on Current Difference, Day ' + str(day)
    p_title = 'Impact of Substrate Addition on Current, Day ' + str(day)
    data, active_channels = utils.load(file)

    #print(active_channels)
    #exit()

    # print(len(data))
    # exit()

    g_data, groups = utils.group(data, groups, active_channels)

    # print(g_data)
    # print(groups)
    # exit()

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    mean = stats.mean()

    # print(mean)
    # exit()

    plot = plots.replicates_mean(mean)
    # plot = plots.replicates_std(g_data)
    # plot = plots.g_replicates(g_data)
    # plot = plots.replicates_mean(echem.charge_accumulation(mean))
    # plot = plots.current_differential()

    print(plot)


def test_acc_series(day):
    file = file = './test_data/Day' + str(day) + '.xlsx'

    if day == 0:
        nc_nc = [0, 1]
        pc_nc = [4, 5]
        pc_pc = [8, 9, 10, 11]
    else:
        nc_nc = [1]
        pc_nc = [2, 3]
        pc_pc = [4, 5, 6, 7]

    groups = [nc_nc, pc_nc, pc_pc]
    categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    p_title = 'Impact of Substrate Addition on Current, Day ' + str(day)
    # p_title = 'Impact of Substrate Addition on Current Difference, Day ' + str(day)
    # p_title = 'Impact of Substrate Addition on Accumulated Charge, Day ' + str(day)
    data, active_channels = utils.load(file)

    #print(active_channels)
    #exit()

    # print(len(data))
    # exit()

    g_data, groups = utils.group(data, groups, active_channels)

    # print(g_data)
    # print(groups)
    # exit()

    stats = Statistics(data, groups, active_channels)
    plots = Plot(data, groups, active_channels, categories=categories, title=p_title)

    mean = stats.mean()

    # print(mean)
    # exit()

    plot = plots.replicates_mean(mean)
    # plot = plots.replicates_std(g_data)
    # plot = plots.g_replicates(g_data)
    # plot = plots.replicates_mean(echem.charge_accumulation(mean))
    # plot = plots.current_differential()

    print(plot)


def test_series_std_acc(day):
    file = file = './test_data/Day' + str(day) + '.xlsx'

    if day == 0:
        nc_nc = [0, 1]
        pc_nc = [4, 5]
        pc_pc = [8, 9, 10, 11]
    else:
        nc_nc = [1]
        pc_nc = [2, 3]
        pc_pc = [4, 5, 6, 7]

    groups = [nc_nc, pc_nc, pc_pc]
    # categories = ['NC NC [No Cells, No Substrate]', 'PC NC [Rhodo, No Substrate]', 'PC PC [Rhodo, Add. Substrate]']
    # p_title = 'Impact of Substrate Addition on Current Difference, Day ' + str(day)
    data, active_channels = utils.load(file)
    g_data, groups = utils.group(data, groups, active_channels)

    # mean_pc_nc = np.mean(groups[1])

    # print(g_data)
    # exit()

    mean_dif = []
    aucs = []
    for i in range(len(g_data[2])):
        x = g_data[2][i] - np.mean(g_data[1], axis=0)
        # print(x)
        y = x[np.logical_not(np.isnan(x))]
        # print(y)
        mean_dif.append(y)
        auc = np.trapz(y)
        aucs.append(auc)

    # print(mean_dif)
    # print(aucs)
    # exit()
    #
    # # print(g_data[2])
    # # exit()
    #
    # aucs = [echem.charge(g_data[1], np.array(x)) for x in g_data[2]]
    #
    # print(aucs)

    aucs = [x/1000 for x in aucs]

    return aucs


# alternat_data()
# exit()


# aucs = []
# for i in [0, 1, 2, 3]:
#     aucs.append(test_series_std_acc(i))
#
# boxplot(aucs)

# test_plot_means_alt()
test_plot_greplicates_alt_data()

# test_means_series(0)
# test_acc_series(3)

# test_plot_accumulated_charge()
# test_echem_current_differential()
# test_plot_greplicates()
# test_plot_means()
# test_plot_replicates()
# Q = test_echem_charge()
# C = echem.coulomb_conversions(Q)

#

# smooth = stats.mean
# stats = Statistics(smooth, groups, active_channels)

# mean = stats.mean()
# plot = plots.replicates_mean(mean)


# plots.current_differential()

# print(mean)
# exit()

# print(utils.group(data, groups, active_channels))
# exit()


# smoothed = stats.smooth()
# plot = plots.replicates_std(mean)

# plot = plots.g_replicates(g_data)


# t_stat, p_value = stats.t_test(1, 2)

# plots.replicates(p_value)

# print(noise.shape)
# print(noise)
