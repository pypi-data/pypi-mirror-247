#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mbejtka
"""
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import os
from traub_data_kcsd_column_figure import (prepare_electrodes, prepare_pots,
                                           do_kcsd, set_axis)
import kCSD2D_reconstruction_from_npx as npx
from scipy.signal import filtfilt, butter


def make_plot_spacetime(ax, val, cut=9, title='True CSD',
                        cmap=plt.cm.bwr, letter='A', ylabel=True):
    yy = np.linspace(-3500, 500, val.shape[1])
    xx = np.linspace(-50, 250, val[cut, :, :].shape[1])
    max_val = np.max(np.abs(val[cut, :, :]))
    levels = np.linspace(-max_val, max_val, 200)
    im = ax.contourf(xx, yy, val[cut, :, :], levels=levels, cmap=cmap)
    if 'CSD' in title:
        name = ['', 'II/III', 'IV', 'V', 'VI']
        layer_level = [0, -400, -700, -1200, -1700]
        for i, value in enumerate(layer_level):
            plt.axhline(y=value, xmin=xx.min(), xmax=xx.max(), linewidth=1,
                        color='k', ls='--')
            plt.text(110, value+165, name[i], fontsize=10, va='top', ha='center')
    ax.set_xlabel('Time (ms)')
    if ylabel:
        ax.set_ylabel('Y ($\mu$m)')
    ax.set_title(title, fontsize=20, pad=30)
    ax.set_xlim(-50, 100)
    ticks = np.linspace(-max_val, max_val, 3, endpoint=True)
    plt.colorbar(im, orientation='horizontal', format='%.3f', ticks=ticks)
    set_axis(ax, letter=letter)
    #plt.tight_layout()


def make_plot_1D_pics(ax, k, est_val, tp, Fs, cut=9, title='Experimental data',
                      cmap=plt.cm.bwr, letter='A', ylabel=True):

    set_axis(ax, letter=letter)
    npx.make_plot_spacetime(ax, k.estm_x, k.estm_y, est_val[cut,:,:], Fs,
                            title=title, cmap=cmap, ylabel=ylabel)
    if letter == 'D':
        for lvl, name in zip([-500,-850,-2000], ['II/III', 'IV', 'V/VI']):
            plt.axhline(lvl, ls='--', color='grey')
            plt.text(340, lvl+20, name)
    elif letter == 'C':
        plt.axvline(tp/Fs*1000, ls='--', color ='grey', lw=2)
    
    plt.xlim(250, 400)
    plt.xticks([250, 300, 350, 400], [-50, 0, 50, 100])
    
    #plt.tight_layout()
    plt.savefig('figure_1D_pics', dpi=300)


def make_figure_spacetime(val_pots_m, val_csd_m, kcsd_obj, val_pots_e, val_csd_e, tp, Fs, cut1=13, cut2=15,
                          titl1='POT', titl2='CSD', fig_title='Pot and CSD in time'):
    fig = plt.figure(figsize=(16, 8))
    ax2 = plt.subplot(141)
    make_plot_spacetime(ax2, val_pots_m, cut=cut1,
              title=titl1, cmap=plt.cm.PRGn, letter='A')
    ax1 = plt.subplot(142)
    make_plot_spacetime(ax1, val_csd_m, cut=cut1, 
              title=titl2, cmap=plt.cm.bwr, letter='B', ylabel=False)
    ax3 = plt.subplot(143)
    make_plot_1D_pics(ax3, kcsd_obj, val_pots_e, tp, Fs, cut=cut2, title=titl1, cmap=plt.cm.PRGn, letter='C', ylabel=False)
    ax4 = plt.subplot(144)
    make_plot_1D_pics(ax4, kcsd_obj, val_csd_e, tp, Fs, cut=cut2, title=titl2, cmap=plt.cm.bwr, letter='D', ylabel=False)
    plt.tight_layout()
    fig.savefig(os.path.join(fig_title + '.png'), dpi=300)


if __name__ == '__main__':
    time_pt_interest = 3000
    time_pts = 6000  # number of all time frames
    num_cmpts = [74, 74, 59, 59, 59, 59, 61, 61, 50, 59, 59, 59]
    cell_range = [0, 1000, 1050, 1140, 1230, 1320,
                  1560, 2360, 2560, 3060, 3160, 3260, 3360]
    num_cells = np.diff(cell_range) / 10  # 10% MODEL
    total_cmpts = list(num_cmpts * num_cells)
    pop_names = ['pyrRS23', 'pyrFRB23', 'bask23', 'axax23', 'LTS23',
                 'spinstel4', 'tuftIB5', 'tuftRS5', 'nontuftRS6',
                 'bask56', 'axax56', 'LTS56']

    h = h5.File('pulsestimulus10model.h5', 'r')
    elec_pos_list, names_list = prepare_electrodes()

    pot_np = prepare_pots(elec_pos_list[1], names_list[1], h, pop_names, time_pts)
    kcsd_m, est_pot_m, x_m, y_m, k_m = do_kcsd(pot_np, elec_pos_list[1][:, :2], -40, 40, -3500, 500)
    
    lowpass = 0.5
    highpass = 300
    Fs = 30000
    resamp = 12
    tp= 760
    
    forfilt=np.load('npx_data.npy')
    
    [b,a] = butter(3, [lowpass/(Fs/2.0), highpass/(Fs/2.0)] ,btype = 'bandpass')
    filtData = filtfilt(b,a, forfilt)
    pots_resamp = filtData[:,::resamp]
    pots = pots_resamp[:, :]
    Fs=int(Fs/resamp)
    
    pots_for_csd = np.delete(pots, 191, axis=0)
    ele_pos_def = npx.eles_to_coords(np.arange(384,0,-1))
    ele_pos_for_csd = np.delete(ele_pos_def, 191, axis=0)
    
    k_e, est_csd_e, est_pots_e, ele_pos_e = npx.do_kcsd(ele_pos_for_csd, pots_for_csd, ele_limit = (0,320))
    
    time_pts_ds = int(time_pts/4)
    cut1 = 9
    start_pt = 625  # 50 ms before the stimulus
    end_pt = 1375  # 250 ms after the stimulus
    # for cut in range(kcsd.shape[0]):
    make_figure_spacetime(est_pot_m[:, :, start_pt:end_pt],
                          kcsd_m[:, :, start_pt:end_pt], k_e, est_pots_e, est_csd_e, tp, Fs, cut1=cut1, cut2=15,
                          titl1='Estimated LFP', titl2='Estimated CSD',
                          fig_title=('Estimated POT and CSD in time 1stim '))
    #plot_1D_pics(k, est_csd, est_pots, tp, 15)
