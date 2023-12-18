import matplotlib.pyplot as plt 
import numpy as np
# from scipy.interpolate import make_interp_spline
from scipy.interpolate import splrep, splev
import statsmodels.api as sm

class viz_tool:
    
    def plot_spectral(self, wavelen, flux, name):
        '''
        makes spectral visualization given wavelen and flux. Save the plot to name_spectral.png

        input:
        wavelen: numpy array [n, ]
        flux: numpy array [n, ]
        name: string on the name of the object

        returns:
        None, saves the plot to name_spectral.png
        '''
        assert len(wavelen) == len(wavelen)
        assert name != ""
        ## sort the wavelen and flux
        ind = np.argsort(wavelen)
        wavelen_sorted = wavelen[ind]
        flux_sorted = flux[ind]

        ## make smoothing 
        max_wavelen = max(wavelen)
        min_wavelen = min(wavelen)
        # spline = make_interp_spline(wavelen_sorted, flux_sorted,  k = 1) ## smoothing using degree 3 spline 
        spline = splrep(wavelen_sorted,flux_sorted,s=1e50)
        wavelen_infered = np.linspace(min_wavelen, max_wavelen, 1000)
        # flux_infered = spline(wavelen_infered)
        flux_infered = splev(wavelen_infered,spline)

        ## plotting 
        f, ax = plt.subplots()
        ax.plot(wavelen_sorted, flux_sorted, label = "spectral")
        ax.plot(wavelen_infered, flux_infered, label = "infered continum")
        ax.legend()
        ax.set_xlabel('Wavelength')
        ax.set_ylabel('Flux')
        ax.set_title('Spectral Information with Inferred Continuum')

        f.savefig(f"{name}_spectral.png")
        return f, ax, spline

    def plot_spectral_ea(self, wavelen, flux, name):
        '''
        makes the spectral plot with emission and absorption indicated 

        input:
        wavelen: numpy array [n, ]
        flux: numpy array [n, ]
        name: string on the name of the object

        returns:
        None, saves the plot to name_spectral.png
        '''
        f, ax, spline = self.plot_spectral(wavelen, flux, name)

        ## sort the wavelen and flux
        ind = np.argsort(wavelen)
        wavelen_sorted = wavelen[ind]
        flux_sorted = flux[ind]

        ## compute upper and lower bound 
        # flux_pred = spline(wavelen_sorted)
        flux_pred = splev(wavelen_sorted,spline)
        std = np.std(flux_sorted - flux_pred)
        flux_upper = flux_pred + 2.0 * std
        flux_lower = flux_pred - 2.0 * std
        # print(min(flux_sorted - flux_lower))

        emission = np.clip(flux_sorted - flux_upper, a_min = 0, a_max = max(flux_sorted - flux_upper))
        absorption = np.clip(flux_sorted - flux_lower, a_max = 0, a_min = min(flux_sorted - flux_lower))


        for i in range(len(wavelen_sorted)):
            e = emission[i]
            a = absorption[i]
            w = wavelen_sorted[i]
            if e > 0:
                ax.axvline(w, label = "emission", color = "red", zorder = 0)
            if a < 0:
                ax.axvline(w, label = "absorption", color = "blue", zorder = 0)
        # ax.legend()
        # ax.legend(a_lines, "absorption")
        
        f.savefig(f"{name}_spectral_ea.png")

        ## TODO: plot for emission and absorption individually. 
        f_a, ax_a = plt.subplots()
        ax_a.plot(wavelen_sorted, absorption)
        ax_a.set_xlabel('Wavelength')
        ax_a.set_ylabel('Flux')
        ax_a.set_title('Absorption line')
        f_a.savefig(f"{name}_absorption.png")

        f_e, ax_e = plt.subplots()
        ax_e.plot(wavelen_sorted, emission)
        ax_e.set_xlabel('Wavelength')
        ax_e.set_ylabel('Flux')
        ax_e.set_title('Absorption line')
        f_e.savefig(f"{name}_emission.png")

        return {
            "wavelen": wavelen_sorted, 
            "flux": flux_sorted, 
            "emission": emission, 
            "absorption": absorption, 
            "infered_continuum": flux_pred
        }


        




