from etl import extract_data, transform_data, load_data, run_etl
import pandas as pd

if __name__ == "__main__":
    print("ETL süreci başlatılıyor...")
    run_etl()
    print("ETL süreci tamamlandı.")
