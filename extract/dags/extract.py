from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 18),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('croplands_data_pipeline', default_args=default_args, schedule_interval='@daily') as dag:

    def extract_cropland_coords(hdf_file, lc_type, cropland_class, output_csv):
        from coord import extract_cropland_coords
        extract_cropland_coords(hdf_file, lc_type, cropland_class, output_csv)

    def extract_uncertainty_values(csv_file, mean_tif_files, output_file):
        from propreties import extract_uncertainty_values
        extract_uncertainty_values(csv_file, mean_tif_files, output_file)

    def process_climate_data(cropland_csv, tif_directories, output_csv_path):
        from climate import process_climate_data
        process_climate_data(cropland_csv, tif_directories, output_csv_path)

    extract_coordinates_task = PythonOperator(
        task_id='extract_coordinates',
        python_callable=extract_cropland_coords,
        op_kwargs={
            'hdf_file': '/opt/airflow/input/MCD12Q1.A2023001.h17v05.061.2024252124735.hdf',
            'lc_type': 'LC_Type1',
            'cropland_class': 12,
            'output_csv': '/opt/airflow/output/cropland_coords.csv'
        }
    )

    extract_properties_task = PythonOperator(
        task_id='extract_properties',
        python_callable=extract_uncertainty_values,
        op_kwargs={
            'csv_file': '/opt/airflow/output/cropland_coords.csv',
            'mean_tif_files': [
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
            ],
            'output_file': '/opt/airflow/output/uncertainty_values_for_all_files.csv'
        }
    )

    climate_task = PythonOperator(
        task_id='process_climate_data',
        python_callable=process_climate_data,
        op_kwargs={
            'cropland_csv': '/opt/airflow/output/uncertainty_values_for_all_files.csv',
            'tif_directories': {
                'tmin': '/opt/airflow/input/wc2.1_cruts4.06_10m_tmin_2010-2019/',
                'tmax': '/opt/airflow/input/wc2.1_cruts4.06_10m_tmax_2010-2019/',
                'prec': '/opt/airflow/input/wc2.1_cruts4.06_10m_prec_2010-2019/'
            },
            'output_csv_path': '/opt/airflow/output/cropland_tmin_tmax_prec_all_months.csv'
        }
    )

    upload_to_gcs_task = LocalFilesystemToGCSOperator(
        task_id='upload_to_gcs',
        src='/opt/airflow/output/cropland_tmin_tmax_prec_all_months.csv',
        dst='cropland_data.csv',
        bucket='beet-bucket-1',
        gcp_conn_id='google_cloud_default'
    )

    extract_coordinates_task >> extract_properties_task >> climate_task >> upload_to_gcs_task
