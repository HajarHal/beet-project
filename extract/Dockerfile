FROM apache/airflow:2.7.1-python3.11

# Switch to root user to install system packages
USER root

# Install required libraries for Chrome and ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libnss3 \
    libgconf-2-4 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Switch to airflow user to install Python packages
USER airflow

# Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip

# Install required Python packages
RUN pip install --no-cache-dir \
    selenium \
    apache-airflow-providers-google \
    webdriver-manager \
    beautifulsoup4 \
    lxml \
    boto3 \
    pandas \
    numpy \
    pyhdf \
    rasterio

# Create a downloads directory
RUN mkdir -p /opt/airflow/output
