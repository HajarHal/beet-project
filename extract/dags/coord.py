from pyhdf.SD import SD, SDC
import numpy as np
import pandas as pd

def extract_cropland_coords(hdf_file, lc_type, cropland_class):
    file = SD(hdf_file, SDC.READ)
    land_cover_data = file.select(lc_type)[:]
    cropland_indices = np.where(land_cover_data == cropland_class)

    lat_start, lon_start = 29.8723, -11.5364
    pixel_size = 0.0045

    lat_coords = lat_start + cropland_indices[0] * pixel_size
    lon_coords = lon_start + cropland_indices[1] * pixel_size

    cropland_data = pd.DataFrame({
        'Latitude': lat_coords,
        'Longitude': lon_coords
    })

    return cropland_data

hdf_file = '/opt/airflow/input/MCD12Q1.A2023001.h17v05.061.2024252124735.hdf'
lc_type = 'LC_Type1'
cropland_class = 12

cropland_data = extract_cropland_coords(hdf_file, lc_type, cropland_class)

output_csv = f'/opt/airflow/output/cropland_coords.csv'
cropland_data.to_csv(output_csv, index=False)
