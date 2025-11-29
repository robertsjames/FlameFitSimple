import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy import interpolate

def find_hist_contour_level( val, xedges, yedges, contour_integral=[ 0.95,0.68]):
        """Finding the contour level that contains a given integral

        The basic algorithm is:
            1. Divide z into many levels (ex. 1000) from min(z) to max(z)
            2. For each level t, integrate the hist bin content if the z value is above t
            3. Build a linear interp map from integral to t
            4. Find the t that corresponds to contour_integral

        Args:
            h: TH2F or uproot4 hist type
            contour_integral: list of float

        Returns:
            array
        """
        contour_integral = np.sort(contour_integral)[::-1] # must be decreasing

        # x_c = (xedges.T[0]+xedges.T[1])*0.5
        # y_c = (yedges.T[0]+yedges.T[1])*0.5
        norm = np.sum(val) # normalization
        val = val/norm # normalized
        n = 1000
        t = np.linspace(val.min(), val.max(), n)
        integral = ((val >= t[:, None, None]) * val).sum(axis=(1,2))
        f = interpolate.interp1d(integral, t)
        return f(contour_integral)*norm
def plot_hist_contour(val, xedges, yedges, fill_contour=True, alpha_val=0.25, levels=None,level=None, axes=None, **kwargs):
    """
    Example how to create a contour using find_hist_contour_level.
    returns 
        polys: a list of each contour's coordinates for optional use later.
        cs: contour object returned by plotting call
    """
    if axes==None:
        axes=plt.gca()
    # find the contour levels that contains 68% and 95% integral
    levels = find_hist_contour_level(val, xedges, yedges)
    
    # get numpy arrays, x bin center, y bin center
    
    x_c = 0.5*(xedges[1:]+xedges[:-1])
    y_c = 0.5*(yedges[1:]+yedges[:-1])
    
    x_c = np.concatenate([[3], x_c])
    #x_c[0] = xedges[0]
    x_c[-1] = xedges[-1]
    val = np.pad(val, ((1,0), (0,0)), 'constant', constant_values=((0, 0), (0, 0)))

    # make the contourf plot
    X,Y = np.meshgrid(x_c, y_c)

    polys = [] #list of coords that define the contours
    for l in range(len(levels[::-1])): # plot low level first
        if fill_contour: 
            cs = axes.contourf(X, Y, val.T, levels=[levels[l], np.max(val)], alpha=alpha_val, **kwargs)
            polys.append( cs.allsegs[0][0] )
        else:
            if level is not None: 
                if l==level:
                    cs = axes.contour(X, Y, val.T, levels=[levels[l], np.max(val)], alpha=alpha_val, **kwargs)
                    polys.append( cs.allsegs[0][0] )
            else:
                cs = axes.contour(X, Y, val.T, levels=[levels[l], np.max(val)], alpha=alpha_val, **kwargs)
                polys.append( cs.allsegs[0][0] )
                alpha_val += 0.25
    return polys, cs