import os
import gzip

def extract_gz_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.gz'):
            gz_file_path = os.path.join(folder_path, filename)
            output_file_path = os.path.join(folder_path, filename[:-3])
            
            with gzip.open(gz_file_path, 'rb') as gz_file:
                with open(output_file_path, 'wb') as output_file:
                    output_file.write(gz_file.read())

def delete_gz_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.gz'):
            gz_file_path = os.path.join(folder_path, filename)
            os.remove(gz_file_path)