import numpy as np
import h5py
import matplotlib.pyplot as plt

def read_files(infiles, read_vars, read_params):
    """
    function that reads variables from input hdf5 file
    
    parameters
        infiles (list): -  of file paths
        read_vars (list): - list of event variables
        read_params (list): - list variables characterizing the simulations
    
    output:
        comb_data (dict) : dictionary with variables
    
    """
    comb_data = {}
    for key in read_vars+read_params: comb_data[key]=[]
    if not (type(infiles) is list):
        infiles=[infiles]
    for infile in infiles:
        print(infile)
        f_ = h5py.File(infile, "r")
        for key in read_vars:
            comb_data[key].append(np.array(f_[key]))
        for key in read_params: 
            comb_data[key].append(f_[key][()])
        f_.close()

    ###
    for key in read_vars: comb_data[key]=np.concatenate(comb_data[key])
    for key in read_params:
        if key !='simparams/n_subfiles':
            if len(set(comb_data[key]))==1: 
                comb_data[key]=list(set(comb_data[key]))[0]
        else: comb_data[key]=np.array(comb_data[key])
    return(comb_data)


def get_eq_energy(en, g1, g2, W):
    cs1_max = en/W*g1
    cs1_ = np.linspace(0, cs1_max, 501)
    cs2_ = g2*(en/W - cs1_/g1)
    return (cs1_, cs2_)
def make_cs1_cs2_fig(ens = [2.0, 5.0,10.0, 15.0], 
                     yrange=(200,3e4),
                     xrange=(0,150), 
                     figsize=(10,8),
                     g1=0.1423,
                     g2=43.515,
                     W =0.01344,
                     with_cax=True
                     ):
    fig = plt.figure(figsize=figsize, facecolor="w")
    ax_rect = [0.08,0.08, 0.9,0.9]
    if with_cax:
        ax_rect = [0.08,0.08, 0.8,0.9]
    cax_rect = [ax_rect[0]+ax_rect[2]+0.01,
                ax_rect[1],
                0.04, 
                ax_rect[3]]
    ax=fig.add_axes(ax_rect)
    ax.set_yscale("log")
    for en in ens:
        l_ = get_eq_energy(en,g1=g1, g2=g2,W=W)
        plt.plot(l_[0],l_[1], c="0.5", ls ="--")
        if l_[0][-1]<xrange[1]:
            plt.text(l_[0][-1]+1.0, yrange[0]*1.03, "{:0.1f} keVee".format(en),fontsize=13, rotation=270,
                 va="bottom", ha="center", color="0.05")
    plt.xlabel("cS1 area [ PE ]", fontsize=14)
    plt.ylabel("cS2 area [ PE ]", fontsize=14)
    plt.ylim(yrange[0], yrange[1])
    plt.xlim(xrange[0], xrange[1])
    if not with_cax: return fig, ax
    cax = fig.add_axes(cax_rect)
    return fig, ax ,cax

read_vars = [
             'truth/oneweight', 'truth/energy', 'truth/x', 'truth/y', 'truth/z',
             'event/s1_n4tw200',
             'event/s2_area', 'event/s1_area', 
             'event/cs2', 'event/cs1', 'event/ces'
            ]
read_params = ['params/g1', 'params/g2', 'params/W', 'simparams/n_subfiles', ]


def get_FV_bool(d_, maxR, Z_range):
    _FV_bool = np.ones_like(d_['truth/energy']).astype(bool)
    _FV_bool *= (d_['truth/x']**2 + d_['truth/y']**2)<maxR**2
    _FV_bool *= (d_['truth/z']> Z_range[0])
    _FV_bool *= (d_['truth/z']< Z_range[1])
    _fiducial_mass = 2.9*np.pi*maxR**2 * (Z_range[1]-Z_range[0])*1e-9
    return _FV_bool, _fiducial_mass


class cS1_cS2_bins:
    cS1_bins = np.linspace(0.0, 150.0, 151)
    cS2_bins = np.logspace(2,4.75, 110+1)
    
import h5py
from datetime import datetime
### Function to convert histogrm to template format expected by binference.
# copy paste from Jacques
def numpy_to_template(bins, histograms, file_name, histogram_names=None, axis_names=None, 
                      metadata={"version":"0.1.0","date":datetime.now().strftime('%Y%m%d_%H:%M:%S')}):
    if histogram_names is None:
        histogram_names = ["{:d}".format(i) for i in range(len(histograms))]
    with h5py.File(file_name, "w") as f:
        print("file f opened, 1st time, ",list(f.keys()))
        for k, i in metadata.items():
            f.attrs[k] = i
        if axis_names is None:
            axis_names = ["" for i in range(len(bins))]
        for i, (b, bn) in enumerate(zip(bins, axis_names)):
            dset = f.create_dataset("bins/{:d}".format(i), data=b)
            dset.attrs["name"] = bn
        for histogram, histogram_name in zip(histograms, histogram_names):
            print("writing histogram name",histogram_name)
            dset = f.create_dataset("./templates/{:s}".format(histogram_name), data=histogram)