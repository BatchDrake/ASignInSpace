#!/usr/bin/env python3

import sys
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Helvetica"

SHIFT_COLOR = 'blue'
DRIFT_COLOR = 'green'

def plot_logfile(path):
    try:
        data = np.loadtxt(path, delimiter = ',')
        tt  = (data[:, 0] - data[0, 0]) * 86400

        units = 1
        unitName = 'seconds'
        
        ttlen = tt[-1] - tt[0]

        if ttlen > 86400:
            units = 86400
            unitName = 'days'
        elif ttlen > 3600:
            units = 3600
            unitName = 'hours'
        elif ttlen > 90:
            units = 60
            unitName = 'minutes'

        tt /= units
        
        ttc = .5 * (tt[1:] + tt[:-1])
        shift = data[:, 5]
        drift = np.diff(shift) / (86400 * np.diff(data[:, 0]))
    except RuntimeError as e:
        print(fr'{path}: log format error')
        return

    plt.figure(figsize=(10, 5))
    ax_drift = plt.gca()
    ax_shift = ax_drift.twinx()

    linewidth = 750 / len(tt)
    if linewidth > 2:
        linewidth = 2

    ax_drift.plot(ttc, drift, color = DRIFT_COLOR, linewidth = linewidth)
    ax_drift.set_ylabel('Droppler drift [Hz/s]', color = DRIFT_COLOR)
    
    ax_shift.plot(tt, shift, color = SHIFT_COLOR, linewidth = 3)
    ax_shift.set_ylabel('Doppler shift [Hz]', color = SHIFT_COLOR)
    ax_drift.set_xlabel(fr'Time since start [{unitName}]')
    
    ax_drift.grid(True, zorder=-10)
    ax_drift.tick_params(axis = 'y', color = DRIFT_COLOR)
    [t.set_color(DRIFT_COLOR) for t in ax_drift.yaxis.get_ticklabels()]
    
    ax_shift.tick_params(axis = 'y', color = SHIFT_COLOR)
    [t.set_color(SHIFT_COLOR) for t in ax_shift.yaxis.get_ticklabels()]

    ax_drift.set_ylim([-100, 100])
    plt.title(path)
    plt.tight_layout()
    
argc = len(sys.argv)

if argc < 2:
    print(fr'Usage: {sys.argv[0]} file1.log [file2.log [...]]')
    sys.exit(1)


for i in range(len(sys.argv) - 1):
    plot_logfile(sys.argv[i + 1])

plt.show()
