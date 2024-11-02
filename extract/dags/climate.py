import rasterio
import pandas as pd
from rasterio.transform import rowcol
import os

def process_climate_data(cropland_csv, tif_directories, output_csv):
    cropland_df = pd.read_csv(cropland_csv)

    def generate_tif_files(directory, data_type):
        tif_files = []
        for year in range(2019, 2020):
            for month in range(1, 13):
                month_str = f"{month:02d}"
                tif_filename = f"wc2.1_10m_{data_type}_{year}-{month_str}.tif"
                tif_filepath = os.path.join(directory, tif_filename)
                if os.path.exists(tif_filepath):
                    tif_files.append((tif_filepath, f"{data_type}_{year}-{month_str}"))
        return tif_files

    def process_tif_directory(tif_directory, data_type):
        for tif_path, column_name in generate_tif_files(tif_directory, data_type):
            print(f"Traitement du fichier {tif_path}...")
            cropland_df[column_name] = None

            with rasterio.open(tif_path) as src:
                data = src.read(1)
                transform = src.transform

                for index, row in cropland_df.iterrows():
                    lon, lat = row['Longitude'], row['Latitude']
                    pixel_row, pixel_col = rowcol(transform, lon, lat)
                    pixel_row = int(pixel_row)
                    pixel_col = int(pixel_col)

                    if 0 <= pixel_row < data.shape[0] and 0 <= pixel_col < data.shape[1]:
                        value = data[pixel_row, pixel_col]
                        if value != src.nodata:
                            cropland_df.at[index, column_name] = value

    for data_type, tif_directory in tif_directories.items():
        process_tif_directory(tif_directory, data_type)

    cropland_df.to_csv(output_csv, index=False)
    print(f"Les valeurs de tmin, tmax et précipitations ont été ajoutées au fichier CSV '{output_csv}'")

cropland_csv = '/opt/airflow/output/cropland_coords.csv'
tif_directories = {
    'tmin': '/opt/airflow/input/wc2.1_cruts4.06_10m_tmin_2010-2019/',
    'tmax': '/opt/airflow/input/wc2.1_cruts4.06_10m_tmax_2010-2019/',
    'prec': '/opt/airflow/input/wc2.1_cruts4.06_10m_prec_2010-2019/'
}
output_csv = '/opt/airflow/output/cropland_tmin_tmax_prec_all_months.csv'

process_climate_data(cropland_csv, tif_directories, output_csv)
