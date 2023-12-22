import shutil
import os

def copy_csv_files():
    src_dir = os.path.join(os.path.dirname(__file__), 'data')
    dst_dir = os.getcwd()  # Current working directory

    for file_name in os.listdir(src_dir):
        if file_name.endswith('.csv'):
            src_path = os.path.join(src_dir, file_name)
            dst_path = os.path.join(dst_dir, file_name)
            shutil.copy(src_path, dst_path)

    print("CSV files copied successfully.")

