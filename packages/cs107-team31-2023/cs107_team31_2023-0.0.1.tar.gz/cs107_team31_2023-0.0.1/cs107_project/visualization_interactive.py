import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import splrep, splev
import ipywidgets as widgets
from IPython.display import display

class viz_tool_interactive:

    def interactive_spectral(self, wavelen, flux, name):
        def update_plot(smoothing, wavelen_range):
            # Filter data based on selected wavelength range
            mask = (wavelen >= wavelen_range[0]) & (wavelen <= wavelen_range[1])
            filtered_wavelen = wavelen[mask]
            filtered_flux = flux[mask]

            # Update plot with smoothing and selected range
            spline = splrep(filtered_wavelen, filtered_flux, s=smoothing)
            wavelen_infered = np.linspace(min(filtered_wavelen), max(filtered_wavelen), 1000)
            flux_infered = splev(wavelen_infered, spline)

            plt.figure(figsize=(10, 6))
            plt.plot(filtered_wavelen, filtered_flux, label="Original")
            plt.plot(wavelen_infered, flux_infered, label="Smoothed")
            plt.xlabel('Wavelength')
            plt.ylabel('Flux')
            plt.title(f'{name} Spectral Information with Smoothing')
            plt.legend()
            plt.show()

            # Calculate and display flux
            flux_integral = np.trapz(flux_infered, wavelen_infered)
            print(f"Total flux in selected range: {flux_integral}")

        # Sliders for smoothing and wavelength range
        smoothing_slider = widgets.FloatSlider(
            value=1e50,
            min=0,
            max=1e60,
            step=1e10,
            description='Smoothing:',
            continuous_update=False
        )

        wavelen_range_slider = widgets.FloatRangeSlider(
            value=[min(wavelen), max(wavelen)],
            min=min(wavelen),
            max=max(wavelen),
            step=0.01,
            description='Wavelength Range:',
            continuous_update=False
        )

        widgets.interactive(update_plot, smoothing=smoothing_slider, wavelen_range=wavelen_range_slider)
