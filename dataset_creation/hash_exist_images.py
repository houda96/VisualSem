import sys
import hashlib
import glob
from tqdm import tqdm
from collections import defaultdict
import os
import json

BUF_SIZE = 65536
FOLDER = '/home/images/babelnet_images/*'
NEW_FOLDER = '/home/images/new/'
sources_file = "data/img_sources.json"

with open(sources_file, 'r') as f:
    sources_img = json.loads(f.read())

# Hash a file with the sha1 hash
def hash_file(file_name):
    sha1 = hashlib.sha1()
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

# Make sure that folders are present
def create_folder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)

if __name__ == "__main__":
    images = [j for i in glob.glob(FOLDER) for j in glob.glob(i + '/*')]

    # if starting from no earlier files, comment below two lines
    hashes = set()
    new_d = defaultdict(set)
    hash_to_source = defaultdict(list)

    # Now start the duplicate removal
    for im in tqdm(images, mininterval = 10):
        synset = im.split("/")[-2]
        hashh = hash_file(im)
        new_d[synset].add(hashh)
        hash_to_source[hashh].append(sources_img[synset][im.split("/")[-1]])
        if hashh not in hashes:
            hashes.add(hashh)
            create_folder(NEW_FOLDER + hashh[:2])
            os.rename(im, NEW_FOLDER + hashh[:2] + '/' + hashh)
        else:
            os.remove(im)

    hash_to_source = {k : list(set(v)) for k, v in hash_to_source.items()}

    with open("data/hash_to_source.json", "w") as f:
        json.dump(hash_to_source, f)

    with open("data/hashes_magic_dict.json", "w") as f:
        json.dump(new_d, f)

    with open("data/hashes.json", "w") as f:
        json.dump(hashes, f)
