FROM apache/airflow:slim-2.9.3-python3.11
COPY requirements.txt .
RUN pip install --no-cache-dir "apache-airflow==2.9.3" -r requirements.txt