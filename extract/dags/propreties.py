import pandas as pd
import rasterio

def extract_uncertainty_values(csv_file, mean_tif_files, output_file):
    data = pd.read_csv(csv_file)

    lat_min = data['Latitude'].min()
    lat_max = data['Latitude'].max()
    lon_min = data['Longitude'].min()
    lon_max = data['Longitude'].max()

    columns_to_drop = [
        'bdod_60-100', 'clay_60-100', 'sand_60-100', 'silt_60-100',
        'wv0010_60-100', 'wv0033_60-100', 'wv1500_60-100', 'cec_60-100',
        'nitrogen_60-100', 'soc_60-100', 'phh2o_60-100', 'ocd_60-100',
        'ocs_0-30'
    ]
    data = data.drop(columns=columns_to_drop)

    uncertainty_tif_files = [tif_file.replace('.tif', '.tif') for tif_file in mean_tif_files]

    def get_uncertainty_tif_values(tif_file):
        with rasterio.open(tif_file) as src:
            tif_values = src.read(1)
            transform = src.transform
            uncertainty_values = []

            for _, row in data.iterrows():
                lat = row['Latitude']
                lon = row['Longitude']

                if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                    row_idx, col_idx = ~transform * (lon, lat)
                    row_idx, col_idx = int(row_idx), int(col_idx)

                    if 0 <= row_idx < tif_values.shape[0] and 0 <= col_idx < tif_values.shape[1]:
                        tif_value = tif_values[row_idx, col_idx]
                    else:
                        tif_value = None
                else:
                    tif_value = None

                uncertainty_values.append(tif_value)

        return uncertainty_values

    for tif_file in uncertainty_tif_files:
        tif_column_name = tif_file.split('/')[-1].replace('.tif', '')
        data[tif_column_name] = get_uncertainty_tif_values(tif_file)

    data.to_csv(output_file, index=False)
    print(f"Uncertainty values have been extracted for all files and saved in {output_file}.")

csv_file = '/opt/airflow/output/cropland_coords.csv'
mean_tif_files = [
    'opt/airflow/input/data/bdod_60-100.tif',
    'opt/airflow/input/data/clay_60-100.tif',
    'opt/airflow/input/data/sand_60-100.tif',
    'opt/airflow/input/data/silt_60-100.tif',
    'opt/airflow/input/data/wv0010_60-100.tif',
    'opt/airflow/input/data/wv0033_60-100.tif',
    'opt/airflow/input/data/wv1500_60-100.tif',
    'opt/airflow/input/data/cec_60-100.tif',
    'opt/airflow/input/data/nitrogen_60-100.tif',
    'opt/airflow/input/data/soc_60-100.tif',
    'opt/airflow/input/data/phh2o_60-100.tif',
    'opt/airflow/input/data/ocd_60-100.tif',
    'opt/airflow/input/data/ocs_0-30.tif'
]
output_file = 'opt/airflow/output/uncertainty_values_for_all_files.csv'

extract_uncertainty_values(csv_file, mean_tif_files, output_file)
