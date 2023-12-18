#!/usr/bin/env python3
# File       : cross_match.py
# Description: Enables cross matching between SDSS and Gaia.
# License    : MIT License
# Copyright 2023 Harvard University. All Rights Reserved.
import sys
print(sys.path)
import pandas as pd
from astroquery.gaia import Gaia
from astropy.coordinates import SkyCoord
from astropy import units as u


def extract_gaia_cross_match(coords, radius=1.0):
    """
    Extracts Gaia cross-match data.
    """
    ra_coords = coords['ra']
    dec_coords = coords['dec']
    sdss_coords = SkyCoord(ra=ra_coords * u.degree, dec=dec_coords * u.degree, frame='icrs')
    gaia_cross_match = []
    if radius <= 0:
        raise ValueError("Radius must be positive")
    for coord in sdss_coords:
        try:
            job = Gaia.cone_search_async(coord, radius * u.arcsec)
            gaia_cross_match.append(job.get_results().to_pandas())
        except Exception as e:
            print(f"Error occurred during Gaia cross-match extraction: {str(e)}")
    if not gaia_cross_match:
        print("No Gaia cross-match data found.")
        return pd.DataFrame()  # return an empty DataFrame
    

    return pd.concat(gaia_cross_match, ignore_index=True)



def main():
    print()

if __name__ == "__main__":
    main()