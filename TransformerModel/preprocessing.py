import os
from tqdm import tqdm
import lzma
from multiprocessing import Pool, cpu_count
import concurrent.futures


def xz_files_in_dir(directory):
    files = []
    for filename in os.listdir(directory):
        if filename.endswith('.xz') and os.path.isfile(os.path.join(directory, filename)):
            files.append(os.path.join(directory, filename))
    return files


folder_path = '/home/icdmlab/Desktop/openwebtext'
output_file_train = "output_train.txt"
output_file_val = "output_val.txt"
output_file = "output{}.txt"
vocab_file = "vocab.txt"

files = xz_files_in_dir(folder_path)

total_files = len(files)

# Calculate the split indices
split_index = int(total_files * 0.9)
files_train = files[:split_index]
files_val = files[split_index:]

# Process the files for training and validation sperately
vocab = set()

# Process the training files
with open(output_file_train, 'w', encoding="utf-8") as outfile:
    for filename in tqdm(files_train):
        file_path = os.path.join(folder_path, filename)
        with lzma.open(file_path, 'rt', encoding="utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)

# Process the validation files
with open(output_file_val, 'w', encoding="utf-8") as outfile:
    for filename in tqdm(files_val):
        file_path = os.path.join(folder_path, filename)
        with lzma.open(file_path, 'rt', encoding="utf-8") as infile:
            text = infile.read()
            outfile.write(text)
            characters = set(text)
            vocab.update(characters)

# Write the vocabulatry to vocab.txt
with open(vocab_file, "w", encoding="utf-8") as vfile:
    for char in vocab:
        vfile.write(char + '\n')


