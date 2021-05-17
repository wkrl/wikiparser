import os
import glob
import json
from tqdm import tqdm
import argparse


def create_output_file(filename):
    with open(filename, 'w') as f:
        dataset = {"name": "Wikipedia", "language": "en", "documents": []}
        f.write(json.dumps(dataset))
        f.close()

def merge_datasets(filename):
    first_access = True
    subfolders = [subfolder for subfolder in glob.glob('./parsed/*')]

    with open(filename, 'rb+') as f:
        for subfolder in tqdm(subfolders):
            files = glob.glob(subfolder+'/*')
            for file_path in files:
                with open(file_path, 'r') as datafile:
                    data = json.loads(datafile.read())                       
                    documents_string = f'{json.dumps(data["documents"])[1:-1]}]}}'
                    f.seek(-2, os.SEEK_END)         
                    if not first_access:
                        documents_string = f', {documents_string}'
                    first_access = False
                    f.write(str.encode(documents_string))
        f.close()

if __name__ == '__main__':    
    parser = argparse.ArgumentParser();
    parser.add_argument('--output', nargs=1, type=str, action='store', help='Filename for output')    
    args = parser.parse_args()
    
    filename = args.output[0]
    create_output_file(filename)
    merge_datasets(filename)
